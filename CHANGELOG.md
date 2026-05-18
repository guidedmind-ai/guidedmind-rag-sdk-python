# Changelog

All notable changes to the GuidedMind RAG SDK Python will be documented in this file.

## [0.1.1] - 2026-05-18

### Fixed
- **APIError message propagation**: `APIError.__str__()` now includes the actual error message from the server response instead of only the HTTP status code. Previously, errors like `"Search method 'hybrid' is not available for this project"` were lost, showing only `"API request failed with status 500"`. Now the full message is preserved: `"API request failed with status 500: Search method 'hybrid' is not available for this project"`.

## [0.1.0] - 2026-05-17

### Added
- Initial release of the GuidedMind RAG SDK Python
- Core `Client` class with `search()` and `asearch()` methods
- Document upload and processing support
- Short-term and long-term memory clients
- JSON response parsing with error handling
- Retry logic with exponential backoff
- API key redaction in error messages
- SSL/TLS 1.2+ enforcement
- Rate limit and authentication error handling
