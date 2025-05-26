"""Trestle API client for Lead Ignite backend.

This module provides a client for interacting with the Trestle API, including
services like Reverse Phone Lookup and Caller Identification. The client handles
authentication, request retries, and error handling.
"""
from __future__ import annotations

import logging
from contextlib import asynccontextmanager

import httpx
from pydantic import ConfigDict, Field, field_validator
from pydantic_settings import BaseSettings

from .api.caller_identification import CallerIDAPI
from .api.find_person import FindPersonAPI
from .api.phone_feedback import PhoneFeedbackAPI
from .api.phone_validation import PhoneValidationAPI
from .api.real_contact import RealContactAPI
from .api.reverse_address import ReverseAddressAPI
from .api.reverse_phone import ReversePhoneAPI
from .api.smart_cnam import SmartCNAMAPI


class TrestleConfig(BaseSettings):
    """Configuration for the Trestle API client."""

    api_key: str = Field(..., env="TRESTLE_API_KEY")
    base_url: str = Field("https://api.trestleiq.com", env="TRESTLE_BASE_URL")
    timeout: int = Field(30, env="TRESTLE_TIMEOUT")
    max_retries: int = Field(3, env="TRESTLE_MAX_RETRIES")

    model_config = ConfigDict(extra="allow")

    @field_validator("base_url")
    def validate_base_url(cls, v: str) -> str:
        """Ensure base URL ends with a slash."""
        return v.rstrip("/") + "/"


