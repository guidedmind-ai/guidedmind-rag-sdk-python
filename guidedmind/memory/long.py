"""Long Memory client for the GuidedMind SDK."""

from typing import Any, Dict, Optional

from guidedmind.memory.types import (
    LongMemorySearchResponse,
    StoreRecordRequest,
    StoreRecordResponse,
)


class LongMemoryClient:
    """Client for long memory operations.

    Long memory provides persistent, searchable conversation memory with summarization.

    Example:
        >>> from guidedmind import Client
        >>> client = Client(api_key="mk_your_api_key")
        >>>
        >>> # Search long-term memories
        >>> response = client.memory.long.search(
        ...     query="What did the user say about pricing?",
        ...     limit=10,
        ...     threshold=0.75
        ... )
        >>>
        >>> # Store a new memory
        >>> record = client.memory.long.store_record(
        ...     user_id="user-456",
        ...     role="user",
        ...     content="User prefers the Pro plan"
        ... )
    """

    def __init__(self, parent_client: Any):
        """Initialize long memory client.

        Args:
            parent_client: Parent Client instance for shared configuration
        """
        self._parent = parent_client

    def _get_headers(self) -> Dict[str, str]:
        """Get request headers."""
        return {
            "Content-Type": "application/json",
            "X-Memory-Api-Key": self._parent._api_key,
        }

    def search(
        self,
        query: str,
        external_user_id: str,
        limit: int = 20,
        offset: int = 0,
        threshold: float = 0.7,
    ) -> LongMemorySearchResponse:
        """Search long memory records.

        Args:
            query: Search query string
            external_user_id: External user identifier (required)
            limit: Maximum results to return (default: 20)
            offset: Result offset for pagination (default: 0)
            threshold: Minimum similarity threshold (default: 0.7)

        Returns:
            LongMemorySearchResponse with search results

        Raises:
            AuthenticationError: If API key is invalid
            APIError: If request fails
        """
        url = f"{self._parent._base_url}/api/v1/memory/long/search"

        payload = {
            "query": query,
            "external_user_id": external_user_id,
            "limit": limit,
            "offset": offset,
            "threshold": threshold,
        }

        response = self._parent._get_client().post(
            url, headers=self._get_headers(), json=payload
        )
        if response.status_code >= 400:
            self._parent._handle_response_error(response)

        data = response.json()
        return LongMemorySearchResponse(**data)

    async def asearch(
        self,
        query: str,
        external_user_id: str,
        limit: int = 20,
        offset: int = 0,
        threshold: float = 0.7,
    ) -> LongMemorySearchResponse:
        """Async version of search().

        Args:
            query: Search query string
            external_user_id: External user identifier (required)
            limit: Maximum results to return (default: 20)
            offset: Result offset for pagination (default: 0)
            threshold: Minimum similarity threshold (default: 0.7)

        Returns:
            LongMemorySearchResponse with search results

        Raises:
            AuthenticationError: If API key is invalid
            APIError: If request fails
        """
        url = f"{self._parent._base_url}/api/v1/memory/long/search"

        payload = {
            "query": query,
            "external_user_id": external_user_id,
            "limit": limit,
            "offset": offset,
            "threshold": threshold,
        }

        response = await (await self._parent._get_async_client()).post(
            url, headers=self._get_headers(), json=payload
        )
        if response.status_code >= 400:
            self._parent._handle_response_error(response)

        data = response.json()
        return LongMemorySearchResponse(**data)

    def store_record(
        self,
        user_id: str,
        role: str,
        content: str,
        session_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> StoreRecordResponse:
        """Store a new long memory record.

        Args:
            user_id: User identifier
            role: Role ("user" or "assistant")
            content: Message content
            session_id: Optional session identifier
            metadata: Optional metadata dictionary

        Returns:
            StoreRecordResponse with record ID

        Raises:
            AuthenticationError: If API key is invalid
            APIError: If request fails
        """
        url = f"{self._parent._base_url}/api/v1/memory/long/record"

        request = StoreRecordRequest(
            user_id=user_id,
            role=role,
            content=content,
            session_id=session_id,
            metadata=metadata,
        )

        response = self._parent._get_client().post(
            url, headers=self._get_headers(), json=request.model_dump()
        )
        if response.status_code >= 400:
            self._parent._handle_response_error(response)

        data = response.json()
        return StoreRecordResponse(**data)

    async def astore_record(
        self,
        user_id: str,
        role: str,
        content: str,
        session_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> StoreRecordResponse:
        """Async version of store_record().

        Args:
            user_id: User identifier
            role: Role ("user" or "assistant")
            content: Message content
            session_id: Optional session identifier
            metadata: Optional metadata dictionary

        Returns:
            StoreRecordResponse with record ID

        Raises:
            AuthenticationError: If API key is invalid
            APIError: If request fails
        """
        url = f"{self._parent._base_url}/api/v1/memory/long/record"

        request = StoreRecordRequest(
            user_id=user_id,
            role=role,
            content=content,
            session_id=session_id,
            metadata=metadata,
        )

        response = await (await self._parent._get_async_client()).post(
            url, headers=self._get_headers(), json=request.model_dump()
        )
        if response.status_code >= 400:
            self._parent._handle_response_error(response)

        data = response.json()
        return StoreRecordResponse(**data)
