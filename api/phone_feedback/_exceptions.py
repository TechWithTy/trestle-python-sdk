"""Exceptions for the Phone Feedback API."""

from trestle.exceptions import TrestleAPIError


class PhoneFeedbackAPIError(TrestleAPIError):
    """Base exception for all Phone Feedback API errors."""
    pass


class PhoneFeedbackValidationError(PhoneFeedbackAPIError):
    """Raised when phone feedback validation fails."""
    pass


class PhoneFeedbackRateLimitError(PhoneFeedbackAPIError):
    """Raised when rate limit is exceeded for phone feedback API."""
    pass


class PhoneFeedbackAuthenticationError(PhoneFeedbackAPIError):
    """Raised when authentication fails for phone feedback API."""
    pass
