"""Short Memory client for the GuidedMind SDK."""

from datetime import datetime
from typing import Any, Dict, Optional

import httpx

from guidedmind.memory.types import (
    AddRecordRequest,
    AddRecordResponse,
    ShortMemoryRecords,
)


class ShortMemoryClient:
    """Client for short memory operations.

    Short memory provides session-based conversation memory with automatic expiration.

    Example:
        >>> from guidedmind import Client
        >>> client = Client(api_key="mk_your_api_key")
        >>>
        >>> # Get records for a session
        >>> records = client.memory.short.get_records(session_id="session-123")
        >>>
        >>> # Add a new record
        >>> response = client.memory.short.add_record(
        ...     session_id="session-123",
        ...     role="user",
        ...     content="Hello!"
        ... )
    """

    def __init__(self, parent_client: Any):
        """Initialize short memory client.

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

    def get_records(self, session_id: str) -> ShortMemoryRecords:
        """Get all records for a session.

        Args:
            session_id: Session identifier

        Returns:
            ShortMemoryRecords with list of records

        Raises:
            AuthenticationError: If API key is invalid
            APIError: If request fails
        """
        url = f"{self._parent._base_url}/api/v1/memory/short/messages/{session_id}"

        response = self._parent._get_client().get(url, headers=self._get_headers())
        if response.status_code >= 400:
            self._parent._handle_response_error(response)

        data = response.json()
        return ShortMemoryRecords(**data)

    async def aget_records(self, session_id: str) -> ShortMemoryRecords:
        """Async version of get_records().

        Args:
            session_id: Session identifier

        Returns:
            ShortMemoryRecords with list of records

        Raises:
            AuthenticationError: If API key is invalid
            APIError: If request fails
        """
        url = f"{self._parent._base_url}/api/v1/memory/short/messages/{session_id}"

        response = await (await self._parent._get_async_client()).get(
            url, headers=self._get_headers()
        )
        if response.status_code >= 400:
            self._parent._handle_response_error(response)

        data = response.json()
        return ShortMemoryRecords(**data)

    def add_record(
        self,
        session_id: str,
        role: str,
        content: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> AddRecordResponse:
        """Add a new record to a session.

        Args:
            session_id: Session identifier
            role: Role ("user" or "assistant")
            content: Message content
            metadata: Optional metadata dictionary

        Returns:
            AddRecordResponse with record ID

        Raises:
            AuthenticationError: If API key is invalid
            APIError: If request fails
        """
        url = f"{self._parent._base_url}/api/v1/memory/short/record"

        request = AddRecordRequest(
            session_id=session_id,
            role=role,
            content=content,
            metadata=metadata,
        )

        response = self._parent._get_client().post(
            url, headers=self._get_headers(), json=request.model_dump()
        )
        if response.status_code >= 400:
            self._parent._handle_response_error(response)

        data = response.json()
        return AddRecordResponse(**data)

    async def aadd_record(
        self,
        session_id: str,
        role: str,
        content: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> AddRecordResponse:
        """Async version of add_record().

        Args:
            session_id: Session identifier
            role: Role ("user" or "assistant")
            content: Message content
            metadata: Optional metadata dictionary

        Returns:
            AddRecordResponse with record ID

        Raises:
            AuthenticationError: If API key is invalid
            APIError: If request fails
        """
        url = f"{self._parent._base_url}/api/v1/memory/short/record"

        request = AddRecordRequest(
            session_id=session_id,
            role=role,
            content=content,
            metadata=metadata,
        )

        response = await (await self._parent._get_async_client()).post(
            url, headers=self._get_headers(), json=request.model_dump()
        )
        if response.status_code >= 400:
            self._parent._handle_response_error(response)

        data = response.json()
        return AddRecordResponse(**data)
