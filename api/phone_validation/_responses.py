"""Response models for the Phone Validation API."""

from typing import Any

from pydantic import BaseModel, Field


class PartialError(BaseModel):
    """Model for partial error responses."""
    name: str | None = None
    message: str | None = None


class LitigatorChecks(BaseModel):
    """Model for litigator checks add-on data."""
    # Add specific litigator check fields as needed
    pass


class AddOnsData(BaseModel):
    """Model for add-ons data in the response."""
    litigator_checks: dict[str, Any] | None = None


class PhoneValidationResponse(BaseModel):
    """Response model for the Phone Validation API."""
    id: str | None = Field(
        default=None,
        description="The persistent ID of the phone number"
    )
    phone_number: str | None = Field(
        default=None,
        description="The phone number in E.164 or local format"
    )
    is_valid: bool | None = Field(
        default=None,
        description="True if the phone number is valid"
    )
    activity_score: int | None = Field(
        default=None,
        description="Activity score from 0-100 indicating phone activity level"
    )
    country_calling_code: str | None = Field(
        default=None,
        description="The country code of the phone number"
    )
    country_code: str | None = Field(
        default=None,
        description="ISO-3166 alpha-2 country code"
    )
    country_name: str | None = Field(
        default=None,
        description="The country name"
    )
    line_type: str | None = Field(
        default=None,
        description="Type of phone line (Landline, Mobile, VOIP, etc.)"
    )
    carrier: str | None = Field(
        default=None,
        description="The carrier/provider of the phone number"
    )
    is_prepaid: bool | None = Field(
        default=None,
        description="True if the phone is associated with a prepaid account"
    )
    add_ons: AddOnsData | None = Field(
        default=None,
        description="Additional data from enabled add-ons"
    )
    error: PartialError | None = Field(
        default=None,
        description="Error information if the request was not fully successful"
    )
    warnings: list[str] | str | None = Field(
        default=None,
        description="Warnings returned as part of the response, if applicable"
    )

    class Config:
        """Pydantic config."""
        json_encoders = {
            dict: lambda v: v if v is not None else {}
        }
        schema_extra = {
            "example": {
                "id": "Phone.3dbb6fef-a2df-4b08-cfe3-bc7128b6f5b4",
                "phone_number": "2069735100",
                "is_valid": True,
                "activity_score": 57,
                "country_calling_code": "1",
                "country_code": "US",
                "country_name": "United States",
                "line_type": "NonFixedVOIP",
                "carrier": "Level 3 Communications, LLC",
                "is_prepaid": False,
                "add_ons": {
                    "litigator_checks": {}
                },
                "error": {
                    "name": "InternalError",
                    "message": "Could not retrieve entire response"
                },
                "warnings": ["Missing Input"]
            }
        }
