"""Main client for the GuidedMind RAG SDK."""

import os
import ssl
from datetime import datetime
from typing import Any, Dict, Optional

import httpx
from httpx import Limits
from tenacity import retry, stop_after_attempt, wait_exponential

from guidedmind.documents.client import DocumentsClient
from guidedmind.exceptions import APIError, AuthenticationError, RateLimitError
from guidedmind.memory.client import MemoryClient
from guidedmind.types import SearchMethod, SearchResponse
from guidedmind.utils import (
    DEFAULT_MAX_CONNECTIONS,
    DEFAULT_MAX_KEEPALIVE_CONNECTIONS,
    DEFAULT_MAX_RETRIES,
    DEFAULT_TIMEOUT,
    get_user_agent,
    log_request,
    validate_api_key,
    validate_base_url,
    validate_limit,
    validate_query,
    validate_threshold,
)


class Client:
    """Main GuidedMind RAG SDK client.

    Provides methods for searching documents and managing document operations.

    Example:
        >>> from guidedmind import Client
        >>> client = Client(api_key="rk_your_api_key")
        >>> response = client.search(query="What are the main features?")
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = "https://api.guidedmind.ai",
        timeout: float = DEFAULT_TIMEOUT,
        max_retries: int = DEFAULT_MAX_RETRIES,
    ):
        """Initialize the client.

        Args:
            api_key: API key for authentication. If not provided,
                     uses GUIDEDMIND_API_KEY environment variable.
            base_url: Base URL for the API.
            timeout: Request timeout in seconds.
            max_retries: Maximum number of retry attempts.

        Raises:
            ValueError: If API key is missing or invalid.
            ValueError: If base_url doesn't use HTTPS.
        """
        # Get API key from argument or environment variable
        api_key_value = api_key or os.environ.get("GUIDEDMIND_API_KEY")

        # Validate API key (will raise ValueError if None or invalid)
        validate_api_key(api_key_value)

        # Store validated API key (assert to narrow type from Optional[str] to str)
        assert api_key_value is not None
        self._api_key = api_key_value

        # Validate base URL
        validate_base_url(base_url)
        self._base_url = base_url

        # Validate timeout
        if timeout <= 0:
            raise ValueError("timeout must be positive")
        self._timeout = httpx.Timeout(
            connect=5.0,
            read=timeout,
            write=5.0,
            pool=5.0,
        )

        # Validate max retries
        if max_retries < 0:
            raise ValueError("max_retries cannot be negative")
        self._max_retries = max_retries

        # Create SSL context with minimum TLS 1.2
        self._ssl_context = ssl.create_default_context()
        self._ssl_context.minimum_version = ssl.TLSVersion.TLSv1_2

        # Initialize HTTP clients
        self._client: Optional[httpx.Client] = None
        self._async_client: Optional[httpx.AsyncClient] = None

        # Initialize documents sub-client
        self.documents = DocumentsClient(self)

        # Initialize memory sub-client
        self.memory = MemoryClient(self)

    @property
    def _headers(self) -> Dict[str, str]:
        """Get request headers with authentication."""
        return {
            "User-Agent": get_user_agent(),
            "X-API-Key": self._api_key,
            "Content-Type": "application/json",
        }

    def _get_client(self) -> httpx.Client:
        """Get or create synchronous HTTP client.

        Returns:
            Configured httpx.Client instance.
        """
        if self._client is None:
            self._client = httpx.Client(
                base_url=self._base_url,
                timeout=self._timeout,
                headers=self._headers,
                verify=self._ssl_context,
                limits=Limits(
                    max_connections=DEFAULT_MAX_CONNECTIONS,
                    max_keepalive_connections=DEFAULT_MAX_KEEPALIVE_CONNECTIONS,
                    keepalive_expiry=5.0,
                ),
            )
        return self._client

    async def _get_async_client(self) -> httpx.AsyncClient:
        """Get or create asynchronous HTTP client.

        Returns:
            Configured httpx.AsyncClient instance.
        """
        if self._async_client is None:
            self._async_client = httpx.AsyncClient(
                base_url=self._base_url,
                timeout=self._timeout,
                headers=self._headers,
                verify=self._ssl_context,
                limits=Limits(
                    max_connections=DEFAULT_MAX_CONNECTIONS,
                    max_keepalive_connections=DEFAULT_MAX_KEEPALIVE_CONNECTIONS,
                    keepalive_expiry=5.0,
                ),
            )
        return self._async_client

    def _handle_response_error(self, response: httpx.Response) -> None:
        """Handle response errors and raise appropriate exceptions.

        Args:
            response: HTTP response that failed.

        Raises:
            AuthenticationError: If status is 401 or 403.
            RateLimitError: If status is 429.
            APIError: For other error statuses.
        """
        if response.status_code == 401:
            raise AuthenticationError(
                "Authentication failed. Please check your API key."
            )

        if response.status_code == 403:
            raise AuthenticationError(
                "Access denied. Please check your API key permissions."
            )

        if response.status_code == 429:
            retry_after = response.headers.get("Retry-After", "60")
            raise RateLimitError(
                f"Rate limit exceeded. Please retry after {retry_after} seconds."
            )

        # For other errors, try to get error message from response
        try:
            response_json = response.json()
            error_message = response_json.get("detail", response_json.get("error", ""))
        except Exception:
            error_message = response.text

        raise APIError(
            message=error_message,
            status_code=response.status_code,
            response_body=response.json() if response.status_code >= 400 else None,
        )

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10),
        reraise=True,
    )
    def search(
        self,
        query: str,
        limit: int = 5,
        threshold: float = 0.7,
        include_metadata: bool = True,
        search_method: Optional[SearchMethod] = None,
        context_strategy: Optional[str] = None,
    ) -> SearchResponse:
        """Search documents in the RAG project.

        Args:
            query: Search query string.
            limit: Number of results to return (1-20).
            threshold: Similarity threshold (0.0-1.0).
            include_metadata: Whether to include metadata in results.
            search_method: Override search method (dense, sparse, hybrid, graph).
            context_strategy: Override context assembly strategy.

        Returns:
            SearchResponse with results and metadata.

        Raises:
            APIError: If the API request fails.
            AuthenticationError: If authentication fails.
            RateLimitError: If rate limit is exceeded.
            ValueError: If parameters are invalid.
        """
        # Validate parameters
        query = validate_query(query)
        limit = validate_limit(limit)
        threshold = validate_threshold(threshold)

        # Build request payload
        payload: Dict[str, Any] = {
            "query": query,
            "limit": limit,
            "threshold": threshold,
            "include_metadata": include_metadata,
        }

        # Add optional parameters
        if search_method is not None:
            payload["search_method"] = search_method.value

        if context_strategy is not None:
            payload["context_strategy"] = context_strategy

        # Make request
        start_time = datetime.utcnow()
        client = self._get_client()

        try:
            response = client.post("/rag/search", json=payload)

            # Log request
            duration_ms = int((datetime.utcnow() - start_time).total_seconds() * 1000)
            log_request("POST", "/rag/search", response.status_code, duration_ms)

            # Handle errors
            if response.status_code >= 400:
                self._handle_response_error(response)

            # Parse response
            return SearchResponse.model_validate(response.json())

        except httpx.TimeoutException:
            raise APIError(
                message="Request timed out",
                status_code=408,
            ) from None
        except httpx.NetworkError as e:
            raise APIError(
                message=f"Network error: {str(e)}",
                status_code=0,
            ) from e

    async def asearch(
        self,
        query: str,
        limit: int = 5,
        threshold: float = 0.7,
        include_metadata: bool = True,
        search_method: Optional[SearchMethod] = None,
        context_strategy: Optional[str] = None,
    ) -> SearchResponse:
        """Async version of search().

        Args:
            query: Search query string.
            limit: Number of results to return (1-20).
            threshold: Similarity threshold (0.0-1.0).
            include_metadata: Whether to include metadata in results.
            search_method: Override search method (dense, sparse, hybrid, graph).
            context_strategy: Override context assembly strategy.

        Returns:
            SearchResponse with results and metadata.

        Raises:
            APIError: If the API request fails.
            AuthenticationError: If authentication fails.
            RateLimitError: If rate limit is exceeded.
            ValueError: If parameters are invalid.
        """
        # Validate parameters
        query = validate_query(query)
        limit = validate_limit(limit)
        threshold = validate_threshold(threshold)

        # Build request payload
        payload: Dict[str, Any] = {
            "query": query,
            "limit": limit,
            "threshold": threshold,
            "include_metadata": include_metadata,
        }

        # Add optional parameters
        if search_method is not None:
            payload["search_method"] = search_method.value

        if context_strategy is not None:
            payload["context_strategy"] = context_strategy

        # Make request
        start_time = datetime.utcnow()
        client = await self._get_async_client()

        try:
            response = await client.post("/rag/search", json=payload)

            # Log request
            duration_ms = int((datetime.utcnow() - start_time).total_seconds() * 1000)
            log_request("POST", "/rag/search", response.status_code, duration_ms)

            # Handle errors
            if response.status_code >= 400:
                self._handle_response_error(response)

            # Parse response
            return SearchResponse.model_validate(response.json())

        except httpx.TimeoutException:
            raise APIError(
                message="Request timed out",
                status_code=408,
            ) from None
        except httpx.NetworkError as e:
            raise APIError(
                message=f"Network error: {str(e)}",
                status_code=0,
            ) from e

    def close(self) -> None:
        """Close the HTTP client and release resources."""
        if self._client is not None:
            self._client.close()
            self._client = None

        if self._async_client is not None:
            # Note: async client will be closed via aclose()
            # This is a no-op for sync close
            self._async_client = None

    async def aclose(self) -> None:
        """Async version of close()."""
        if self._client is not None:
            self._client.close()
            self._client = None

        if self._async_client is not None:
            await self._async_client.aclose()
            self._async_client = None

    def __enter__(self) -> "Client":
        """Context manager entry."""
        return self

    def __exit__(
        self,
        exc_type: Optional[type],
        exc_val: Optional[BaseException],
        exc_tb: Optional[object],
    ) -> None:
        """Context manager exit."""
        self.close()

    async def __aenter__(self) -> "Client":
        """Async context manager entry."""
        return self

    async def __aexit__(
        self,
        exc_type: Optional[type],
        exc_val: Optional[BaseException],
        exc_tb: Optional[object],
    ) -> None:
        """Async context manager exit."""
        await self.aclose()
