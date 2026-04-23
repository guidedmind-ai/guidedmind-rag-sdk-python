"""Types for the GuidedMind Memory SDK."""

from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


# Short Memory Types
class ShortMemoryRecord(BaseModel):
    """A single short memory record."""

    id: str = Field(..., description="Unique record ID")
    session_id: str = Field(..., description="Session identifier")
    role: str = Field(..., description="Role ('user' or 'assistant')")
    content: str = Field(..., description="Message content")
    created_at: datetime = Field(..., description="Creation timestamp")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")


class ShortMemoryMessage(BaseModel):
    """A single message in short memory."""

    role: str = Field(..., description="Role ('user' or 'assistant')")
    content: str = Field(..., description="Message content")
    timestamp: datetime = Field(..., description="Message timestamp")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")


class ShortMemoryRecords(BaseModel):
    """Response from get_records."""

    session_id: str = Field(..., description="Session identifier")
    messages: List[ShortMemoryMessage] = Field(..., description="List of messages")
    total_count: int = Field(..., description="Total number of messages")


class AddRecordRequest(BaseModel):
    """Request to add a short memory record."""

    session_id: str = Field(..., description="Session identifier")
    role: str = Field(..., description="Role ('user' or 'assistant')")
    content: str = Field(..., description="Message content")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")


class AddRecordResponse(BaseModel):
    """Response from add_record."""

    record_id: str = Field(..., description="Created record ID")
    created_at: datetime = Field(..., description="Creation timestamp")
    success: bool = Field(..., description="Operation success status")


# Long Memory Types
class LongMemoryRecord(BaseModel):
    """A single long memory record."""

    id: str = Field(..., description="Unique record ID")
    user_id: str = Field(..., description="User identifier")
    role: str = Field(..., description="Role ('user' or 'assistant')")
    content: str = Field(..., description="Message content")
    session_id: Optional[str] = Field(None, description="Optional session ID")
    created_at: datetime = Field(..., description="Creation timestamp")
    summary: Optional[str] = Field(None, description="Generated summary")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")
    heat_score: Optional[float] = Field(None, description="Heat score for recency")


class LongMemorySearchResult(BaseModel):
    """A search result from long memory."""

    id: str = Field(..., description="Record ID")
    memory_user_id: str = Field(..., description="Memory user ID")
    record_type: str = Field(..., description="Record type")
    category: str = Field(..., description="Category")
    content: str = Field(..., description="Record content")
    confidence: float = Field(..., description="Confidence score")
    heat_score: float = Field(..., description="Heat score")
    access_count: int = Field(..., description="Access count")
    last_accessed_at: datetime = Field(..., description="Last accessed timestamp")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Update timestamp")
    expires_at: Optional[datetime] = Field(None, description="Expiration timestamp")
    version: int = Field(..., description="Record version")
    qdrant_synced: bool = Field(..., description="Qdrant sync status")


class LongMemorySearchResponse(BaseModel):
    """Response from long memory search."""

    records: List[LongMemorySearchResult] = Field(..., description="Search results")
    total_count: int = Field(..., description="Total number of results")
    query: str = Field(..., description="Original search query")


class StoreRecordRequest(BaseModel):
    """Request to store a long memory record."""

    user_id: str = Field(..., description="User identifier")
    role: str = Field(..., description="Role ('user' or 'assistant')")
    content: str = Field(..., description="Message content")
    session_id: Optional[str] = Field(None, description="Optional session ID")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")


class StoreRecordResponse(BaseModel):
    """Response from store_record."""

    record_id: str = Field(..., description="Created record ID")
    created_at: datetime = Field(..., description="Creation timestamp")
    success: bool = Field(..., description="Operation success status")
