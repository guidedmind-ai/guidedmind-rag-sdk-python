"""Utility functions for the GuidedMind RAG SDK."""

import logging
import re
from pathlib import Path
from typing import Optional, Union

from guidedmind.version import __version__

# Configure logger
logger = logging.getLogger("guidedmind")
logger.setLevel(logging.INFO)

# API key pattern for redaction (supports both rk_ for RAG and mk_ for Memory)
API_KEY_PATTERN = re.compile(r"(rk_|mk_)[a-zA-Z0-9_]+")

# Default configuration
DEFAULT_TIMEOUT = 30.0
DEFAULT_MAX_RETRIES = 3
DEFAULT_MAX_CONNECTIONS = 10
DEFAULT_MAX_KEEPALIVE_CONNECTIONS = 5
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100 MB


def redact_api_key(text: str) -> str:
    """Redact API keys from text.

    Args:
        text: Text that may contain API keys.

    Returns:
        Text with API keys redacted.
    """
    return API_KEY_PATTERN.sub("rk_***REDACTED***", text)


def validate_api_key(api_key: str) -> None:
    """Validate API key format before use.

    Args:
        api_key: API key to validate.

    Raises:
        ValueError: If API key is invalid.
    """
    if not api_key:
        raise ValueError("API key is required")

    # SDK is agnostic to API key prefixes - validation is done server-side
    # RAG keys use 'rk_' prefix, memory keys have no prefix

    # Check minimum length
    if len(api_key) < 8:
        raise ValueError("API key appears to be too short")


def validate_file_path(file_path: Union[str, Path]) -> Path:
    """Validate and resolve file path.

    Args:
        file_path: Path to the file.

    Returns:
        Resolved Path object.

    Raises:
        FileNotFoundError: If file doesn't exist.
        ValueError: If path is not a file or file is too large.
    """
    path = Path(file_path).expanduser().resolve()

    # Check if file exists
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    # Check if it's a file (not directory)
    if not path.is_file():
        raise ValueError(f"Path is not a file: {file_path}")

    # Check for path traversal attempts (log for monitoring)
    original = str(file_path)
    if ".." in original:
        logger.warning(f"Path traversal detected in: {file_path}")

    # Check file size before upload
    file_size = path.stat().st_size
    if file_size > MAX_FILE_SIZE:
        raise ValueError(
            f"File too large: {file_size / (1024 * 1024):.2f}MB "
            f"(max: {MAX_FILE_SIZE / (1024 * 1024):.0f}MB)"
        )

    return path


def validate_query(query: str) -> str:
    """Validate search query.

    Args:
        query: Search query string.

    Returns:
        Validated and stripped query.

    Raises:
        ValueError: If query is invalid.
    """
    if not query or not query.strip():
        raise ValueError("Query cannot be empty")

    query = query.strip()

    # Length limits
    if len(query) < 1:
        raise ValueError("Query too short")

    if len(query) > 1000:
        raise ValueError("Query too long (max 1000 characters)")

    # Check for obvious injection attempts
    dangerous_patterns = [
        "<script",
        "javascript:",
        "onerror=",
        "onclick=",
        "--",
        "/*",
        "*/",
    ]

    query_lower = query.lower()
    for pattern in dangerous_patterns:
        if pattern in query_lower:
            raise ValueError("Query contains potentially dangerous content")

    return query


def validate_limit(limit: int) -> int:
    """Validate limit parameter.

    Args:
        limit: Number of results to return.

    Returns:
        Validated limit.

    Raises:
        TypeError: If limit is not an integer.
        ValueError: If limit is out of range.
    """
    if not isinstance(limit, int):
        raise TypeError("limit must be an integer")

    if limit < 1:
        raise ValueError("limit must be at least 1")

    if limit > 20:
        raise ValueError("limit cannot exceed 20")

    return limit


def validate_threshold(threshold: float) -> float:
    """Validate threshold parameter.

    Args:
        threshold: Similarity threshold.

    Returns:
        Validated threshold.

    Raises:
        TypeError: If threshold is not a number.
        ValueError: If threshold is out of range.
    """
    if not isinstance(threshold, (int, float)):
        raise TypeError("threshold must be a number")

    if threshold < 0.0 or threshold > 1.0:
        raise ValueError("threshold must be between 0.0 and 1.0")

    return float(threshold)


def validate_base_url(base_url: str) -> None:
    """Validate base URL.

    Args:
        base_url: Base URL for the API.

    Raises:
        ValueError: If URL doesn't use HTTPS.
    """
    if not base_url.startswith("https://"):
        raise ValueError(
            "base_url must use HTTPS for secure communication. " f"Got: {base_url}"
        )


def get_user_agent() -> str:
    """Generate User-Agent header.

    Returns:
        User-Agent string identifying the SDK.
    """
    import sys

    return f"guidedmind-rag-sdk-python/{__version__} (Python/{sys.version_info.major}.{sys.version_info.minor})"


def log_request(
    method: str,
    endpoint: str,
    status_code: int,
    duration_ms: int,
    error: Optional[str] = None,
) -> None:
    """Log request with structured data.

    Args:
        method: HTTP method.
        endpoint: API endpoint.
        status_code: Response status code.
        duration_ms: Request duration in milliseconds.
        error: Optional error message.
    """
    from datetime import datetime

    log_data = {
        "timestamp": datetime.utcnow().isoformat(),
        "event": "api_request",
        "method": method,
        "endpoint": endpoint,
        "status_code": status_code,
        "duration_ms": duration_ms,
        "sdk_version": __version__,
    }

    if error:
        log_data["error"] = redact_api_key(error)
        logger.warning(log_data)
    else:
        logger.info(log_data)
