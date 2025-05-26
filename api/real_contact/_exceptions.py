"""Exceptions for the Real Contact API."""

from ...exceptions import TrestleAPIError
from typing import Any

class RealContactAPIError(TrestleAPIError):
    """Base exception for Real Contact API errors."""
    pass


class InvalidSearchCriteriaError(RealContactAPIError):
    """Raised when search criteria are invalid or insufficient."""
    def __init__(self, message: str, details: dict[str, Any] | None = None):
        super().__init__(message, status_code=400, details=details)


class AuthenticationError(RealContactAPIError):
    """Raised when authentication fails (invalid or missing API key)."""
    def __init__(self, message: str = "Authentication failed"):
        super().__init__(message, status_code=401)


class RateLimitExceededError(RealContactAPIError):
    """Raised when the rate limit has been exceeded."""
    def __init__(self, retry_after: int = 60):
        self.retry_after = retry_after
        super().__init__(
            f"Rate limit exceeded. Please try again in {retry_after} seconds.",
            status_code=429,
            headers={"Retry-After": str(retry_after)},
        )


class ValidationError(RealContactAPIError):
    """Raised when request validation fails."""
    def __init__(self, message: str, details: dict[str, Any] | None = None):
        super().__init__(f"Validation error: {message}", status_code=400, details=details)


class ServerError(RealContactAPIError):
    """Raised when a server error occurs."""
    def __init__(self, message: str = "Internal server error"):
        super().__init__(message, status_code=500)


class APIError(RealContactAPIError):
    """Raised for other API errors."""
    def __init__(self, message: str, status_code: int, details: dict[str, Any] | None = None):
        super().__init__(message, status_code=status_code, details=details)
