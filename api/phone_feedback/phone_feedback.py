"""Phone Feedback API client for Trestle.

This module provides a client for interacting with the Trestle Phone Feedback API,
which allows submitting feedback about phone number status and right party contact.
"""
from __future__ import annotations

from typing import Any

import httpx

from ...client import TrestleAPIClient
from ._exceptions import (
    PhoneFeedbackAPIError,
    PhoneFeedbackAuthenticationError,
    PhoneFeedbackRateLimitError,
    PhoneFeedbackValidationError,
)
from ._requests import PhoneFeedbackRequest
from ._responses import PhoneFeedbackResponse


class PhoneFeedbackAPI:
    """Client for the Trestle Phone Feedback API.

    Example:
        ```python
        async with TrestleAPIClient() as client:
            feedback = PhoneFeedbackRequest(
                response_id="T_b5d031b8-e8a3-4eef-8fa8-d87d3b7e386f",
                phone="2069735100",
                name="John Doe",
                phone_status="Connected",
                phone_right_party_contact=True
            )
            result = await client.phone_feedback.submit_feedback(feedback)
            print(f"Feedback status: {result.status}")
        ```
    """

    def __init__(self, client: TrestleAPIClient) -> None:
        """Initialize the Phone Feedback API client.

        Args:
            client: An instance of TrestleAPIClient.
        """
        self._client = client
        self._base_url = f"{client._config.base_url.rstrip('/')}/1.0"

    async def submit_feedback(
        self,
        feedback: PhoneFeedbackRequest,
        **kwargs: Any,
    ) -> PhoneFeedbackResponse:
        """Submit phone feedback to Trestle.

        Args:
            feedback: The phone feedback data to submit.
            **kwargs: Additional arguments to pass to the underlying HTTP client.

        Returns:
            PhoneFeedbackResponse: The API response.

        Raises:
            PhoneFeedbackValidationError: If the request validation fails.
            PhoneFeedbackAuthenticationError: If authentication fails.
            PhoneFeedbackRateLimitError: If rate limit is exceeded.
            PhoneFeedbackAPIError: For other API errors.
        """
        url = f"{self._base_url}/phone_feedback"

        try:
            response = await self._client._request(
                "POST",
                url,
                json=feedback.model_dump(exclude_unset=True),
                **kwargs,
            )

            return PhoneFeedbackResponse.model_validate(response)

        except httpx.HTTPStatusError as e:
            if e.response is None:
                raise PhoneFeedbackAPIError("No response received from server") from e

            if e.response.status_code == 400:
                raise PhoneFeedbackValidationError(
                    f"Validation error: {e.response.text}",
                    status_code=400,
                    response=e.response,
                ) from e
            if e.response.status_code == 403:
                raise PhoneFeedbackAuthenticationError(
                    "Authentication failed. Please check your API key.",
                    status_code=403,
                    response=e.response,
                ) from e
            if e.response.status_code == 429:
                retry_after = int(e.response.headers.get("Retry-After", 60))
                raise PhoneFeedbackRateLimitError(
                    "Rate limit exceeded. Please try again later.",
                    status_code=429,
                    response=e.response,
                    retry_after=retry_after,
                ) from e

            raise PhoneFeedbackAPIError(
                f"API request failed with status {e.response.status_code}: {e.response.text}",
                status_code=e.response.status_code,
                response=e.response,
            ) from e

        except Exception as e:
            raise PhoneFeedbackAPIError(
                f"Failed to submit phone feedback: {e!s}"
            ) from e
