from __future__ import annotations

from enum import Enum
from typing import Any

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


class PartialError(BaseModel):
    """Model for partial error responses."""
    name: str | None = None
    message: str | None = None


class ReversePhoneOwnerPerson(BaseModel):
    """Model for a person associated with a phone number."""
    id: str | None = None
    name: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    middle_name: str | None = None
    age_range: str | None = None
    gender: str | None = None
    link: HttpUrl | None = None
    location: dict[str, Any] | None = None
    address: dict[str, Any] | None = None
    phones: list[dict[str, Any]] | None = None
    emails: list[dict[str, Any]] | None = None
    relatives: list[dict[str, Any]] | None = None
    associates: list[dict[str, Any]] | None = None
    education: list[dict[str, Any]] | None = None
    employment: list[dict[str, Any]] | None = None
    profiles: dict[str, Any] | None = None


class ReversePhoneOwnerBusiness(BaseModel):
    """Model for a business associated with a phone number."""
    id: str | None = None
    name: str | None = None
    alt_names: list[str] | None = None
    description: str | None = None
    founded: int | None = None
    employee_count: str | None = None
    industry: str | None = None
    link: HttpUrl | None = None
    location: dict[str, Any] | None = None
    address: dict[str, Any] | None = None
    phones: list[dict[str, Any]] | None = None
    emails: list[dict[str, Any]] | None = None
    categories: list[str] | None = None
    profiles: dict[str, Any] | None = None


class ReversePhoneResponse(BaseModel):
    """Response model for the Reverse Phone API."""
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
    owners: list[ReversePhoneOwnerPerson | ReversePhoneOwnerBusiness] | None = Field(
        default=None,
        description="The owner(s) associated with the phone.",
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
                "owners": [],
                "error": {
                    "name": "InternalError",
                    "message": "Could not retrieve entire response"
                },
                "warnings": ["Missing Input"]
            }
        }
