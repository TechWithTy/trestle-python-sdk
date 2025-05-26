"""Reverse Phone API client for Trestle integration."""

import logging
from datetime import datetime, timezone
from typing import Any, Dict, Optional, Union

import httpx
from tenacity import (
    before_sleep_log,
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from ...models.reverse_phone import ReversePhoneResponse
from ._exceptions import (
    APIError,
    AuthenticationError,
    InvalidPhoneNumberError,
    RateLimitExceededError,
    ReversePhoneAPIError,
    ServerError,
    ValidationError,
)
from ._requests import ReversePhoneRequest
from ._responses import ReversePhoneResponse as ResponseModel

logger = logging.getLogger(__name__)

# Default timeout for API requests (in seconds)
DEFAULT_TIMEOUT = 30.0

# Base URL for the Trestle API
BASE_URL = "https://api.trestleiq.com/3.2"


class ReversePhoneAPI:
    """Client for interacting with the Trestle Reverse Phone API.
    
    This client provides methods to look up phone number information using the Trestle API.
    It includes retry logic, error handling, and request/response validation.
    
    Args:
        api_key: Your Trestle API key
        base_url: Base URL for the Trestle API (defaults to production)
        timeout: Request timeout in seconds (default: 30.0)
        max_retries: Maximum number of retry attempts (default: 3)
    """
    
    def __init__(
        self,
        api_key: str,
        base_url: str = BASE_URL,
        timeout: float = DEFAULT_TIMEOUT,
        max_retries: int = 3,
    ):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.max_retries = max_retries
        
        # Configure the HTTP client with retry logic
        self._client = self._get_http_client()
    
    def _get_http_client(self) -> httpx.AsyncClient:
        """Create and configure the HTTP client with retry logic."""
        # Define which exceptions should trigger a retry
        retry_exceptions = (
            httpx.NetworkError,
            httpx.TimeoutException,
            httpx.HTTPStatusError,
            ServerError,
            RateLimitExceededError,
        )
        
        # Configure retry decorator
        retry_decorator = retry(
            stop=stop_after_attempt(self.max_retries),
            wait=wait_exponential(multiplier=1, min=4, max=10),
            retry=retry_if_exception_type(retry_exceptions),
            before_sleep=before_sleep_log(logger, logging.WARNING),
            reraise=True,
        )
        
        # Create client with retry logic
        transport = httpx.AsyncHTTPTransport(
            retries=self.max_retries,
            http2=True,
        )
        
        client = httpx.AsyncClient(
            base_url=self.base_url,
            timeout=self.timeout,
            transport=transport,
            headers={
                "x-api-key": self.api_key,
                "User-Agent": "LeadIgnite/1.0",
                "Accept": "application/json",
            },
        )
        
        # Apply retry decorator to the request method
        client.send = retry_decorator(client.send)
        
        return client
    
    async def close(self) -> None:
        """Close the HTTP client and release resources."""
        await self._client.aclose()
    
    async def __aenter__(self):
        """Support async context manager."""
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Ensure resources are cleaned up when exiting context."""
        await self.close()
    
    async def lookup_phone(
        self,
        phone: str,
        country_hint: Optional[str] = None,
        name_hint: Optional[str] = None,
        postal_code_hint: Optional[str] = None,
    ) -> ReversePhoneResponse:
        """Look up information about a phone number.
        
        Args:
            phone: The phone number to look up (E.164 or local format)
            country_hint: ISO-3166 alpha-2 country code hint
            name_hint: Name associated with the phone number
            postal_code_hint: Postal code of the subscriber address
            
        Returns:
            ReversePhoneResponse: The response from the API
            
        Raises:
            InvalidPhoneNumberError: If the phone number is invalid
            AuthenticationError: If authentication fails
            RateLimitExceededError: If rate limit is exceeded
            ServerError: If there's a server-side error
            APIError: For other API errors
            ValidationError: If request validation fails
        """
        # Validate request
        request_data = ReversePhoneRequest(
            phone=phone,
            country_hint=country_hint,
            name_hint=name_hint,
            postal_code_hint=postal_code_hint,
        )
        
        # Prepare query parameters
        params = {"phone": request_data.phone}
        if request_data.country_hint:
            params["phone.country_hint"] = request_data.country_hint
        if request_data.name_hint:
            params["phone.name_hint"] = request_data.name_hint
        if request_data.postal_code_hint:
            params["phone.postal_code_hint"] = request_data.postal_code_hint
        
        try:
            # Make the API request
            response = await self._client.get(
                "/phone",
                params=params,
                headers={"x-api-key": self.api_key},
            )
            
            # Handle different status codes
            if response.status_code == 200:
                return ResponseModel(**response.json())
            elif response.status_code == 400:
                raise InvalidPhoneNumberError("Invalid phone number")
            elif response.status_code == 401:
                raise AuthenticationError("Invalid API key")
            elif response.status_code == 403:
                error_data = response.json()
                raise AuthenticationError(
                    error_data.get("message", "Forbidden"),
                    details=error_data,
                )
            elif response.status_code == 429:
                retry_after = response.headers.get("Retry-After")
                raise RateLimitExceededError(
                    "Rate limit exceeded",
                    details={"retry_after": retry_after},
                )
            elif 500 <= response.status_code < 600:
                error_data = response.json()
                raise ServerError(
                    error_data.get("message", "Internal server error"),
                    details=error_data,
                )
            else:
                error_data = response.json()
                raise APIError(
                    error_data.get("message", f"Unexpected status code: {response.status_code}"),
                    status_code=response.status_code,
                    details=error_data,
                )
                
        except httpx.RequestError as e:
            logger.error(f"Request failed: {str(e)}")
            raise ReversePhoneAPIError(f"Request failed: {str(e)}") from e
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}", exc_info=True)
            raise ReversePhoneAPIError(f"Unexpected error: {str(e)}") from e
