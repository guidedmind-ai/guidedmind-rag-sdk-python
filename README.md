# GuidedMind RAG SDK Python

Official Python SDK for the GuidedMind platform. A production-ready, type-safe client for interacting with GuidedMind's RAG, Short Memory, and Long Memory services.

## Features

- **Type-safe interfaces** with Pydantic v2 data models
- **Async support** for non-blocking operations
- **Comprehensive error handling** with custom exceptions
- **Automatic retries** with exponential backoff
- **Secure by default** with HTTPS enforcement and API key validation
- **Structured logging** with API key redaction
- **Unified client** for RAG, Short Memory, and Long Memory operations

## Quick Start

### Installation

```bash
pip install guidedmind-rag-sdk-python
```

### Get Your API Key

1. Sign up at [GuidedMind](https://guidedmind.ai)
2. Navigate to API Keys in your dashboard
3. Generate a new API key

### Basic Usage

```python
from guidedmind import Client

# Initialize client with API key
client = Client(api_key="your_api_key")

# Or use environment variable
# export GUIDEDMIND_API_KEY="your_api_key"
client = Client()
```

## Core Functionality

### 1. RAG (Retrieval-Augmented Generation)

Search your documents with semantic, keyword, or hybrid search.

```python
from guidedmind import Client, SearchMethod

client = Client(api_key="your_api_key")

# Simple semantic search
response = client.search(query="What are the main features?")

print(f"Found {len(response.results)} results")
for result in response.results:
    print(f"- {result.content[:100]}... (score: {result.score:.3f})")

# Advanced hybrid search
response = client.search(
    query="Explain the microservices architecture",
    limit=10,
    threshold=0.75,
    search_method=SearchMethod.HYBRID,
    include_metadata=True
)

print(f"Search method: {response.metadata.search_method_used}")
print(f"Processing time: {response.metadata.processing_time_ms}ms")
```

### 2. Short Memory

Session-based conversation memory with automatic expiration.

```python
from guidedmind import Client

client = Client(api_key="your_api_key")

# Add conversation records
user_record = client.memory.short.add_record(
    session_id="session-123",
    role="user",
    content="What pricing plans do you offer?"
)

assistant_record = client.memory.short.add_record(
    session_id="session-123",
    role="assistant",
    content="We offer Free, Pro, and Enterprise plans."
)

# Retrieve all records for a session
records = client.memory.short.get_records(session_id="session-123")

print(f"Total records: {records.total}")
for record in records.records:
    print(f"{record.role}: {record.content}")
```

### 3. Long Memory

Persistent, searchable conversation memory with automatic summarization.

```python
from guidedmind import Client

client = Client(api_key="your_api_key")

# Store conversation records
client.memory.long.store_record(
    user_id="user-456",
    role="user",
    content="I'm interested in the Pro plan for my team of 10"
)

client.memory.long.store_record(
    user_id="user-456",
    role="assistant",
    content="The Pro plan includes advanced features for teams up to 20 members."
)

# Search long-term memories
response = client.memory.long.search(
    query="What did the user say about pricing?",
    limit=10,
    threshold=0.75
)

print(f"Found {response.total} relevant memories")
for result in response.results:
    print(f"- {result.content} (score: {result.score:.3f})")
```

### 4. Document Management

Upload and process documents for RAG.

```python
from guidedmind import Client

client = Client(api_key="your_api_key")

# Upload and process a document
response = client.documents.upload_and_process(
    file_path="technical-docs.pdf",
    metadata={"team": "engineering", "version": "2.1"}
)

print(f"Document uploaded: {response.document_id}")
print(f"Chunks created: {response.chunks_created}")
```

## Async Support

All operations have async versions for non-blocking I/O.

```python
import asyncio
from guidedmind import Client

async def main():
    client = Client(api_key="your_api_key")
    
    # Async RAG search
    response = await client.asearch(
        query="How does authentication work?",
        limit=10,
        threshold=0.75
    )
    
    # Async short memory
    records = await client.memory.short.aget_records(session_id="session-123")
    
    # Async long memory
    memories = await client.memory.long.search(
        query="user preferences",
        limit=5
    )
    
    # Async document upload
    upload_response = await client.documents.aupload_and_process(
        file_path="doc.pdf"
    )

asyncio.run(main())
```

## Context Manager

The SDK supports context managers for automatic resource cleanup.

```python
from guidedmind import Client

# Synchronous context manager
with Client(api_key="your_api_key") as client:
    response = client.search(query="What is RAG?")
    print(response.results)

# Async context manager
import asyncio

async def main():
    async with Client(api_key="your_api_key") as client:
        response = await client.asearch(query="What is RAG?")
        print(response.results)

asyncio.run(main())
```

## Integration with AI Frameworks

### LangChain Integration

```python
from langchain.vectorstores import BaseVectorStore
from guidedmind import Client

class GuidedMindVectorStore(BaseVectorStore):
    def __init__(self, client: Client):
        self.client = client
    
    def similarity_search(self, query: str, k: int = 4):
        response = self.client.search(query=query, limit=k)
        return [result.content for result in response.results]

# Usage
client = Client(api_key="your_api_key")
vectorstore = GuidedMindVectorStore(client)
docs = vectorstore.similarity_search("microservices architecture", k=5)
```

### LlamaIndex Integration

```python
from llama_index.core.base.response.schema import Response
from guidedmind import Client

class GuidedMindRetriever:
    def __init__(self, client: Client):
        self.client = client
    
    def retrieve(self, query: str, top_k: int = 5):
        response = self.client.search(query=query, limit=top_k)
        return [result.content for result in response.results]

# Usage
client = Client(api_key="your_api_key")
retriever = GuidedMindRetriever(client)
context = retriever.retrieve("API authentication", top_k=3)
```

## API Reference

### Client

The main entry point for the SDK.

#### Constructor

```python
Client(
    api_key: Optional[str] = None,
    base_url: str = "https://api.guidedmind.ai",
    timeout: float = 30.0,
    max_retries: int = 3
)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `api_key` | `str` | `None` | API key (or use `GUIDEDMIND_API_KEY` env var) |
| `base_url` | `str` | `"https://api.guidedmind.ai"` | API base URL (must use HTTPS) |
| `timeout` | `float` | `30.0` | Request timeout in seconds |
| `max_retries` | `int` | `3` | Maximum retry attempts |

#### Methods

| Method | Description |
|--------|-------------|
| `search()` | Search documents (synchronous) |
| `asearch()` | Search documents (asynchronous) |
| `close()` | Close HTTP client |
| `aclose()` | Close HTTP client (async) |

### DocumentsClient

Accessed via `client.documents`.

| Method | Description |
|--------|-------------|
| `upload()` | Upload document without processing |
| `upload_and_process()` | Upload and process document |
| `aupload()` | Async upload |
| `aupload_and_process()` | Async upload and process |

### ShortMemoryClient

Accessed via `client.memory.short`.

| Method | Description |
|--------|-------------|
| `get_records()` | Get all records for a session |
| `add_record()` | Add a new record to a session |
| `aget_records()` | Async get records |
| `aadd_record()` | Async add record |

### LongMemoryClient

Accessed via `client.memory.long`.

| Method | Description |
|--------|-------------|
| `search()` | Search long memory records |
| `store_record()` | Store a new long memory record |
| `asearch()` | Async search |
| `astore_record()` | Async store record |

### Search Methods

| Method | Description |
|--------|-------------|
| `SearchMethod.DENSE` | Vector-based semantic search |
| `SearchMethod.SPARSE` | Keyword-based BM25 search |
| `SearchMethod.HYBRID` | Combined dense + sparse search |
| `SearchMethod.GRAPH` | Knowledge graph-based search |

## Error Handling

The SDK provides custom exceptions for different error scenarios:

```python
from guidedmind import Client, APIError, AuthenticationError, RateLimitError

client = Client(api_key="your_api_key")

try:
    response = client.search(query="What is RAG?")
except AuthenticationError as e:
    # 401/403 errors
    print(f"Authentication failed: {e}")
except RateLimitError as e:
    # 429 errors
    print(f"Rate limit exceeded: {e}")
except APIError as e:
    # Other API errors
    print(f"API error {e.status_code}: {e}")
```

## Security

### API Key Management

**DO:**
- Use environment variables for API keys (`GUIDEDMIND_API_KEY`)
- Store keys in secret management services (AWS Secrets Manager, HashiCorp Vault)
- Use `.env` files with proper `.gitignore`
- Rotate keys regularly

**DON'T:**
- Hardcode API keys in source code
- Commit API keys to version control
- Log API keys (the SDK automatically redacts them)

```python
# ✅ GOOD
from guidedmind import Client
import os

client = Client()  # Uses GUIDEDMIND_API_KEY env var
# or
client = Client(api_key=os.environ.get("GUIDEDMIND_API_KEY"))

# ❌ BAD
client = Client(api_key="12345678_...")  # Never hardcode!
```

### Security Features

- ✅ **API key validation** - Validates key format before use
- ✅ **API key redaction** - Automatically redacts keys in logs and errors
- ✅ **HTTPS enforcement** - Requires TLS 1.2+ connections
- ✅ **Input validation** - Validates all user inputs
- ✅ **Structured logging** - Logs without sensitive data
- ✅ **Secure error handling** - Error messages don't leak sensitive info

## Configuration

### Logging

```python
import logging
from guidedmind import Client

# Enable debug logging
logging.getLogger("guidedmind").setLevel(logging.DEBUG)
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

client = Client(api_key="your_api_key")
```

### Custom Timeout

```python
client = Client(
    api_key="your_api_key",
    timeout=60.0  # 60 second timeout
)
```

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Support

- **Documentation**: https://github.com/guidedmind/guidedmind-rag-sdk-python#readme
- **Issues**: https://github.com/guidedmind/guidedmind-rag-sdk-python/issues
- **Email**: support@guidedmind.com
