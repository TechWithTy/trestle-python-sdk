"""Custom exceptions for the Reverse Phone API."""

from typing import Optional, Dict, Any


class ReversePhoneAPIError(Exception):
    """Base exception for all Reverse Phone API errors."""
    def __init__(self, message: str, status_code: Optional[int] = None, details: Optional[Dict[str, Any]] = None):
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)


class InvalidPhoneNumberError(ReversePhoneAPIError):
    """Raised when the provided phone number is invalid."""
    def __init__(self, message: str = "Invalid phone number", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, status_code=400, details=details)


class RateLimitExceededError(ReversePhoneAPIError):
    """Raised when the rate limit is exceeded."""
    def __init__(self, message: str = "Rate limit exceeded", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, status_code=429, details=details)


class AuthenticationError(ReversePhoneAPIError):
    """Raised when authentication fails."""
    def __init__(self, message: str = "Authentication failed", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, status_code=401, details=details)


class ServerError(ReversePhoneAPIError):
    """Raised when there's a server-side error."""
    def __init__(self, message: str = "Internal server error", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, status_code=500, details=details)


class APIError(ReversePhoneAPIError):
    """Raised when the API returns an error."""
    def __init__(self, message: str, status_code: int, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, status_code=status_code, details=details)


class ValidationError(ReversePhoneAPIError):
    """Raised when request validation fails."""
    def __init__(self, message: str = "Validation error", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, status_code=400, details=details)
