"""Trestle Phone Feedback API.

This module provides access to the Trestle Phone Feedback API, allowing you to
submit feedback about phone number status and right party contact.

Example:
    ```python
    from trestle import TrestleAPIClient
    from trestle.api.phone_feedback import PhoneFeedbackRequest
    
    async with TrestleAPIClient() as client:
        feedback = PhoneFeedbackRequest(
            response_id="T_b5d031b8-e8a3-4eef-8fa8-d87d3b7e386f",
"""

from __future__ import annotations

from ._exceptions import (
    PhoneFeedbackAPIError,
    PhoneFeedbackAuthenticationError,
    PhoneFeedbackRateLimitError,
    PhoneFeedbackValidationError,
)
from ._requests import PhoneFeedbackRequest
from ._responses import PhoneFeedbackError, PhoneFeedbackResponse
from .phone_feedback import PhoneFeedbackAPI

__all__ = [
    # Models
    "PhoneFeedbackRequest",
    "PhoneFeedbackResponse",
    "PhoneFeedbackError",
    # Exceptions
    "PhoneFeedbackAPIError",
    "PhoneFeedbackValidationError",
    "PhoneFeedbackRateLimitError",
    "PhoneFeedbackAuthenticationError",
    # Client
    "PhoneFeedbackAPI",
]
