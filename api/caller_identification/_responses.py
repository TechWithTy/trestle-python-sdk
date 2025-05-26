"""Response models for the Caller Identification API."""

from __future__ import annotations

from enum import Enum
from typing import Any, Literal

from pydantic import BaseModel, Field, HttpUrl


class LineType(str, Enum):
    """Enumeration of possible phone line types."""
    LANDLINE = "Landline"
    PREMIUM = "Premium"
    NON_FIXED_VOIP = "NonFixedVOIP"
    MOBILE = "Mobile"
    FIXED_VOIP = "FixedVOIP"
    TOLL_FREE = "TollFree"
    OTHER = "Other"
    VOICEMAIL = "Voicemail"


class Address(BaseModel):
    """Address information."""
    street_line1: str | None = None
    street_line2: str | None = None
    city: str | None = None
    state_code: str | None = None
    postal_code: str | None = None
    country_code: str | None = None
    lat_long: dict[str, float] | None = None
    is_active: bool | None = None
    delivery_point: str | None = None
    link_to_person_start_date: str | None = None
    link_to_person_end_date: str | None = None


class PhoneOwnerPerson(BaseModel):
    """Model for a person associated with a phone number."""
    id: str | None = None
    name: str | None = None
    firstname: str | None = None
    middlename: str | None = None
    lastname: str | None = None
    alternate_names: list[str] | None = None
    age_range: str | None = None
    gender: str | None = None
    type: Literal["Person"] = "Person"
    link_to_phone_start_date: str | None = None
    industry: str | None = None


class PhoneOwnerBusiness(BaseModel):
    """Model for a business associated with a phone number."""
    id: str | None = None
    name: str | None = None
    alternate_names: list[str] | None = None
    description: str | None = None
    founded: int | None = None
    employee_count: str | None = None
    industry: str | None = None
    type: Literal["Business"] = "Business"
    link_to_phone_start_date: str | None = None


class PartialError(BaseModel):
    """Model for partial error responses."""
    name: str | None = None
    message: str | None = None


class CallerIDResponse(BaseModel):
    """Response model for the Caller Identification API."""
    id: str | None = Field(
        default=None,
        description="The persistent ID of the phone number.",
        example="Phone.3dbb6fef-a2df-4b08-cfe3-bc7128b6f5b4",
    )
    phone_number: str | None = Field(
        default=None,
        description="The phone number in E.164 or local format.",
        example="2069735100",
    )
    is_valid: bool | None = Field(
        default=None,
        description="True if the phone number is valid.",
        example=True,
    )
    country_calling_code: str | None = Field(
        default=None,
        description="The country code of the phone number.",
        example="1",
    )
    line_type: LineType | None = Field(
        default=None,
        description="The type of phone line.",
    )
    carrier: str | None = Field(
        default=None,
        description="The carrier providing service for the phone number.",
        example="Trestle Telco",
    )
    is_prepaid: bool | None = Field(
        default=None,
        description="True if the phone is associated with a prepaid account.",
        example=False,
    )
    is_commercial: bool | None = Field(
        default=None,
        description="True if the phone number is registered to a business.",
        example=False,
    )
    belongs_to: list[PhoneOwnerPerson | PhoneOwnerBusiness] | None = Field(
        default=None,
        description="The owner(s) associated with the phone.",
    )
    current_addresses: list[Address] | None = Field(
        default=None,
        description="Current addresses associated with the phone owner.",
    )
    emails: list[str] | None = Field(
        default=None,
        description="Email addresses associated with the phone owner.",
    )
    error: PartialError | None = Field(
        default=None,
        description="Partial error information if the request was not fully successful.",
    )
    warnings: list[str] | None = Field(
        default=None,
        description="Warnings returned as part of the response, if applicable.",
    )

    class Config:
        """Pydantic config."""
        json_encoders = {
            HttpUrl: lambda v: str(v) if v else None
        }
        schema_extra = {
            "example": {
                "id": "Phone.3dbb6fef-a2df-4b08-cfe3-bc7128b6f5b4",
                "phone_number": "2069735100",
                "is_valid": True,
                "country_calling_code": "1",
                "line_type": "NonFixedVOIP",
                "carrier": "Trestle Telco",
                "is_prepaid": False,
                "is_commercial": False,
                "belongs_to": [{
                    "id": "Person.fffdcf06-0929-4b5a-9921-ee49b101ca84",
                    "name": "John Doe",
                    "firstname": "John",
                    "lastname": "Doe",
                    "type": "Person"
                }],
                "current_addresses": [{
                    "street_line1": "123 Main St",
                    "city": "Seattle",
                    "state_code": "WA",
                    "postal_code": "98101",
                    "country_code": "US"
                }],
                "emails": ["john.doe@example.com"],
                "error": {
                    "name": "InternalError",
                    "message": "Could not retrieve entire response"
                },
                "warnings": ["Missing Input"]
            }
        }
