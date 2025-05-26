"""Response models for the Reverse Phone API."""

from typing import Optional, List, Dict, Any, Union
from enum import Enum
from pydantic import BaseModel, Field, HttpUrl


class LineType(str, Enum):
    """Enumeration of possible phone line types."""
    LANDLINE = "Landline"
    PREMIUM = "Premium"
    NON_FIXED_VOIP = "NonFixedVOIP"
    MOBILE = "Mobile"
    FIXED_VOIP = "FixedVOIP"
    TOLL_FREE = "TollFree"
    OTHER = "Other"
    VOICEMAIL = "Voicemail"


class PartialError(BaseModel):
    """Model for partial error responses."""
    name: Optional[str] = None
    message: Optional[str] = None


class ReversePhoneOwnerPerson(BaseModel):
    """Model for a person associated with a phone number."""
    id: Optional[str] = None
    name: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    middle_name: Optional[str] = None
    age_range: Optional[str] = None
    gender: Optional[str] = None
    link: Optional[HttpUrl] = None
    location: Optional[Dict[str, Any]] = None
    address: Optional[Dict[str, Any]] = None
    phones: Optional[List[Dict[str, Any]]] = None
    emails: Optional[List[Dict[str, Any]]] = None
    relatives: Optional[List[Dict[str, Any]]] = None
    associates: Optional[List[Dict[str, Any]]] = None
    education: Optional[List[Dict[str, Any]]] = None
    employment: Optional[List[Dict[str, Any]]] = None
    profiles: Optional[Dict[str, Any]] = None


class ReversePhoneOwnerBusiness(BaseModel):
    """Model for a business associated with a phone number."""
    id: Optional[str] = None
    name: Optional[str] = None
    alt_names: Optional[List[str]] = None
    description: Optional[str] = None
    founded: Optional[int] = None
    employee_count: Optional[str] = None
    industry: Optional[str] = None
    link: Optional[HttpUrl] = None
    location: Optional[Dict[str, Any]] = None
    address: Optional[Dict[str, Any]] = None
    phones: Optional[List[Dict[str, Any]]] = None
    emails: Optional[List[Dict[str, Any]]] = None
    categories: Optional[List[str]] = None
    profiles: Optional[Dict[str, Any]] = None


class ReversePhoneResponse(BaseModel):
    """Response model for the Reverse Phone API."""
    id: Optional[str] = Field(
        None, 
        description="The persistent ID of the phone number.",
        example="Phone.3dbb6fef-a2df-4b08-cfe3-bc7128b6f5b4"
    )
    phone_number: Optional[str] = Field(
        None,
        description="The phone number in E.164 or local format.",
        example="2069735100"
    )
    is_valid: Optional[bool] = Field(
        None,
        description="True if the phone number is valid.",
        example=True
    )
    country_calling_code: Optional[str] = Field(
        None,
        description="The country code of the phone number.",
        example="1"
    )
    line_type: Optional[LineType] = Field(
        None,
        description="The type of phone line."
    )
    carrier: Optional[str] = Field(
        None,
        description="The carrier providing service for the phone number.",
        example="Trestle Telco"
    )
    is_prepaid: Optional[bool] = Field(
        None,
        description="True if the phone is associated with a prepaid account.",
        example=False
    )
    is_commercial: Optional[bool] = Field(
        None,
        description="True if the phone number is registered to a business.",
        example=False
    )
    owners: Optional[List[Union[ReversePhoneOwnerPerson, ReversePhoneOwnerBusiness]]] = Field(
        None,
        description="The owner(s) associated with the phone."
    )
    error: Optional[PartialError] = Field(
        None,
        description="Partial error information if the request was not fully successful."
    )
    warnings: Optional[List[str]] = Field(
        None,
        description="Warnings returned as part of the response, if applicable."
    )

    class Config:
        json_encoders = {
            HttpUrl: lambda v: str(v) if v else None
        }
        schema_extra = {
            "example": {
                "id": "Phone.3dbb6fef-a2df-4b08-cfe3-bc7128b6f5b4",
                "phone_number": "2069735100",
                "is_valid": True,
                "country_calling_code": "1",
                "line_type": "NonFixedVOIP",
                "carrier": "Trestle Telco",
                "is_prepaid": False,
                "is_commercial": False,
                "owners": [],
                "error": {
                    "name": "InternalError",
                    "message": "Could not retrieve entire response"
                },
                "warnings": ["Missing Input"]
            }
        }
