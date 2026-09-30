from datetime import datetime

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, Text, JSON, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    mobile: Mapped[str] = mapped_column(String(16), unique=True, index=True)
    password_hash: Mapped[str | None] = mapped_column(String(255))
    role: Mapped[str] = mapped_column(String(16), default="citizen", index=True)
    department: Mapped[str | None] = mapped_column(String(120), index=True)
    preferred_language: Mapped[str] = mapped_column(String(5), default="en")
    name: Mapped[str | None] = mapped_column(String(120))
    gender: Mapped[str | None] = mapped_column(String(20))
    email: Mapped[str | None] = mapped_column(String(254))
    city: Mapped[str | None] = mapped_column(String(120))
    state: Mapped[str | None] = mapped_column(String(120))
    district: Mapped[str | None] = mapped_column(String(120))
    village: Mapped[str | None] = mapped_column(String(120))
    pincode: Mapped[str | None] = mapped_column(String(12))
    address: Mapped[str | None] = mapped_column(String(500))
    latitude: Mapped[float | None] = mapped_column(Float)
    longitude: Mapped[float | None] = mapped_column(Float)
    profile_photo_data: Mapped[str | None] = mapped_column(Text)
    profile_complete: Mapped[bool] = mapped_column(Boolean, default=False)
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    complaints: Mapped[list["Complaint"]] = relationship(
        back_populates="citizen", foreign_keys="Complaint.citizen_id"
    )
    assigned_complaints: Mapped[list["Complaint"]] = relationship(
        back_populates="assigned_officer", foreign_keys="Complaint.assigned_officer_id"
    )


class Complaint(Base):
    __tablename__ = "complaints"

    id: Mapped[int] = mapped_column(primary_key=True)
    ticket_number: Mapped[str] = mapped_column(String(32), unique=True, index=True)
    citizen_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    complaint_text: Mapped[str] = mapped_column(Text)

    category_predicted: Mapped[str | None] = mapped_column(String(80), index=True)
    category_verified: Mapped[str | None] = mapped_column(String(120))
    category_source: Mapped[str | None] = mapped_column(String(32))
    ml_confidence: Mapped[float | None] = mapped_column(Float)
    severity: Mapped[str | None] = mapped_column(String(32), index=True)
    priority: Mapped[str | None] = mapped_column(String(32), index=True)
    department: Mapped[str | None] = mapped_column(String(120), index=True)
    team: Mapped[str | None] = mapped_column(String(120))
    routing_status: Mapped[str | None] = mapped_column(String(32))

    city: Mapped[str | None] = mapped_column(String(120), index=True)
    district: Mapped[str | None] = mapped_column(String(120), index=True)
    area: Mapped[str | None] = mapped_column(String(120))
    state: Mapped[str | None] = mapped_column(String(120))
    latitude: Mapped[float | None] = mapped_column(Float)
    longitude: Mapped[float | None] = mapped_column(Float)
    location_source: Mapped[str | None] = mapped_column(String(20))

    language: Mapped[str | None] = mapped_column(String(12))
    estimated_resolution_hours: Mapped[float | None] = mapped_column(Float)
    estimated_resolution_days: Mapped[float | None] = mapped_column(Float)
    evidence_path: Mapped[str | None] = mapped_column(String(500))
    ai_response: Mapped[str | None] = mapped_column(Text)

    duplicate_flag: Mapped[bool] = mapped_column(Boolean, default=False)
    duplicate_similarity: Mapped[float | None] = mapped_column(Float)
    duplicate_existing_id: Mapped[str | None] = mapped_column(String(120))

    assigned_department: Mapped[str | None] = mapped_column(String(120), index=True)
    assigned_officer_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), index=True)

    status: Mapped[str] = mapped_column(String(32), default="pending", index=True)
    status_note: Mapped[str | None] = mapped_column(String(1000))
    resolution_hours_actual: Mapped[float | None] = mapped_column(Float)
    resolved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    sla_due_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), index=True)
    escalated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    escalation_level: Mapped[int] = mapped_column(Integer, default=0)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), index=True)

    citizen: Mapped[User] = relationship(back_populates="complaints", foreign_keys=[citizen_id])
    assigned_officer: Mapped[User | None] = relationship(back_populates="assigned_complaints", foreign_keys=[assigned_officer_id])
    history: Mapped[list["ComplaintStatusHistory"]] = relationship(back_populates="complaint", cascade="all, delete-orphan")
    notifications: Mapped[list["Notification"]] = relationship(back_populates="complaint", cascade="all, delete-orphan")
    feedback: Mapped["Feedback | None"] = relationship(back_populates="complaint", uselist=False, cascade="all, delete-orphan")

    @property
    def citizen_name(self) -> str | None:
        return self.citizen.name if self.citizen else None

    @property
    def citizen_mobile(self) -> str | None:
        return self.citizen.mobile if self.citizen else None

    @property
    def assigned_officer_name(self) -> str | None:
        return self.assigned_officer.name if self.assigned_officer else None


class ComplaintDraft(Base):
    __tablename__ = "complaint_drafts"

    id: Mapped[int] = mapped_column(primary_key=True)
    token: Mapped[str] = mapped_column(String(80), unique=True, index=True)
    citizen_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    payload_json: Mapped[dict] = mapped_column(JSON)
    ai_json: Mapped[dict] = mapped_column(JSON)
    ticket_number: Mapped[str] = mapped_column(String(32), unique=True, index=True)
    complaint_id: Mapped[int | None] = mapped_column(ForeignKey("complaints.id", ondelete="SET NULL"))
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), index=True)


class ComplaintStatusHistory(Base):
    __tablename__ = "complaint_status_history"

    id: Mapped[int] = mapped_column(primary_key=True)
    complaint_id: Mapped[int] = mapped_column(ForeignKey("complaints.id", ondelete="CASCADE"), index=True)
    old_status: Mapped[str | None] = mapped_column(String(32))
    new_status: Mapped[str] = mapped_column(String(32))
    note: Mapped[str | None] = mapped_column(String(1000))
    changed_by_user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), index=True)

    complaint: Mapped[Complaint] = relationship(back_populates="history")


class Notification(Base):
    __tablename__ = "notifications"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    complaint_id: Mapped[int | None] = mapped_column(ForeignKey("complaints.id", ondelete="SET NULL"), index=True)
    title: Mapped[str] = mapped_column(String(200))
    message: Mapped[str] = mapped_column(String(1000))
    is_read: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), index=True)

    complaint: Mapped[Complaint | None] = relationship(back_populates="notifications")


class Feedback(Base):
    __tablename__ = "feedback"

    id: Mapped[int] = mapped_column(primary_key=True)
    complaint_id: Mapped[int] = mapped_column(ForeignKey("complaints.id", ondelete="CASCADE"), unique=True, index=True)
    citizen_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    rating: Mapped[int] = mapped_column(Integer)
    comment: Mapped[str | None] = mapped_column(String(1000))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    complaint: Mapped[Complaint] = relationship(back_populates="feedback")
