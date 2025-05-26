"""Request models for the Smart CNAM API."""

from pydantic import BaseModel, Field, HttpUrl


class SmartCNAMRequest(BaseModel):
    """Request model for the Smart CNAM API.
    
    Args:
        phone: The phone number in E.164 or local format.
        country_hint: ISO-3166 alpha-2 country code hint.
    """
    phone: str = Field(..., description="The phone number in E.164 or local format")
    country_hint: str | None = Field(
        default=None,
        alias="phone.country_hint",
        description="ISO-3166 alpha-2 country code hint"
    )

    class Config:
        """Pydantic config."""
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "phone": "2069735100",
                "phone.country_hint": "US"
            }
        }
