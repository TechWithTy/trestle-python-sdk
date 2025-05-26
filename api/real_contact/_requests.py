"""Request models for the Real Contact API."""

from enum import Enum
from typing import Any

from pydantic import BaseModel, Field, field_validator


class AddOns(str, Enum):
    """Available add-ons for the Real Contact API."""
    EMAIL_CHECKS_DELIVERABILITY = "email_checks_deliverability"
    EMAIL_CHECKS_AGE = "email_checks_age"
    LITIGATOR_CHECKS = "litigator_checks"


class AddressRequest(BaseModel):
    """Address request model for Real Contact API."""
    street_line_1: str | None = Field(
        default=None,
        max_length=1000,
        description="The first line of the street part in the structured address.",
        alias="address.street_line_1",
    )
    city: str | None = Field(
        default=None,
        max_length=500,
        description="The name of the city in the structured address.",
        alias="address.city",
    )
    state_code: str | None = Field(
        default=None,
        max_length=100,
        description="The state code of the structured address.",
        alias="address.state_code",
    )
    postal_code: str | None = Field(
        default=None,
        max_length=100,
        description="The postal code of the structured address.",
        alias="address.postal_code",
    )
    country_code: str | None = Field(
        default="US",
        max_length=2,
        min_length=2,
        description="The ISO-3166 alpha-2 country code of the address.",
        alias="address.country_code",
    )


class BusinessRequest(BaseModel):
    """Business request model for Real Contact API."""
    name: str | None = Field(
        default=None,
        description="The business name to search.",
        alias="business.name",
    )


class RealContactRequest(BaseModel):
    """Real Contact API request model."""
    name: str = Field(..., description="The name of the person to search.")
    phone: str = Field(..., description="The phone provided by the lead on the web form.")
    email: str | None = Field(
        default=None,
        description="The email provided by the lead on the web form.",
    )
    ip_address: str | None = Field(
        default=None,
        description="The IP address from which the lead signed up on the web form.",
        alias="ip_address",
    )
    address: AddressRequest | None = None
    business: BusinessRequest | None = None
    add_ons: list[AddOns] | None = Field(
        default=None,
        description="List of add-ons to enable for the request.",
    )

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v: str) -> str:
        """Validate and clean phone number."""
        # Remove all non-digit characters
        cleaned = "".join(c for c in v if c.isdigit())
        if not cleaned:
            raise ValueError("Phone number must contain at least one digit")
        return cleaned

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str | None) -> str | None:
        """Basic email validation."""
        if v is None:
            return None
        if "@" not in v or "." not in v.partition("@")[2]:
            raise ValueError("Invalid email format")
        return v.lower()

    @field_validator("ip_address")
    @classmethod
    def validate_ip_address(cls, v: str | None) -> str | None:
        """Basic IP address validation."""
        if v is None:
            return None
        parts = v.split(".")
        if len(parts) != 4:
            raise ValueError("Invalid IP address format (expected IPv4)")
        for part in parts:
            try:
                num = int(part)
                if not 0 <= num <= 255:
                    raise ValueError("IP octet out of range")
            except ValueError as e:
                raise ValueError("IP address must contain numbers") from e
        return v

    def model_dump(self, **kwargs) -> dict[str, Any]:
        """Override model_dump to handle nested models and aliases."""
        data = super().model_dump(
            by_alias=True,
            exclude_none=True,
            **kwargs,
        )
        
        # Handle nested address and business models
        if self.address:
            address_data = self.address.model_dump(by_alias=True, exclude_none=True)
            data.update(address_data)
            data.pop("address", None)
            
        if self.business:
            business_data = self.business.model_dump(by_alias=True, exclude_none=True)
            data.update(business_data)
            data.pop("business", None)
        
        # Convert add_ons to comma-separated string
        if "add_ons" in data and data["add_ons"] is not None:
            data["add_ons"] = ",".join(add_on.value for add_on in data["add_ons"])
            
        return data
