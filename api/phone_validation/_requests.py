"""Request models for the Phone Validation API."""

from pydantic import BaseModel, Field


class PhoneValidationRequest(BaseModel):
    """Request model for the Phone Validation API.
    
    Args:
        phone: The phone number in E.164 or local format.
        country_hint: ISO-3166 alpha-2 country code hint.
        add_ons: Optional add-ons like 'litigator_checks'.
    """
    phone: str = Field(..., description="The phone number in E.164 or local format")
    country_hint: str | None = Field(
        default=None,
        alias="phone.country_hint",
        description="ISO-3166 alpha-2 country code hint"
    )
    add_ons: str | None = Field(
        default=None,
        description="Optional add-ons like 'litigator_checks'"
    )

    class Config:
        """Pydantic config."""
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "phone": "2069735100",
                "phone.country_hint": "US",
                "add_ons": "litigator_checks"
            }
        }
