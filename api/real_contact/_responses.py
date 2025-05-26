"""Response models for the Real Contact API."""

from typing import Any, Literal

from pydantic import BaseModel, Field, field_validator


class PhoneInfo(BaseModel):
    """Phone information from Real Contact API response."""
    is_valid: bool | None = Field(
        default=None,
        alias="phone.is_valid",
        description="True if the phone number is valid.",
    )
    activity_score: int | None = Field(
        default=None,
        alias="phone.activity_score",
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
        alias="phone.line_type",
        description="The line type of the phone number.",
    )
    name_match: bool | None = Field(
        default=None,
        alias="phone.name_match",
        description="A match/no match indicator for the name associated with the phone.",
    )
    contact_grade: Literal["A", "B", "C", "D", "F"] | None = Field(
        default=None,
        alias="phone.contact_grade",
        description="An A–F grade determining the quality of the lead's phone.",
    )


class EmailInfo(BaseModel):
    """Email information from Real Contact API response."""
    is_valid: bool | None = Field(
        default=None,
        alias="email.is_valid",
        description="True if the email is valid.",
    )
    name_match: bool | None = Field(
        default=None,
        alias="email.name_match",
        description="A match/no match indicator for the name associated with the email.",
    )
    contact_grade: Literal["A", "B", "C", "D", "F"] | None = Field(
        default=None,
        alias="email.contact_grade",
        description="An A–F grade determining the quality of the lead's email.",
    )
    deliverability: str | None = Field(
        default=None,
        alias="email.deliverability",
        description="Email deliverability status (if add-on enabled).",
    )
    age_score: int | None = Field(
        default=None,
        alias="email.age_score",
        description="Email age score (if add-on enabled).",
        ge=0,
        le=100,
    )


class AddressInfo(BaseModel):
    """Address information from Real Contact API response."""
    is_valid: bool | None = Field(
        default=None,
        alias="address.is_valid",
        description="True if the address is valid.",
    )
    name_match: bool | None = Field(
        default=None,
        alias="address.name_match",
        description="A match/no match indicator for the name associated with the address.",
    )


class LitigatorChecks(BaseModel):
    """Litigator checks information (if add-on enabled)."""
    is_litigator: bool | None = Field(
        default=None,
        alias="litigator_checks.is_litigator",
        description="True if the email is associated with known litigators.",
    )
    risk_score: int | None = Field(
        default=None,
        alias="litigator_checks.risk_score",
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
        # Extract base fields
        phone = {
            "phone.is_valid": data.get("phone.is_valid"),
            "phone.activity_score": data.get("phone.activity_score"),
            "phone.line_type": data.get("phone.line_type"),
            "phone.name_match": data.get("phone.name_match"),
            "phone.contact_grade": data.get("phone.contact_grade"),
        }

        email = {
            "email.is_valid": data.get("email.is_valid"),
            "email.name_match": data.get("email.name_match"),
            "email.contact_grade": data.get("email.contact_grade"),
            "email.deliverability": data.get("email.deliverability"),
            "email.age_score": data.get("email.age_score"),
        }
        
        address = {
            "address.is_valid": data.get("address.is_valid"),
            "address.name_match": data.get("address.name_match"),
        }
        
        # Handle add-ons if present
        add_ons = data.get("add_ons", {})
        litigator_checks = {
            "litigator_checks.is_litigator": add_ons.get("litigator_checks", {}).get("is_litigator"),
            "litigator_checks.risk_score": add_ons.get("litigator_checks", {}).get("risk_score"),
        } if add_ons and "litigator_checks" in add_ons else None
        
        return cls(
            phone=PhoneInfo.model_validate(phone),
            email=EmailInfo.model_validate(email),
            address=AddressInfo.model_validate(address),
            add_ons=AddOnsResponse(
                litigator_checks=LitigatorChecks.model_validate(litigator_checks) if litigator_checks else None,
                email_checks=add_ons.get("email_checks"),
            ) if add_ons else None,
            error=PartialError(**data["error"]) if "error" in data and data["error"] else None,
            warnings=data.get("warnings"),
        )

    class Config:
        """Pydantic config."""
        json_encoders = {
            dict: lambda v: v if v is not None else {}
        }
        populate_by_name = True
