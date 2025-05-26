"""Request models for the Find Person API."""

from pydantic import BaseModel, Field, HttpUrl


class AddressSearch(BaseModel):
    """Address search parameters for finding a person."""
    street_line_1: str | None = Field(
        default=None,
        max_length=1000,
        alias="address.street_line_1",
        description="First line of the street address"
    )
    street_line_2: str | None = Field(
        default=None,
        max_length=1000,
        alias="address.street_line_2",
        description="Second line of the street address (optional)"
    )
    city: str | None = Field(
        default=None,
        max_length=500,
        alias="address.city",
        description="City name"
    )
    postal_code: str | None = Field(
        default=None,
        max_length=100,
        alias="address.postal_code",
        description="Postal/ZIP code"
    )
    state_code: str | None = Field(
        default=None,
        max_length=100,
        alias="address.state_code",
        description="State/Province code"
    )
    country_code: str | None = Field(
        default="US",
        max_length=2,
        alias="address.country_code",
        description="ISO-3166 alpha-2 country code"
    )


class FindPersonRequest(AddressSearch):
    """Request model for the Find Person API.
    
    Args:
        name: Name of the person to search for
        address: Address search parameters (optional)
    """
    name: str = Field(
        ...,
        description="Name of the person to search for"
    )

    class Config:
        """Pydantic config."""
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "name": "John Smith",
                "address.street_line_1": "100 Syrws St",
                "address.street_line_2": "Ste 1",
                "address.city": "Lynden",
                "address.postal_code": "98264",
                "address.state_code": "WA",
                "address.country_code": "US"
            }
        }