class TrestleAPIClient:
    """Async client for interacting with the Trestle API.

    This client provides an interface to the Trestle API with built-in
    retry logic, error handling, and request/response validation.

    Example:
        ```python
        async with TrestleAPIClient() as client:
            # Use the client
            response = await client._request("GET", "some/endpoint")
        ```
    """

    def __init__(
        self,
        config: TrestleConfig | None = None,
        api_key: str | None = None,
        base_url: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> None:
        """Initialize the Trestle API client.

        Args:
            config: Optional configuration. If not provided, will be loaded from environment.
            api_key: Optional API key. Overrides config if provided.
            base_url: Optional base URL. Overrides config if provided.
            timeout: Optional timeout in seconds. Overrides config if provided.
            max_retries: Optional max retries. Overrides config if provided.
        """
        self._config = config or TrestleConfig()
        self._client: httpx.AsyncClient | None = None
        self._logger = logging.getLogger(__name__)

        # Override config with explicit parameters if provided
        if api_key:
            self._config.api_key = api_key
        if base_url:
            self._config.base_url = base_url
        if timeout is not None:
            self._config.timeout = timeout
        if max_retries is not None:
            self._config.max_retries = max_retries

        # Initialize API clients
        self._reverse_phone: ReversePhoneAPI | None = None
        self._caller_id: CallerIDAPI | None = None
        self._smart_cnam: SmartCNAMAPI | None = None
        self._phone_validation: PhoneValidationAPI | None = None
        self._reverse_address: ReverseAddressAPI | None = None
        self._find_person: FindPersonAPI | None = None
        self._real_contact: RealContactAPI | None = None
        self._phone_feedback: PhoneFeedbackAPI | None = None
    
    @property
    def reverse_phone(self) -> ReversePhoneAPI:
        """Access the Reverse Phone API."""
        if self._reverse_phone is None:
            self._reverse_phone = ReversePhoneAPI(
                self._client,
                self._config.base_url,
                self._config.api_key,
            )
        return self._reverse_phone

    @property
    def caller_id(self) -> CallerIDAPI:
        """Access the Caller Identification API."""
        if self._caller_id is None:
            self._caller_id = CallerIDAPI(
                self._client,
                self._config.base_url,
                self._config.api_key,
            )
        return self._caller_id
        
    @property
    def smart_cnam(self) -> SmartCNAMAPI:
        """Access the Smart CNAM API."""
        if self._smart_cnam is None:
            self._smart_cnam = SmartCNAMAPI(
                self._client,
                self._config.base_url,
                self._config.api_key,
            )
        return self._smart_cnam
        
    @property
    def phone_validation(self) -> PhoneValidationAPI:
        """Access the Phone Validation API."""
        if self._phone_validation is None:
            self._phone_validation = PhoneValidationAPI(
                client=self._client,
                base_url=self._config.base_url,
                api_key=self._config.api_key,
            )
        return self._phone_validation
        
    @property
    def reverse_address(self) -> ReverseAddressAPI:
        """Access the Reverse Address API.
        
        Example:
            ```python
            async with TrestleAPIClient() as client:
                result = await client.reverse_address.lookup_address(
                    street_line_1="100 Syrws St",
                    city="Lynden",
                    postal_code="98264",
                    state_code="WA"
                )
                print(result.street_line_1, result.city, result.state_code)
            ```
        """
        if self._reverse_address is None:
            self._reverse_address = ReverseAddressAPI(
                client=self._client,
                base_url=self._config.base_url,
                api_key=self._config.api_key,
            )
        return self._reverse_address
        
    @property
    def find_person(self) -> FindPersonAPI:
        """Access the Find Person API.
        
        Example:
            ```python
            async with TrestleAPIClient() as client:
                result = await client.find_person.find_person(
                    name="John Smith",
                    city="Seattle",
                    state_code="WA"
                )
                for person in result.person or []:
                    print(f"Found: {person.full_name}")
            ```
        """
        if self._find_person is None:
            self._find_person = FindPersonAPI(
                client=self._client,
                base_url=self._config.base_url,
                api_key=self._config.api_key,
            )
        return self._find_person
        
    @property
    def real_contact(self) -> RealContactAPI:
        """Access the Real Contact API for contact verification.
        
        Example:
            ```python
            async with TrestleAPIClient() as client:
                result = await client.real_contact.verify_contact(
                    name="John Smith",
                    phone="+14259853735",
                    email="john.smith@example.com",
                    street_line_1="100 Syrws St",
                    city="Lynden",
                    state_code="WA",
                    postal_code="98264",
                    enable_email_deliverability=True
                )
                print(f"Phone grade: {result.phone.contact_grade}")
                print(f"Email grade: {result.email.contact_grade}")
                print(f"Address valid: {result.address.is_valid}")
            ```
        """
        if self._real_contact is None:
            self._real_contact = RealContactAPI(self)
        return self._real_contact
        
    @property
    def phone_feedback(self) -> PhoneFeedbackAPI:
        """Access the Phone Feedback API for submitting call feedback.
        
        Example:
            ```python
            from trestle.api.phone_feedback import PhoneFeedbackRequest
            
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
        if self._phone_feedback is None:
            self._phone_feedback = PhoneFeedbackAPI(self)
        return self._phone_feedback
    
    async def __aenter__(self):
        """Support async context manager."""
        self._client = httpx.AsyncClient(base_url=self._config.base_url, timeout=self._config.timeout)
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Clean up resources when exiting the context."""
        await self.close()
    
    async def close(self) -> None:
        """Close the client and release resources."""
        if self._client:
            await self._client.aclose()
            self._client = None
        if self._reverse_phone:
            await self._reverse_phone.close()
            self._reverse_phone = None
    
    async def is_healthy(self) -> bool:
        """Check if the Trestle API is healthy.
        
        Returns:
            bool: True if the API is healthy, False otherwise.
        """
        try:
            # Try a simple request to check if the API is responding
            async with httpx.AsyncClient(base_url=self._config.base_url) as client:
                response = await client.get(
                    "/health",
                    headers={"x-api-key": self._config.api_key},
                    timeout=5.0,
                )
                return response.status_code == 200
        except Exception:
            return False


@asynccontextmanager
async def get_trestle_client(
    api_key: str | None = None,
    base_url: str | None = None,
    timeout: float | None = None,
    max_retries: int | None = None,
) -> TrestleAPIClient:
    """Async context manager for getting a Trestle API client.
    
    Example:
        ```python
        async with get_trestle_client() as client:
            result = await client.reverse_phone.lookup_phone("2069735100")
        ```
    
    Args:
        api_key: Your Trestle API key. If not provided, will be loaded from
                environment variables or .env file.
        base_url: Base URL for the Trestle API. Defaults to production.
        timeout: Request timeout in seconds. Defaults to 30.0.
        max_retries: Maximum number of retry attempts. Defaults to 3.
        
    Yields:
        TrestleAPIClient: An initialized Trestle API client.
    """
    client = TrestleAPIClient(
        api_key=api_key,
        base_url=base_url,
        timeout=timeout,
        max_retries=max_retries,
    )
    try:
        yield client
    finally:
        await client.close()


# For backward compatibility
__all__ = [
    "TrestleAPIClient",
    "TrestleConfig",
    "get_trestle_client",
    # API clients
    "CallerIDAPI",
    "FindPersonAPI",
    "PhoneValidationAPI",
    "RealContactAPI",
    "ReverseAddressAPI",
    "ReversePhoneAPI",
    "SmartCNAMAPI",
    "PhoneFeedbackAPI",
]