"""Pydantic data models for the GuidedMind RAG SDK."""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class SearchMethod(str, Enum):
    """Available search methods."""

    DENSE = "dense"
    SPARSE = "sparse"
    HYBRID = "hybrid"
    GRAPH = "graph"


class SearchResult(BaseModel):
    """Individual search result."""

    content: str = Field(..., description="The content of the search result")
    score: float = Field(..., description="Similarity score (0.0-1.0)")
    document_id: Optional[str] = Field(None, description="Document ID")
    document_name: Optional[str] = Field(None, description="Document name")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")


class SearchMetadata(BaseModel):
    """Metadata about the search."""

    project_id: int = Field(..., description="Project ID")
    project_name: str = Field(..., description="Project name")
    processing_time_ms: int = Field(..., description="Processing time in milliseconds")
    chunks_retrieved: int = Field(..., description="Number of chunks retrieved")
    search_method_used: str = Field(..., description="Search method used")
    timestamp: str = Field(..., description="Search timestamp (ISO 8601)")


class SearchResponse(BaseModel):
    """Response from a search request."""

    query: str = Field(..., description="Original search query")
    answer: Optional[str] = Field(None, description="Generated answer (if available)")
    results: List[SearchResult] = Field(..., description="Search results")
    metadata: SearchMetadata = Field(..., description="Search metadata")


class DocumentUploadResponse(BaseModel):
    """Response from document upload."""

    document_id: str = Field(..., description="Unique document ID")
    project_id: int = Field(..., description="Project ID")
    filename: str = Field(..., description="Uploaded filename")
    status: str = Field(..., description="Document status")
    created_at: datetime = Field(..., description="Creation timestamp")


class UploadAndProcessResponse(BaseModel):
    """Response from upload and process."""

    document_id: str = Field(..., description="Unique document ID")
    project_id: int = Field(..., description="Project ID")
    filename: str = Field(..., description="Uploaded filename")
    status: str = Field(..., description="Processing status")
    chunks_created: int = Field(..., description="Number of chunks created")
    processing_time_ms: int = Field(..., description="Processing time in milliseconds")
    created_at: datetime = Field(..., description="Creation timestamp")
