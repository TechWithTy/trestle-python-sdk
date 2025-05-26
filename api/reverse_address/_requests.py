"""Request models for the Reverse Address API."""

from pydantic import BaseModel, Field, HttpUrl


class ReverseAddressRequest(BaseModel):
    """Request model for the Reverse Address API.
    
    Args:
        street_line_1: First line of the street address
        street_line_2: Second line of the street address (optional)
        city: City name
        postal_code: Postal/ZIP code
        state_code: State/Province code
        country_code: ISO-3166 alpha-2 country code (default: US)
    """
    street_line_1: str = Field(
        ...,
        max_length=1000,
        description="First line of the street address"
    )
    street_line_2: str | None = Field(
        default=None,
        max_length=1000,
        description="Second line of the street address (optional)"
    )
    city: str = Field(
        ...,
        max_length=500,
        description="City name"
    )
    postal_code: str = Field(
        ...,
        max_length=100,
        description="Postal/ZIP code"
    )
    state_code: str = Field(
        ...,
        max_length=100,
        description="State/Province code"
    )
    country_code: str = Field(
        default="US",
        max_length=2,
        description="ISO-3166 alpha-2 country code"
    )

    class Config:
        """Pydantic config."""
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "street_line_1": "100 Syrws St",
                "street_line_2": "Ste 1",
                "city": "Lynden",
                "postal_code": "98264",
                "state_code": "WA",
                "country_code": "US"
            }
        }
