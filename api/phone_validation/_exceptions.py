"""Exceptions for the Phone Validation API."""
from typing import Any


class PhoneValidationAPIError(Exception):
    """Base exception for all Phone Validation API errors."""
    def __init__(self, message: str, details: dict[str, Any] | None = None) -> None:
        self.message = message
        self.details = details or {}
        super().__init__(self.message)


class InvalidPhoneNumberError(PhoneValidationAPIError):
    """Raised when the provided phone number is invalid."""
    pass


class RateLimitExceededError(PhoneValidationAPIError):
    """Raised when the rate limit is exceeded."""
    def __init__(self, retry_after: int | None = None) -> None:
        self.retry_after = retry_after
        super().__init__(
            "Rate limit exceeded. Please try again later.",
            {"retry_after": retry_after} if retry_after else {}
        )


class AuthenticationError(PhoneValidationAPIError):
    """Raised when authentication fails."""
    pass


class ServerError(PhoneValidationAPIError):
    """Raised when there's a server-side error (5xx)."""
    pass


class APIError(PhoneValidationAPIError):
    """Generic API error with status code and details."""
    def __init__(self, message: str, status_code: int, details: dict[str, Any] | None = None) -> None:
        self.status_code = status_code
        super().__init__(message, details)


class ValidationError(PhoneValidationAPIError):
    """Raised when request validation fails."""
    pass
