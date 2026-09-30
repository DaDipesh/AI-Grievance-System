from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class RegisterRequest(BaseModel):
    mobile: str = Field(min_length=8, max_length=16)
    password: str = Field(min_length=8, max_length=128)
    confirm_password: str = Field(min_length=8, max_length=128)
    language: str = Field(default="en", pattern="^(en|hi)$")
    role: str = Field(default="citizen", pattern="^(citizen|officer|admin)$")
    special_id: str | None = Field(default=None, min_length=1, max_length=128)
    name: str | None = Field(default=None, max_length=120)
    email: EmailStr | None = None
    department: str | None = Field(default=None, max_length=120)

class LoginRequest(BaseModel):
    mobile: str = Field(min_length=8, max_length=16)
    password: str = Field(min_length=1, max_length=128)
    language: str = Field(default="en", pattern="^(en|hi)$")


class ProfileUpdate(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    gender: str = Field(min_length=1, max_length=20)
    email: EmailStr
    city: str = Field(min_length=2, max_length=120)
    state: str = Field(min_length=2, max_length=120)
    district: str | None = Field(default=None, max_length=120)
    village: str | None = Field(default=None, max_length=120)
    pincode: str | None = Field(default=None, max_length=12)
    address: str | None = Field(default=None, max_length=500)
    latitude: float | None = None
    longitude: float | None = None
    profile_photo_data: str | None = Field(default=None, max_length=7_000_000)
    remove_profile_photo: bool = False


class StaffProfileUpdate(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    email: EmailStr
    gender: str = Field(min_length=1, max_length=20)
    city: str = Field(min_length=2, max_length=120)
    state: str = Field(min_length=2, max_length=120)
    district: str | None = Field(default=None, max_length=120)
    address: str | None = Field(default=None, max_length=500)
    latitude: float | None = None
    longitude: float | None = None
    profile_photo_data: str | None = Field(default=None, max_length=7_000_000)
    remove_profile_photo: bool = False
    model_config = ConfigDict(extra="forbid")


class UserOut(BaseModel):
    id: int
    mobile: str
    role: str
    department: str | None
    preferred_language: str
    name: str | None
    gender: str | None
    email: EmailStr | None
    city: str | None
    state: str | None
    district: str | None
    village: str | None
    pincode: str | None
    address: str | None
    profile_photo_data: str | None
    latitude: float | None
    longitude: float | None
    profile_complete: bool
    active: bool
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut


class ComplaintCreate(BaseModel):
    complaint_text: str = Field(min_length=5, max_length=5000)
    city: str | None = Field(default=None, max_length=120)
    district: str | None = Field(default=None, max_length=120)
    area: str | None = Field(default=None, max_length=120)
    state: str | None = Field(default=None, max_length=120)
    latitude: float | None = None
    longitude: float | None = None
    location_source: str | None = Field(default=None, max_length=20)
    evidence_file_id: str | None = Field(default=None, max_length=500)
    preview_token: str | None = Field(default=None, max_length=80)


class ComplaintOut(BaseModel):
    id: int
    ticket_number: str
    citizen_name: str | None = None
    citizen_mobile: str | None = None
    citizen_id: int
    complaint_text: str
    category_predicted: str | None
    category_verified: str | None
    category_source: str | None
    ml_confidence: float | None
    severity: str | None
    priority: str | None
    department: str | None
    team: str | None
    routing_status: str | None
    city: str | None
    district: str | None
    area: str | None
    state: str | None
    latitude: float | None
    longitude: float | None
    location_source: str | None
    language: str | None
    estimated_resolution_hours: float | None
    estimated_resolution_days: float | None
    evidence_path: str | None
    ai_response: str | None
    duplicate_flag: bool
    duplicate_similarity: float | None
    assigned_department: str | None
    assigned_officer_id: int | None
    assigned_officer_name: str | None = None
    status: str
    status_note: str | None
    resolution_hours_actual: float | None
    created_at: datetime
    updated_at: datetime
    resolved_at: datetime | None
    sla_due_at: datetime | None
    escalated_at: datetime | None
    escalation_level: int
    model_config = ConfigDict(from_attributes=True)


class ComplaintStatusUpdate(BaseModel):
    status: str = Field(pattern="^(pending|in_progress|resolved|rejected|reopened|closed)$")
    note: str | None = Field(default=None, max_length=1000)
    category_verified: str | None = Field(default=None, max_length=120)


class ComplaintAssign(BaseModel):
    officer_id: int


class FeedbackCreate(BaseModel):
    rating: int = Field(ge=1, le=5)
    comment: str | None = Field(default=None, max_length=1000)


class NotificationOut(BaseModel):
    id: int
    complaint_id: int | None
    title: str
    message: str
    is_read: bool
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class ComplaintHistoryOut(BaseModel):
    id: int
    complaint_id: int
    old_status: str | None
    new_status: str
    note: str | None
    changed_by_user_id: int | None
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class FeedbackOut(BaseModel):
    id: int
    complaint_id: int
    rating: int
    comment: str | None
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class ComplaintPreviewOut(BaseModel):
    preview_token: str
    ticket_number: str
    complaint_text: str
    category_predicted: str | None
    severity: str | None
    priority: str | None
    department: str | None
    team: str | None
    city: str | None
    district: str | None
    area: str | None
    state: str | None
    latitude: float | None
    longitude: float | None
    language: str | None
    estimated_resolution_hours: float | None
    estimated_resolution_days: float | None
    duplicate_flag: bool
    duplicate_similarity: float | None
    response: str | None

