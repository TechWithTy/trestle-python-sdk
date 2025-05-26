"""Pydantic models for Smart CNAM API responses."""

from typing import Any

from pydantic import BaseModel, Field, HttpUrl


class PartialError(BaseModel):
    """Model for partial error responses."""
    name: str | None = None
    message: str | None = None


class PhoneOwnerPersonSmartCNAM(BaseModel):
    """Model for a person associated with a phone number in Smart CNAM response."""
    id: str | None = Field(
        default=None,
        description="Unique identifier for the person"
    )
    name: str | None = Field(
        default=None,
        description="Full name of the person"
    )
    firstname: str | None = Field(
        default=None,
        description="First name of the person"
    )
    middlename: str | None = Field(
        default=None,
        description="Middle name or initial of the person"
    )
    lastname: str | None = Field(
        default=None,
        description="Last name of the person"
    )


class SmartCNAMResponse(BaseModel):
    """Response model for the Smart CNAM API."""
    id: str | None = Field(
        default=None,
        description="The persistent ID of the phone number",
        example="Phone.3dbb6fef-a2df-4b08-cfe3-bc7128b6f5b4"
    )
    is_valid: bool | None = Field(
        default=None,
        description="True if the phone number is valid"
    )
    belongs_to: PhoneOwnerPersonSmartCNAM | None = Field(
        default=None,
        description="The primary owner of the phone number"
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
                "is_valid": True,
                "belongs_to": {
                    "id": "Person.fffdcf06-0929-4b5a-9921-ee49b101ca84",
                    "name": "Waidong L Syrws",
                    "firstname": "Waidong",
                    "middlename": "L",
                    "lastname": "Syrws"
                },
                "error": {
                    "name": "InternalError",
                    "message": "Could not retrieve entire response"
                },
                "warnings": ["Missing Input"]
            }
        }
