"""Custom exceptions for the GuidedMind RAG SDK."""

from typing import Dict, Optional


class GuidedMindError(Exception):
    """Base exception for all GuidedMind SDK errors."""

    pass


class AuthenticationError(GuidedMindError):
    """Raised when authentication fails (401, 403)."""

    pass


class RateLimitError(GuidedMindError):
    """Raised when rate limit is exceeded (429)."""

    pass


class APIError(GuidedMindError):
    """Raised for general API errors."""

    def __init__(
        self,
        message: str,
        status_code: int,
        response_body: Optional[Dict] = None,
    ):
        self.status_code = status_code
        self.response_body = response_body
        # Store sanitized message
        super().__init__(self._get_safe_message(message))

    def _get_safe_message(self, message: str) -> str:
        """Return a safe message without sensitive data."""
        from guidedmind.utils import redact_api_key

        return redact_api_key(message)

    def __str__(self) -> str:
        """Return generic error message for users."""
        return f"API request failed with status {self.status_code}"
