"""Pydantic models for Find Person API responses."""

from typing import Any, Literal

from pydantic import BaseModel, Field


class Address(BaseModel):
    """Address information for a person."""
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
    state_code: str | None = Field(
        default=None,
        description="State/Province code"
    )
    country_code: str | None = Field(
        default=None,
        description="ISO-3166 alpha-2 country code"
    )
    is_current: bool | None = Field(
        default=None,
        description="Whether this is the current address"
    )
    start_date: str | None = Field(
        default=None,
        description="Start date of residence (YYYY-MM-DD)"
    )
    end_date: str | None = Field(
        default=None,
        description="End date of residence (YYYY-MM-DD) if not current"
    )


class PhoneNumber(BaseModel):
    """Phone number information for a person."""
    number: str | None = Field(
        default=None,
        description="Phone number in E.164 format"
    )
    type: Literal["home", "work", "mobile", "fax", "other"] | None = Field(
        default=None,
        description="Type of phone number"
    )
    is_current: bool | None = Field(
        default=None,
        description="Whether this is a current phone number"
    )


class EmailAddress(BaseModel):
    """Email address information for a person."""
    address: str | None = Field(
        default=None,
        description="Email address"
    )
    type: Literal["personal", "work", "other"] | None = Field(
        default=None,
        description="Type of email address"
    )
    is_current: bool | None = Field(
        default=None,
        description="Whether this is a current email address"
    )


class Person(BaseModel):
    """Information about a found person."""
    id: str | None = Field(
        default=None,
        description="Unique identifier for the person"
    )
    first_name: str | None = Field(
        default=None,
        description="First name"
    )
    middle_name: str | None = Field(
        default=None,
        description="Middle name"
    )
    last_name: str | None = Field(
        default=None,
        description="Last name"
    )
    full_name: str | None = Field(
        default=None,
        description="Full name"
    )
    age: int | None = Field(
        default=None,
        description="Age in years"
    )
    date_of_birth: str | None = Field(
        default=None,
        description="Date of birth (YYYY-MM-DD)"
    )
    gender: Literal["male", "female", "other"] | None = Field(
        default=None,
        description="Gender"
    )
    addresses: list[Address] | None = Field(
        default=None,
        description="List of known addresses"
    )
    phone_numbers: list[PhoneNumber] | None = Field(
        default=None,
        description="List of known phone numbers"
    )
    email_addresses: list[EmailAddress] | None = Field(
        default=None,
        description="List of known email addresses"
    )
    linkedin_url: str | None = Field(
        default=None,
        description="LinkedIn profile URL if available"
    )
    facebook_url: str | None = Field(
        default=None,
        description="Facebook profile URL if available"
    )
    twitter_handle: str | None = Field(
        default=None,
        description="Twitter handle if available"
    )


class PartialError(BaseModel):
    """Model for partial error responses."""
    name: str | None = None
    message: str | None = None


class FindPersonResponse(BaseModel):
    """Response model for the Find Person API."""
    count_person: int = Field(
        default=0,
        description="Number of people found"
    )
    person: list[Person] | None = Field(
        default=None,
        description="List of matching people"
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
                "count_person": 1,
                "person": [
                    {
                        "id": "person_123",
                        "first_name": "John",
                        "last_name": "Smith",
                        "full_name": "John Smith",
                        "age": 42,
                        "addresses": [
                            {
                                "street_line_1": "100 Syrws St",
                                "street_line_2": "Ste 1",
                                "city": "Lynden",
                                "postal_code": "98264",
                                "state_code": "WA",
                                "country_code": "US",
                                "is_current": True
                            }
                        ],
                        "phone_numbers": [
                            {
                                "number": "+12065551234",
                                "type": "mobile",
                                "is_current": True
                            }
                        ],
                        "email_addresses": [
                            {
                                "address": "john.smith@example.com",
                                "type": "personal",
                                "is_current": True
                            }
                        ]
                    }
                ],
                "error": {
                    "name": "InternalError",
                    "message": "Could not retrieve entire response"
                },
                "warnings": ["Missing Input"]
            }
        }
