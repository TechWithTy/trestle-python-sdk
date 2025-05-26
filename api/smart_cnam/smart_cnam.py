"""Smart CNAM API client for Trestle integration."""

import logging
from typing import Any

import httpx
from tenacity import (
    before_sleep_log,
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from ...models.smart_cnam import SmartCNAMResponse
from ._requests import SmartCNAMRequest
from ._exceptions import (
    APIError,
    AuthenticationError,
    InvalidPhoneNumberError,
    RateLimitExceededError,
    ServerError,
    SmartCNAMAPIError,
    ValidationError,
)

logger = logging.getLogger(__name__)

# Configure retry settings
RETRY_STATUS_CODES = {429, 500, 502, 503, 504}
MAX_RETRIES = 3
MIN_RETRY_DELAY = 1  # seconds
MAX_RETRY_DELAY = 10  # seconds


def _should_retry_error(exception: Exception) -> bool:
    """Determine if the request should be retried based on the exception."""
    if isinstance(exception, (RateLimitExceededError, ServerError)):
        return True
    if isinstance(exception, APIError) and exception.status_code in RETRY_STATUS_CODES:
        return True
    if isinstance(exception, (httpx.RequestError, httpx.HTTPStatusError)):
        return True
    return False


class SmartCNAMAPI:
    """Client for the Trestle Smart CNAM API."""

    def __init__(self, client: httpx.AsyncClient, base_url: str, api_key: str) -> None:
        """Initialize the SmartCNAMAPI client.

        Args:
            client: HTTPX async client instance.
            base_url: Base URL for the Trestle API.
            api_key: Trestle API key.
        """
        self._client = client
        self._base_url = base_url.rstrip("/")
        self._api_key = api_key
        self._endpoint = f"{self._base_url}/3.1/cnam"

    @retry(
        stop=stop_after_attempt(MAX_RETRIES),
        wait=wait_exponential(
            multiplier=1, min=MIN_RETRY_DELAY, max=MAX_RETRY_DELAY
        ),
        retry=retry_if_exception_type(_should_retry_error),
        before_sleep=before_sleep_log(logger, logging.WARNING),
        reraise=True,
    )
    async def lookup_caller(
        self,
        phone: str,
        country_hint: str | None = None,
    ) -> SmartCNAMResponse:
        """Look up caller information by phone number using Smart CNAM.

        Args:
            phone: The phone number to look up (E.164 or local format).
            country_hint: ISO-3166 alpha-2 country code hint.

        Returns:
            SmartCNAMResponse with the caller information.

        Raises:
            InvalidPhoneNumberError: If the phone number is invalid.
            AuthenticationError: If authentication fails.
            RateLimitExceededError: If rate limit is exceeded.
            ServerError: If there's a server-side error.
            APIError: For other API errors.
            ValidationError: If request validation fails.
        """
        try:
            # Validate and prepare the request
            request_data = SmartCNAMRequest(
                phone=phone,
                country_hint=country_hint,
            )

            # Make the API request
            response = await self._client.get(
                self._endpoint,
                params=request_data.dict(exclude_none=True, by_alias=True),
                headers={"x-api-key": self._api_key},
                timeout=30.0,
            )

            # Handle error responses
            if response.status_code == 400:
                error_data = response.json()
                raise InvalidPhoneNumberError(
                    f"Invalid phone number: {error_data.get('message', 'Unknown error')}",
                    error_data,
                )
            if response.status_code == 401:
                raise AuthenticationError("Invalid API key")
            if response.status_code == 403:
                raise AuthenticationError("Forbidden - check API key permissions")
            if response.status_code == 429:
                retry_after = int(response.headers.get("Retry-After", "60"))
                raise RateLimitExceededError(retry_after=retry_after)
            if response.status_code >= 500:
                raise ServerError("Server error occurred")
            if not response.is_success:
                error_data = response.json()
                raise APIError(
                    f"API error: {error_data.get('message', 'Unknown error')}",
                    status_code=response.status_code,
                    details=error_data,
                )

            # Parse and return the successful response
            return SmartCNAMResponse(**response.json())

        except httpx.RequestError as e:
            logger.error(f"Request failed: {str(e)}")
            raise APIError(f"Request failed: {str(e)}", status_code=0) from e
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error: {str(e)}")
            raise APIError(
                f"HTTP error: {str(e)}",
                status_code=e.response.status_code if e.response else 0,
            ) from e
        except ValueError as e:
            logger.error(f"Invalid response data: {str(e)}")
            raise ValidationError(f"Invalid response data: {str(e)}") from e
