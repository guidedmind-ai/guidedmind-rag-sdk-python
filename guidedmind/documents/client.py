"""Documents client for the GuidedMind RAG SDK."""

import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional, Union

import httpx

from guidedmind.exceptions import APIError
from guidedmind.types import DocumentUploadResponse, UploadAndProcessResponse
from guidedmind.utils import (
    log_request,
    validate_file_path,
)


class DocumentsClient:
    """Client for document operations.

    Provides methods for uploading and processing documents.

    Example:
        >>> from guidedmind import Client
        >>> client = Client(api_key="rk_your_api_key")
        >>> response = client.documents.upload(file_path="doc.pdf")
    """

    def __init__(self, parent_client: Any):
        """Initialize the documents client.

        Args:
            parent_client: Parent Client instance for HTTP operations.
        """
        self._parent = parent_client

    def _handle_response_error(self, response: httpx.Response) -> None:
        """Handle response errors and raise appropriate exceptions.

        Args:
            response: HTTP response that failed.

        Raises:
            APIError: For error statuses.
        """
        if response.status_code == 401:
            from guidedmind.exceptions import AuthenticationError

            raise AuthenticationError(
                "Authentication failed. Please check your API key."
            )

        if response.status_code == 403:
            from guidedmind.exceptions import AuthenticationError

            raise AuthenticationError(
                "Access denied. Please check your API key permissions."
            )

        if response.status_code == 429:
            from guidedmind.exceptions import RateLimitError

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

    def upload(
        self,
        file_path: Union[str, Path],
        config: Optional[Dict[str, Any]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> DocumentUploadResponse:
        """Upload a document without processing.

        Args:
            file_path: Path to the document file.
            config: Optional processing configuration.
            metadata: Optional document metadata.

        Returns:
            DocumentUploadResponse with document details.

        Raises:
            FileNotFoundError: If file doesn't exist.
            ValueError: If file is too large or path is invalid.
            APIError: If the API request fails.
        """
        # Validate file path
        path = validate_file_path(file_path)

        # Build request payload
        payload: Dict[str, Any] = {}

        if config is not None:
            payload["config"] = config

        if metadata is not None:
            payload["metadata"] = metadata

        # Make request with file
        start_time = datetime.utcnow()

        with open(path, "rb") as f:
            files = {"file": (path.name, f, "application/octet-stream")}
            data = payload

            client = self._parent._get_client()

            try:
                response = client.post("/rag/upload", files=files, data=data)

                # Log request
                duration_ms = int(
                    (datetime.utcnow() - start_time).total_seconds() * 1000
                )
                log_request("POST", "/rag/upload", response.status_code, duration_ms)

                # Handle errors
                if response.status_code >= 400:
                    self._handle_response_error(response)

                # Parse response
                return DocumentUploadResponse.model_validate(response.json())

            except httpx.TimeoutException:
                raise APIError(
                    message="Request timed out",
                    status_code=408,
                )
            except httpx.NetworkError as e:
                raise APIError(
                    message=f"Network error: {str(e)}",
                    status_code=0,
                )

    def upload_and_process(
        self,
        file_path: Union[str, Path],
        config: Optional[Dict[str, Any]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> UploadAndProcessResponse:
        """Upload and immediately process a document.

        Args:
            file_path: Path to the document file.
            config: Optional processing configuration.
            metadata: Optional document metadata.

        Returns:
            UploadAndProcessResponse with processing details.

        Raises:
            FileNotFoundError: If file doesn't exist.
            ValueError: If file is too large or path is invalid.
            APIError: If the API request fails.
        """
        # Validate file path
        path = validate_file_path(file_path)

        # Build request payload
        payload: Dict[str, Any] = {}

        if config is not None:
            payload["config"] = config

        if metadata is not None:
            payload["metadata"] = metadata

        # Make request with file
        start_time = datetime.utcnow()

        with open(path, "rb") as f:
            files = {"file": (path.name, f, "application/octet-stream")}
            data = payload

            client = self._parent._get_client()

            try:
                response = client.post(
                    "/rag/upload-and-process", files=files, data=data
                )

                # Log request
                duration_ms = int(
                    (datetime.utcnow() - start_time).total_seconds() * 1000
                )
                log_request(
                    "POST", "/rag/upload-and-process", response.status_code, duration_ms
                )

                # Handle errors
                if response.status_code >= 400:
                    self._handle_response_error(response)

                # Parse response
                return UploadAndProcessResponse.model_validate(response.json())

            except httpx.TimeoutException:
                raise APIError(
                    message="Request timed out",
                    status_code=408,
                )
            except httpx.NetworkError as e:
                raise APIError(
                    message=f"Network error: {str(e)}",
                    status_code=0,
                )

    async def aupload(
        self,
        file_path: Union[str, Path],
        config: Optional[Dict[str, Any]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> DocumentUploadResponse:
        """Async version of upload().

        Args:
            file_path: Path to the document file.
            config: Optional processing configuration.
            metadata: Optional document metadata.

        Returns:
            DocumentUploadResponse with document details.

        Raises:
            FileNotFoundError: If file doesn't exist.
            ValueError: If file is too large or path is invalid.
            APIError: If the API request fails.
        """
        # Validate file path
        path = validate_file_path(file_path)

        # Build request payload
        payload: Dict[str, Any] = {}

        if config is not None:
            payload["config"] = config

        if metadata is not None:
            payload["metadata"] = metadata

        # Make request with file
        start_time = datetime.utcnow()

        with open(path, "rb") as f:
            # Read file content
            content = f.read()

            files = {"file": (path.name, content, "application/octet-stream")}
            data = payload

            client = await self._parent._get_async_client()

            try:
                response = await client.post("/rag/upload", files=files, data=data)

                # Log request
                duration_ms = int(
                    (datetime.utcnow() - start_time).total_seconds() * 1000
                )
                log_request("POST", "/rag/upload", response.status_code, duration_ms)

                # Handle errors
                if response.status_code >= 400:
                    self._handle_response_error(response)

                # Parse response
                return DocumentUploadResponse.model_validate(response.json())

            except httpx.TimeoutException:
                raise APIError(
                    message="Request timed out",
                    status_code=408,
                )
            except httpx.NetworkError as e:
                raise APIError(
                    message=f"Network error: {str(e)}",
                    status_code=0,
                )

    async def aupload_and_process(
        self,
        file_path: Union[str, Path],
        config: Optional[Dict[str, Any]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> UploadAndProcessResponse:
        """Async version of upload_and_process().

        Args:
            file_path: Path to the document file.
            config: Optional processing configuration.
            metadata: Optional document metadata.

        Returns:
            UploadAndProcessResponse with processing details.

        Raises:
            FileNotFoundError: If file doesn't exist.
            ValueError: If file is too large or path is invalid.
            APIError: If the API request fails.
        """
        # Validate file path
        path = validate_file_path(file_path)

        # Build request payload
        payload: Dict[str, Any] = {}

        if config is not None:
            payload["config"] = config

        if metadata is not None:
            payload["metadata"] = metadata

        # Make request with file
        start_time = datetime.utcnow()

        with open(path, "rb") as f:
            # Read file content
            content = f.read()

            files = {"file": (path.name, content, "application/octet-stream")}
            data = payload

            client = await self._parent._get_async_client()

            try:
                response = await client.post(
                    "/rag/upload-and-process", files=files, data=data
                )

                # Log request
                duration_ms = int(
                    (datetime.utcnow() - start_time).total_seconds() * 1000
                )
                log_request(
                    "POST", "/rag/upload-and-process", response.status_code, duration_ms
                )

                # Handle errors
                if response.status_code >= 400:
                    self._handle_response_error(response)

                # Parse response
                return UploadAndProcessResponse.model_validate(response.json())

            except httpx.TimeoutException:
                raise APIError(
                    message="Request timed out",
                    status_code=408,
                )
            except httpx.NetworkError as e:
                raise APIError(
                    message=f"Network error: {str(e)}",
                    status_code=0,
                )
