"""Memory client wrapper for the GuidedMind SDK."""

from typing import Any, Dict, cast

from guidedmind.memory.long import LongMemoryClient
from guidedmind.memory.short import ShortMemoryClient


class MemoryClient:
    """Wrapper client for memory operations.

    Provides access to both short-term and long-term memory clients.

    Example:
        >>> from guidedmind import Client
        >>> client = Client(api_key="mk_your_api_key")
        >>>
        >>> # Short memory operations
        >>> records = client.memory.short.get_records(session_id="session-123")
        >>>
        >>> # Long memory operations
        >>> response = client.memory.long.search(query="pricing")
    """

    def __init__(self, parent_client: Any):
        """Initialize memory client.

        Args:
            parent_client: Parent Client instance for shared configuration
        """
        self._parent = parent_client
        self.short = ShortMemoryClient(self)
        self.long = LongMemoryClient(self)

    @property
    def _base_url(self) -> str:
        """Delegate to parent client's base_url."""
        return cast(str, self._parent._base_url)

    @property
    def _api_key(self) -> str:
        """Delegate to parent client's api_key."""
        return cast(str, self._parent._api_key)

    @property
    def _headers(self) -> Dict[str, str]:
        """Delegate to parent client's headers."""
        return cast(Dict[str, str], self._parent._headers)

    def _get_client(self) -> Any:
        """Delegate to parent client's _get_client."""
        return self._parent._get_client()

    async def _get_async_client(self) -> Any:
        """Delegate to parent client's _get_async_client."""
        return await self._parent._get_async_client()

    def _handle_response_error(self, response: Any) -> None:
        """Delegate to parent client's _handle_response_error."""
        self._parent._handle_response_error(response)
