"""Tests for Short Memory client."""

import pytest
from unittest.mock import AsyncMock, Mock, patch

from guidedmind import Client
from guidedmind.memory.types import ShortMemoryRecords, AddRecordResponse


class TestShortMemoryClient:
    """Test Short Memory client."""

    @pytest.fixture
    def client(self):
        """Create test client."""
        return Client(api_key="rk_test_key_1234567890")

    def test_get_records(self, client):
        """Test getting records for a session."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "messages": [
                {
                    "role": "user",
                    "content": "Hello",
                    "timestamp": "2024-01-01T00:00:00Z",
                }
            ],
            "session_id": "test-session",
            "total_count": 1,
        }

        with patch.object(client.memory, "_get_client") as mock_get_client:
            mock_get_client.return_value.get.return_value = mock_response

            records = client.memory.short.get_records(session_id="test-session")

            assert isinstance(records, ShortMemoryRecords)
            assert len(records.messages) == 1
            assert records.messages[0].content == "Hello"

    @pytest.mark.asyncio
    async def test_aget_records(self, client):
        """Test async get records."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "messages": [],
            "session_id": "test-session",
            "total_count": 0,
        }

        with patch.object(client.memory, "_get_async_client") as mock_get_async:
            mock_get_async.return_value = AsyncMock()
            mock_get_async.return_value.get.return_value = mock_response

            records = await client.memory.short.aget_records(session_id="test-session")

            assert isinstance(records, ShortMemoryRecords)
            assert records.total_count == 0

    def test_add_record(self, client):
        """Test adding a record."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "record_id": "new-record-123",
            "created_at": "2024-01-01T00:00:00Z",
            "success": True,
        }

        with patch.object(client.memory, "_get_client") as mock_get_client:
            mock_get_client.return_value.post.return_value = mock_response

            response = client.memory.short.add_record(
                session_id="test-session",
                role="user",
                content="Test message",
            )

            assert isinstance(response, AddRecordResponse)
            assert response.record_id == "new-record-123"
            assert response.success is True

    @pytest.mark.asyncio
    async def test_aadd_record(self, client):
        """Test async add record."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "record_id": "new-record-456",
            "created_at": "2024-01-01T00:00:00Z",
            "success": True,
        }

        with patch.object(client.memory, "_get_async_client") as mock_get_async:
            mock_get_async.return_value = AsyncMock()
            mock_get_async.return_value.post.return_value = mock_response

            response = await client.memory.short.aadd_record(
                session_id="test-session",
                role="assistant",
                content="Test response",
            )

            assert isinstance(response, AddRecordResponse)
            assert response.success is True

    def test_add_record_with_metadata(self, client):
        """Test adding a record with metadata."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "record_id": "new-record-789",
            "created_at": "2024-01-01T00:00:00Z",
            "success": True,
        }

        with patch.object(client.memory, "_get_client") as mock_get_client:
            mock_get_client.return_value.post.return_value = mock_response

            response = client.memory.short.add_record(
                session_id="test-session",
                role="user",
                content="Test message",
                metadata={"timestamp": "2024-01-01T00:00:00Z"},
            )

            assert isinstance(response, AddRecordResponse)
            assert response.success is True

    @pytest.mark.asyncio
    async def test_aadd_record_with_metadata(self, client):
        """Test async add record with metadata."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "record_id": "new-record-012",
            "created_at": "2024-01-01T00:00:00Z",
            "success": True,
        }

        with patch.object(client.memory, "_get_async_client") as mock_get_async:
            mock_get_async.return_value = AsyncMock()
            mock_get_async.return_value.post.return_value = mock_response

            response = await client.memory.short.aadd_record(
                session_id="test-session",
                role="user",
                content="Test message",
                metadata={"timestamp": "2024-01-01T00:00:00Z"},
            )

            assert isinstance(response, AddRecordResponse)
            assert response.success is True
