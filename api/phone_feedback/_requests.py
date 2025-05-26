"""Request models for the Phone Feedback API."""
from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field, field_validator


class PhoneFeedbackRequest(BaseModel):
    """Request model for submitting phone feedback.

    Attributes:
        response_id: The response ID from the Trestle API.
        phone: The phone number in E.164 or local format.
        name: Person or business name associated with the phone number.
        phone_status: The status of the phone number from a live call.
        phone_right_party_contact: Whether the phone number belongs to the correct party.
    """

    response_id: str = Field(..., description="The response ID from the Trestle API.")
    phone: str = Field(..., description="The phone number in E.164 or local format.")
    name: str = Field(..., description="Person or business name associated with the phone number.")
    phone_status: Literal["Connected", "Disconnected"] = Field(
        ...,
        description="The status of the phone number from a live call.",
    )
    phone_right_party_contact: bool = Field(
        ...,
        description="Whether the phone number belongs to the correct party.",
    )

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v: str) -> str:
        """Validate phone number format."""
        # Remove all non-digit characters
        digits = "".join(filter(str.isdigit, v))
        if not digits:
            raise ValueError("Phone number must contain digits")
        return digits
