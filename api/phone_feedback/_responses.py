"""Response models for the Phone Feedback API."""
from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field


class PhoneFeedbackError(BaseModel):
    """Error details in case of partial success."""

    name: str = Field(..., description="The type of error that occurred.")
    message: str = Field(..., description="A human-readable error message.")


class PhoneFeedbackResponse(BaseModel):
    """Response model for phone feedback submission.

    Attributes:
        status: Whether the data was successfully received.
        error: Optional error details in case of partial success.
    """

    status: str = Field(..., description="Whether the data was successfully received.")
    error: PhoneFeedbackError | None = Field(
        None,
        description="Error details if the request encountered a partial error.",
    )
