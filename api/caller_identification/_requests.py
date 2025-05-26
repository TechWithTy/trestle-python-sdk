"""Request models for the Caller Identification API."""

from pydantic import BaseModel, Field, HttpUrl


class CallerIDRequest(BaseModel):
    """Request model for the Caller Identification API."""
    
    phone: str = Field(
        ...,
        description="The phone number in E.164 or local format.",
        example="2069735100",
    )
    country_hint: str | None = Field(
        default=None,
        description="ISO-3166 alpha-2 country code hint.",
        example="US",
        alias="phone.country_hint",
    )
    name_hint: str | None = Field(
        default=None,
        description="Name associated with the phone number.",
        alias="phone.name_hint",
    )
    postal_code_hint: str | None = Field(
        default=None,
        description="Postal code of the subscriber address.",
        alias="phone.postal_code_hint",
    )

    class Config:
        """Pydantic config."""
        populate_by_name = True
        allow_population_by_field_name = True
