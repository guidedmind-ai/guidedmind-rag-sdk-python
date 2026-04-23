"""GuidedMind RAG SDK for Python.

A production-ready Python SDK for interacting with the GuidedMind RAG API.

Example:
    >>> from guidedmind import Client
    >>> client = Client(api_key="rk_your_api_key")
    >>> response = client.search(query="What are the main features?")
    >>> for result in response.results:
    ...     print(f"{result.score}: {result.content}")
"""

from guidedmind.client import Client
from guidedmind.exceptions import (
    APIError,
    AuthenticationError,
    GuidedMindError,
    RateLimitError,
)
from guidedmind.memory.client import MemoryClient
from guidedmind.memory.long import LongMemoryClient
from guidedmind.memory.short import ShortMemoryClient
from guidedmind.memory.types import (
    AddRecordRequest,
    AddRecordResponse,
    LongMemoryRecord,
    LongMemorySearchResponse,
    LongMemorySearchResult,
    ShortMemoryRecord,
    ShortMemoryRecords,
    StoreRecordRequest,
    StoreRecordResponse,
)
from guidedmind.types import (
    DocumentUploadResponse,
    SearchMethod,
    SearchResponse,
    SearchResult,
    UploadAndProcessResponse,
)
from guidedmind.version import __version__

__all__ = [
    # Version
    "__version__",
    # Clients
    "Client",
    "MemoryClient",
    "ShortMemoryClient",
    "LongMemoryClient",
    # Exceptions
    "GuidedMindError",
    "AuthenticationError",
    "RateLimitError",
    "APIError",
    # Types
    "SearchMethod",
    "SearchResponse",
    "SearchResult",
    "DocumentUploadResponse",
    "UploadAndProcessResponse",
    # Memory types
    "ShortMemoryRecord",
    "ShortMemoryRecords",
    "AddRecordRequest",
    "AddRecordResponse",
    "LongMemoryRecord",
    "LongMemorySearchResult",
    "LongMemorySearchResponse",
    "StoreRecordRequest",
    "StoreRecordResponse",
]
