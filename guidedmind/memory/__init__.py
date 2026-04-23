"""Memory module for the GuidedMind SDK."""

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

__all__ = [
    # Clients
    "MemoryClient",
    "ShortMemoryClient",
    "LongMemoryClient",
    # Short memory types
    "ShortMemoryRecord",
    "ShortMemoryRecords",
    "AddRecordRequest",
    "AddRecordResponse",
    # Long memory types
    "LongMemoryRecord",
    "LongMemorySearchResult",
    "LongMemorySearchResponse",
    "StoreRecordRequest",
    "StoreRecordResponse",
]
