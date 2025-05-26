"""Pydantic models for Real Contact API responses."""

from typing import Any, Literal, Optional

from pydantic import BaseModel, Field, field_validator


class PhoneInfo(BaseModel):
    """Phone information from Real Contact API response."""
    is_valid: bool | None = Field(
        default=None,
        description="True if the phone number is valid.",
    )
    activity_score: int | None = Field(
        default=None,
        description="Trestle's activity scores range from 0 to 100.",
        ge=0,
        le=100,
    )
    line_type: Literal[
        "Landline",
        "Premium",
        "NonFixedVOIP",
        "Mobile",
        "FixedVOIP",
        "TollFree",
        "Other",
        "Voicemail",
    ] | None = Field(
        default=None,
        description="The line type of the phone number.",
    )
    name_match: bool | None = Field(
        default=None,
        description="A match/no match indicator for the name associated with the phone.",
    )
    contact_grade: Literal["A", "B", "C", "D", "F"] | None = Field(
        default=None,
        description="An A–F grade determining the quality of the lead's phone.",
    )


class EmailInfo(BaseModel):
    """Email information from Real Contact API response."""
    is_valid: bool | None = Field(
        default=None,
        description="True if the email is valid.",
    )
    name_match: bool | None = Field(
        default=None,
        description="A match/no match indicator for the name associated with the email.",
    )
    contact_grade: Literal["A", "B", "C", "D", "F"] | None = Field(
        default=None,
        description="An A–F grade determining the quality of the lead's email.",
    )
    deliverability: str | None = Field(
        default=None,
        description="Email deliverability status (if add-on enabled).",
    )
    age_score: int | None = Field(
        default=None,
        description="Email age score (if add-on enabled).",
        ge=0,
        le=100,
    )


class AddressInfo(BaseModel):
    """Address information from Real Contact API response."""
    is_valid: bool | None = Field(
        default=None,
        description="True if the address is valid.",
    )
    name_match: bool | None = Field(
        default=None,
        description="A match/no match indicator for the name associated with the address.",
    )


class LitigatorChecks(BaseModel):
    """Litigator checks information (if add-on enabled)."""
    is_litigator: bool | None = Field(
        default=None,
        description="True if the email is associated with known litigators.",
    )
    risk_score: int | None = Field(
        default=None,
        description="Risk score from 0-100 (if available).",
        ge=0,
        le=100,
    )


class AddOnsResponse(BaseModel):
    """Add-ons response data."""
    litigator_checks: LitigatorChecks | None = None
    email_checks: dict[str, Any] | None = None


class PartialError(BaseModel):
    """Partial error response model."""
    name: str | None = None
    message: str | None = None


class RealContactResponse(BaseModel):
    """Real Contact API response model."""
    phone: PhoneInfo
    email: EmailInfo
    address: AddressInfo
    add_ons: AddOnsResponse | None = None
    error: PartialError | None = None
    warnings: list[str] | None = None

    @classmethod
    @field_validator("warnings", mode="before")
    def validate_warnings(cls, v: Any) -> list[str] | None:
        """Convert single warning string to list if needed."""
        if v is None:
            return None
        if isinstance(v, str):
            return [v]
        if isinstance(v, list) and all(isinstance(item, str) for item in v):
            return v
        return None

    @classmethod
    def from_api_response(cls, data: dict[str, Any]) -> "RealContactResponse":
        """Create a RealContactResponse from the raw API response.
        
        This handles the flat structure of the API response and maps it to our nested model.
        """
        # Extract phone info
        phone = PhoneInfo(
            is_valid=data.get("phone.is_valid"),
            activity_score=data.get("phone.activity_score"),
            line_type=data.get("phone.line_type"),
            name_match=data.get("phone.name_match"),
            contact_grade=data.get("phone.contact_grade"),
        )
        
        # Extract email info
        email = EmailInfo(
            is_valid=data.get("email.is_valid"),
            name_match=data.get("email.name_match"),
            contact_grade=data.get("email.contact_grade"),
            deliverability=data.get("email.deliverability"),
            age_score=data.get("email.age_score"),
        )
        
        # Extract address info
        address = AddressInfo(
            is_valid=data.get("address.is_valid"),
            name_match=data.get("address.name_match"),
        )
        
        # Handle add-ons if present
        add_ons_data = data.get("add_ons", {})
        add_ons = None
        
        if add_ons_data:
            litigator_checks = None
            if "litigator_checks" in add_ons_data:
                litigator_checks = LitigatorChecks(
                    is_litigator=add_ons_data["litigator_checks"].get("is_litigator"),
                    risk_score=add_ons_data["litigator_checks"].get("risk_score"),
                )
            
            add_ons = AddOnsResponse(
                litigator_checks=litigator_checks,
                email_checks=add_ons_data.get("email_checks"),
            )
        
        # Handle error if present
        error_data = data.get("error")
        error = None
        if error_data:
            error = PartialError(
                name=error_data.get("name"),
                message=error_data.get("message"),
            )
        
        return cls(
            phone=phone,
            email=email,
            address=address,
            add_ons=add_ons,
            error=error,
            warnings=data.get("warnings"),
        )

    class Config:
        """Pydantic config."""
        json_encoders = {
            dict: lambda v: v if v is not None else {}
        }
        populate_by_name = True
