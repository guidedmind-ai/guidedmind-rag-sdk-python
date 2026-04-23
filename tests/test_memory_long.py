"""Tests for Long Memory client."""

import pytest
from unittest.mock import AsyncMock, Mock, patch

from guidedmind import Client
from guidedmind.memory.types import LongMemorySearchResponse, StoreRecordResponse


class TestLongMemoryClient:
    """Test Long Memory client."""

    @pytest.fixture
    def client(self):
        """Create test client."""
        return Client(api_key="rk_test_key_1234567890")

    def test_search(self, client):
        """Test searching long memory."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "records": [
                {
                    "id": "1",
                    "memory_user_id": "user-123",
                    "record_type": "summary",
                    "category": "preference",
                    "content": "User asked about pricing",
                    "confidence": 0.95,
                    "heat_score": 0.8,
                    "access_count": 5,
                    "last_accessed_at": "2024-01-01T00:00:00Z",
                    "created_at": "2024-01-01T00:00:00Z",
                    "updated_at": "2024-01-01T00:00:00Z",
                    "version": 1,
                    "qdrant_synced": True,
                }
            ],
            "total_count": 1,
            "query": "pricing",
        }

        with patch.object(client.memory, "_get_client") as mock_get_client:
            mock_get_client.return_value.post.return_value = mock_response

            response = client.memory.long.search(
                query="pricing", external_user_id="user-123", limit=20
            )

            assert isinstance(response, LongMemorySearchResponse)
            assert len(response.records) == 1
            assert response.records[0].confidence == 0.95
            assert response.total_count == 1

    @pytest.mark.asyncio
    async def test_asearch(self, client):
        """Test async search."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "records": [],
            "total_count": 0,
            "query": "test query",
        }

        with patch.object(client.memory, "_get_async_client") as mock_get_async:
            mock_get_async.return_value = AsyncMock()
            mock_get_async.return_value.post.return_value = mock_response

            response = await client.memory.long.asearch(
                query="test query", external_user_id="user-123", limit=10
            )

            assert isinstance(response, LongMemorySearchResponse)
            assert response.total_count == 0

    def test_store_record(self, client):
        """Test storing a record."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "record_id": "long-memory-789",
            "created_at": "2024-01-01T00:00:00Z",
            "success": True,
        }

        with patch.object(client.memory, "_get_client") as mock_get_client:
            mock_get_client.return_value.post.return_value = mock_response

            response = client.memory.long.store_record(
                user_id="user-456",
                role="user",
                content="Important information",
            )

            assert isinstance(response, StoreRecordResponse)
            assert response.record_id == "long-memory-789"
            assert response.success is True

    @pytest.mark.asyncio
    async def test_astore_record(self, client):
        """Test async store record."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "record_id": "long-memory-012",
            "created_at": "2024-01-01T00:00:00Z",
            "success": True,
        }

        with patch.object(client.memory, "_get_async_client") as mock_get_async:
            mock_get_async.return_value = AsyncMock()
            mock_get_async.return_value.post.return_value = mock_response

            response = await client.memory.long.astore_record(
                user_id="user-789",
                role="assistant",
                content="Response message",
                session_id="session-abc",
            )

            assert isinstance(response, StoreRecordResponse)
            assert response.success is True

    def test_store_record_with_metadata(self, client):
        """Test storing a record with metadata."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "record_id": "long-memory-345",
            "created_at": "2024-01-01T00:00:00Z",
            "success": True,
        }

        with patch.object(client.memory, "_get_client") as mock_get_client:
            mock_get_client.return_value.post.return_value = mock_response

            response = client.memory.long.store_record(
                user_id="user-456",
                role="user",
                content="Important information",
                metadata={"category": "preferences"},
            )

            assert isinstance(response, StoreRecordResponse)
            assert response.success is True

    @pytest.mark.asyncio
    async def test_astore_record_with_metadata(self, client):
        """Test async store record with metadata."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "record_id": "long-memory-678",
            "created_at": "2024-01-01T00:00:00Z",
            "success": True,
        }

        with patch.object(client.memory, "_get_async_client") as mock_get_async:
            mock_get_async.return_value = AsyncMock()
            mock_get_async.return_value.post.return_value = mock_response

            response = await client.memory.long.astore_record(
                user_id="user-456",
                role="user",
                content="Important information",
                metadata={"category": "preferences"},
            )

            assert isinstance(response, StoreRecordResponse)
            assert response.success is True

    def test_search_with_threshold(self, client):
        """Test search with custom threshold."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "records": [],
            "total_count": 0,
            "query": "pricing",
        }

        with patch.object(client.memory, "_get_client") as mock_get_client:
            mock_get_client.return_value.post.return_value = mock_response

            response = client.memory.long.search(
                query="pricing", external_user_id="user-123", limit=20, threshold=0.85
            )

            assert isinstance(response, LongMemorySearchResponse)
            assert response.query == "pricing"

    @pytest.mark.asyncio
    async def test_asearch_with_offset(self, client):
        """Test async search with offset."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "records": [],
            "total_count": 0,
            "query": "test",
        }

        with patch.object(client.memory, "_get_async_client") as mock_get_async:
            mock_get_async.return_value = AsyncMock()
            mock_get_async.return_value.post.return_value = mock_response

            response = await client.memory.long.asearch(
                query="test", external_user_id="user-123", limit=10, offset=20
            )

            assert isinstance(response, LongMemorySearchResponse)
            assert response.total_count == 0
