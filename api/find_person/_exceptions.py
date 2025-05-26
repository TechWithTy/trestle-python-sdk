"""Exceptions for the Find Person API."""
from typing import Any


class FindPersonAPIError(Exception):
    """Base exception for all Find Person API errors."""
    def __init__(self, message: str, details: dict[str, Any] | None = None) -> None:
        self.message = message
        self.details = details or {}
        super().__init__(self.message)


class InvalidSearchCriteriaError(FindPersonAPIError):
    """Raised when the search criteria are invalid or insufficient."""
    pass


class RateLimitExceededError(FindPersonAPIError):
    """Raised when the rate limit is exceeded."""
    def __init__(self, retry_after: int | None = None) -> None:
        self.retry_after = retry_after
        super().__init__(
            "Rate limit exceeded. Please try again later.",
            {"retry_after": retry_after} if retry_after else {}
        )


class AuthenticationError(FindPersonAPIError):
    """Raised when authentication fails."""
    pass


class ServerError(FindPersonAPIError):
    """Raised when there's a server-side error (5xx)."""
    pass


class APIError(FindPersonAPIError):
    """Generic API error with status code and details."""
    def __init__(self, message: str, status_code: int, details: dict[str, Any] | None = None) -> None:
        self.status_code = status_code
        super().__init__(message, details)


class ValidationError(FindPersonAPIError):
    """Raised when request validation fails."""
    pass
