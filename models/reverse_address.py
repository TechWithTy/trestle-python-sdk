"""Pydantic models for Reverse Address API responses."""

from typing import Any, Literal

from pydantic import BaseModel, Field


class Coordinates(BaseModel):
    """Geographical coordinates with accuracy information."""
    latitude: float | None = Field(
        default=None,
        description="Latitude coordinate"
    )
    longitude: float | None = Field(
        default=None,
        description="Longitude coordinate"
    )
    accuracy: str | None = Field(
        default=None,
        description="Accuracy level of the coordinates"
    )


class ResidentPerson(BaseModel):
    """Model for a person resident at an address."""
    id: str | None = Field(
        default=None,
        description="Unique identifier for the person"
    )
    name: str | None = Field(
        default=None,
        description="Full name of the person"
    )
    first_name: str | None = Field(
        default=None,
        description="First name of the person"
    )
    middle_name: str | None = Field(
        default=None,
        description="Middle name of the person"
    )
    last_name: str | None = Field(
        default=None,
        description="Last name of the person"
    )
    age: int | None = Field(
        default=None,
        description="Age of the person"
    )
    gender: str | None = Field(
        default=None,
        description="Gender of the person"
    )


class ResidentBusiness(BaseModel):
    """Model for a business resident at an address."""
    id: str | None = Field(
        default=None,
        description="Unique identifier for the business"
    )
    name: str | None = Field(
        default=None,
        description="Name of the business"
    )
    industry: str | None = Field(
        default=None,
        description="Industry of the business"
    )
    phone: str | None = Field(
        default=None,
        description="Phone number of the business"
    )
    website: str | None = Field(
        default=None,
        description="Website URL of the business"
    )


class PartialError(BaseModel):
    """Model for partial error responses."""
    name: str | None = None
    message: str | None = None


class ReverseAddressResponse(BaseModel):
    """Response model for the Reverse Address API."""
    id: str | None = Field(
        default=None,
        description="The persistent ID of the address"
    )
    is_valid: bool | None = Field(
        default=None,
        description="True if the address is valid"
    )
    street_line_1: str | None = Field(
        default=None,
        description="First line of the street address"
    )
    street_line_2: str | None = Field(
        default=None,
        description="Second line of the street address"
    )
    city: str | None = Field(
        default=None,
        description="City name"
    )
    postal_code: str | None = Field(
        default=None,
        description="Postal/ZIP code"
    )
    zip4: str | None = Field(
        default=None,
        description="ZIP+4 code (US only)",
        pattern=r"^\d+-\d{4}$"
    )
    state_code: str | None = Field(
        default=None,
        description="State/Province code"
    )
    country_code: str | None = Field(
        default=None,
        description="ISO-3166 alpha-2 country code"
    )
    lat_long: Coordinates | None = Field(
        default=None,
        description="Geographical coordinates of the address"
    )
    is_active: bool | None = Field(
        default=None,
        description="True if the address is currently receiving mail"
    )
    is_commercial: bool | None = Field(
        default=None,
        description="True if the address is a business address"
    )
    delivery_point: Literal["SingleUnit", "MultiUnit", "POBox", "PartialAddress"] | None = Field(
        default=None,
        description="Type of delivery point"
    )
    current_residents: list[ResidentPerson | ResidentBusiness] | None = Field(
        default=None,
        description="Current residents at the address"
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
                "id": "Location.d1a40ed5-a70a-46f8-80a9-bb4ac27e3a01",
                "is_valid": True,
                "street_line_1": "100 Syrws St",
                "street_line_2": "Ste 1",
                "city": "Lynden",
                "postal_code": "98264",
                "zip4": "98264-9999",
                "state_code": "WA",
                "country_code": "US",
                "lat_long": {
                    "latitude": 0,
                    "longitude": 0,
                    "accuracy": "Neighborhood"
                },
                "is_active": True,
                "is_commercial": True,
                "delivery_point": "SingleUnit",
                "current_residents": [{}],
                "error": {
                    "name": "InternalError",
                    "message": "Could not retrieve entire response"
                },
                "warnings": ["Missing Input"]
            }
        }
