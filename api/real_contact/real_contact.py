"""Real Contact API client for Trestle integration."""

import logging

import httpx
from tenacity import (
    before_sleep_log,
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from ...models.real_contact import RealContactResponse
from ._exceptions import (
    APIError,
    AuthenticationError,
    InvalidSearchCriteriaError,
    RateLimitExceededError,
    ServerError,
    ValidationError,
)
from ._requests import AddOns, RealContactRequest

logger = logging.getLogger(__name__)

# Configure retry settings
RETRY_STATUS_CODES = {429, 500, 502, 503, 504}
MAX_RETRIES = 3
MIN_RETRY_DELAY = 1  # seconds
MAX_RETRY_DELAY = 10  # seconds


def _should_retry_error(exception: Exception) -> bool:
    """Determine if the request should be retried based on the exception."""
    if isinstance(exception, RateLimitExceededError | ServerError):
        return True
    if isinstance(exception, APIError) and exception.status_code in RETRY_STATUS_CODES:
        return True
    if isinstance(exception, httpx.RequestError | httpx.HTTPStatusError):
        return True
    return False


class RealContactAPI:
    """Client for the Trestle Real Contact API."""

    def __init__(self, client: httpx.AsyncClient, base_url: str, api_key: str) -> None:
        """Initialize the RealContactAPI client.

        Args:
            client: HTTPX async client instance.
            base_url: Base URL for the Trestle API.
            api_key: Trestle API key.
        """
        self._client = client
        self._base_url = base_url.rstrip("/")
        self._api_key = api_key
        self._endpoint = f"{self._base_url}/1.1/real_contact"

    @retry(
        stop=stop_after_attempt(MAX_RETRIES),
        wait=wait_exponential(
            multiplier=1, min=MIN_RETRY_DELAY, max=MAX_RETRY_DELAY
        ),
        retry=retry_if_exception_type(_should_retry_error),
        before_sleep=before_sleep_log(logger, logging.WARNING),
        reraise=True,
    )
    async def verify_contact(
        self,
        name: str,
        phone: str,
        email: str | None = None,
        ip_address: str | None = None,
        street_line_1: str | None = None,
        city: str | None = None,
        postal_code: str | None = None,
        state_code: str | None = None,
        country_code: str = "US",
        business_name: str | None = None,
        enable_email_deliverability: bool = False,
        enable_email_age: bool = False,
        enable_litigator_checks: bool = False,
    ) -> RealContactResponse:
        """Verify contact information and get quality scores.

        Args:
            name: The name of the person to verify.
            phone: The phone number to verify.
            email: The email address to verify.
            ip_address: The IP address from which the lead signed up.
            street_line_1: First line of the street address.
            city: City name.
            postal_code: Postal/ZIP code.
            state_code: State/Province code.
            country_code: ISO-3166 alpha-2 country code (default: US).
            business_name: The business name (if applicable).
            enable_email_deliverability: Enable email deliverability checks.
            enable_email_age: Enable email age score.
            enable_litigator_checks: Enable litigator checks.

        Returns:
            RealContactResponse with verification results.

        Raises:
            InvalidSearchCriteriaError: If search criteria are insufficient.
            AuthenticationError: If authentication fails.
            RateLimitExceededError: If rate limit is exceeded.
            ServerError: If there's a server-side error.
            APIError: For other API errors.
            ValidationError: If request validation fails.
        """
        try:
            # Prepare add-ons
            add_ons = []
            if enable_email_deliverability:
                add_ons.append(AddOns.EMAIL_CHECKS_DELIVERABILITY)
            if enable_email_age:
                add_ons.append(AddOns.EMAIL_CHECKS_AGE)
            if enable_litigator_checks:
                add_ons.append(AddOns.LITIGATOR_CHECKS)

            # Create request model
            request_data = RealContactRequest(
                name=name,
                phone=phone,
                email=email,
                ip_address=ip_address,
                address={
                    "street_line_1": street_line_1,
                    "city": city,
                    "postal_code": postal_code,
                    "state_code": state_code,
                    "country_code": country_code,
                } if any([street_line_1, city, postal_code, state_code]) else None,
                business={"name": business_name} if business_name else None,
                add_ons=add_ons if add_ons else None,
            )

            # Make the API request
            response = await self._client.get(
                self._endpoint,
                params=request_data.model_dump(),
                headers={"x-api-key": self._api_key},
                timeout=30.0,
            )

            # Handle error responses
            response_data = response.json()

            if response.status_code == 400:
                raise InvalidSearchCriteriaError(
                    f"Invalid search criteria: {response_data.get('message', 'Insufficient or invalid parameters')}",
                    response_data,
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
                raise APIError(
                    f"API error: {response_data.get('message', 'Unknown error')}",
                    status_code=response.status_code,
                    details=response_data,
                )

            # Parse and return the successful response
            return RealContactResponse.from_api_response(response_data)

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
