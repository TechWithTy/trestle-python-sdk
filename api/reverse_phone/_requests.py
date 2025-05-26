"""Request models for the Reverse Phone API."""

from typing import Optional
from pydantic import BaseModel, Field, HttpUrl


class ReversePhoneRequest(BaseModel):
    """Request model for reverse phone lookup.
    
    Args:
        phone: The phone number in E.164 or local format.
        country_hint: ISO-3166 alpha-2 country code hint.
        name_hint: Name associated with the phone number.
        postal_code_hint: Postal code of the subscriber address.
    """
    phone: str = Field(..., description="The phone number in E.164 or local format.")
    country_hint: Optional[str] = Field(
        None, 
        description="ISO-3166 alpha-2 country code hint.",
        alias="phone.country_hint"
    )
    name_hint: Optional[str] = Field(
        None,
        description="Name associated with the phone number.",
        alias="phone.name_hint"
    )
    postal_code_hint: Optional[str] = Field(
        None,
        description="Postal code of the subscriber address.",
        alias="phone.postal_code_hint"
    )

    class Config:
        allow_population_by_field_name = True
        json_encoders = {
            HttpUrl: lambda v: str(v) if v else None
        }
