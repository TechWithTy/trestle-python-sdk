"""Exceptions for the Reverse Address API."""
from typing import Any


class ReverseAddressAPIError(Exception):
    """Base exception for all Reverse Address API errors."""
    def __init__(self, message: str, details: dict[str, Any] | None = None) -> None:
        self.message = message
        self.details = details or {}
        super().__init__(self.message)


class InvalidAddressError(ReverseAddressAPIError):
    """Raised when the provided address is invalid."""
    pass


class RateLimitExceededError(ReverseAddressAPIError):
    """Raised when the rate limit is exceeded."""
    def __init__(self, retry_after: int | None = None) -> None:
        self.retry_after = retry_after
        super().__init__(
            "Rate limit exceeded. Please try again later.",
            {"retry_after": retry_after} if retry_after else {}
        )


class AuthenticationError(ReverseAddressAPIError):
    """Raised when authentication fails."""
    pass


class ServerError(ReverseAddressAPIError):
    """Raised when there's a server-side error (5xx)."""
    pass


class APIError(ReverseAddressAPIError):
    """Generic API error with status code and details."""
    def __init__(self, message: str, status_code: int, details: dict[str, Any] | None = None) -> None:
        self.status_code = status_code
        super().__init__(message, details)


class ValidationError(ReverseAddressAPIError):
    """Raised when request validation fails."""
    pass
