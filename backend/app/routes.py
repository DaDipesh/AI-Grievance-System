from __future__ import annotations

import logging
import secrets
import hmac
from datetime import datetime, timedelta, timezone
from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.ai_service import analyze_complaint_with_ai
from app.config import get_settings
from app.database import get_db
from app.files import save_evidence
from app.i18n import message, normalize_ui_language
from app.models import Complaint, ComplaintDraft, ComplaintStatusHistory, Feedback, Notification, User
from app.schemas import (
    ComplaintAssign, ComplaintCreate, ComplaintHistoryOut, ComplaintOut, ComplaintPreviewOut,
    ComplaintStatusUpdate, FeedbackCreate, FeedbackOut, NotificationOut, ProfileUpdate, StaffProfileUpdate,
    LoginRequest, RegisterRequest, TokenOut, UserOut,
)
from app.security import create_access_token, current_user, hash_password, normalize_mobile, require_roles, verify_password

router = APIRouter()
logger = logging.getLogger("grievance.api")
STATUS_VALUES = {"pending", "in_progress", "resolved", "rejected", "reopened", "closed"}


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


def aware(dt: datetime | None) -> datetime | None:
    if dt is None:
        return None
    return dt.replace(tzinfo=timezone.utc) if dt.tzinfo is None else dt


def lang(user: User) -> str:
    return normalize_ui_language(user.preferred_language)


def complaint_visible_to(user: User, complaint: Complaint) -> bool:
    if user.role == "admin":
        return True
    if user.role == "citizen":
        return complaint.citizen_id == user.id
    return complaint.assigned_officer_id == user.id or complaint.assigned_department == user.department


def notify_user(db: Session, user_id: int, title_en: str, title_hi: str, body_en: str, body_hi: str, complaint_id: int | None = None, language_override: str | None = None) -> None:
    target = db.get(User, user_id)
    if not target:
        return
    hi = (str(language_override).lower() in {"hindi", "hinglish"}) if language_override else normalize_ui_language(target.preferred_language) == "hi"
    db.add(Notification(user_id=user_id, complaint_id=complaint_id, title=title_hi if hi else title_en, message=body_hi if hi else body_en))


def notify_department(db: Session, department: str | None, ticket: str, category: str, complaint_id: int) -> None:
    if not department:
        return
    officers = db.scalars(select(User).where(User.role == "officer", User.department == department, User.active.is_(True))).all()
    for officer in officers:
        notify_user(db, officer.id, "New complaint assigned", "नई शिकायत सौंपी गई", f"Complaint {ticket} ({category}) has been assigned to your department.", f"शिकायत {ticket} ({category}) आपके विभाग को सौंपी गई है।", complaint_id)


@router.post("/auth/register", response_model=TokenOut, status_code=201)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    mobile = normalize_mobile(payload.mobile)
    if payload.password != payload.confirm_password:
        raise HTTPException(422, "Passwords do not match.")
    role = payload.role
    if role in {"officer", "admin"}:
        settings = get_settings()
        if role == "admin":
            expected_id = settings.admin_registration_id
            required_length = 16
        else:
            officer_ids = {
                "Water Supply Department": settings.officer_water_id,
                "Electricity Department": settings.officer_electricity_id,
                "Municipal Street Light Department": settings.officer_street_light_id,
                "Road Department": settings.officer_road_id,
                "Health Department": settings.officer_healthcare_id,
                "Sanitation Department": settings.officer_sanitation_id,
                "Drainage Department": settings.officer_drainage_id,
                "Environment Department": settings.officer_environment_id,
            }
            if payload.department not in officer_ids:
                raise HTTPException(422, "Select one of the listed departments for the officer account.")
            expected_id = officer_ids.get(payload.department or "", "")
            required_length = 12
        if not expected_id:
            raise HTTPException(403, f"{role.title()} registration is not enabled. Ask the system administrator to configure its registration ID.")
        if not payload.special_id or len(payload.special_id) != required_length or not hmac.compare_digest(payload.special_id, expected_id):
            raise HTTPException(403, "Invalid ID. This account was not registered.")
    if db.scalar(select(User).where(User.mobile == mobile)):
        raise HTTPException(409, "This mobile number is already registered. Please log in.")
    user = User(mobile=mobile, password_hash=hash_password(payload.password), role=role, preferred_language=payload.language,
                name=payload.name.strip() if role == "citizen" and payload.name else None,
                email=str(payload.email) if role == "citizen" and payload.email else None,
                department=payload.department.strip() if role == "officer" and payload.department else None,
                profile_complete=False)
    db.add(user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(409, "This mobile number is already registered. Please log in.") from None
    db.refresh(user)
    return {"access_token": create_access_token(user), "user": user}


@router.post("/auth/login", response_model=TokenOut)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    mobile = normalize_mobile(payload.mobile)
    user = db.scalar(select(User).where(User.mobile == mobile))
    if user is None:
        detail = "इस मोबाइल नंबर से कोई खाता नहीं है। पहले रजिस्टर करें।" if payload.language == "hi" else "No account is registered with this mobile number. Please register first."
        raise HTTPException(404, detail)
    if not user.password_hash or not verify_password(payload.password, user.password_hash):
        raise HTTPException(401, "मोबाइल नंबर या पासवर्ड गलत है।" if payload.language == "hi" else "Incorrect mobile number or password.")
    if not user.active:
        raise HTTPException(403, "This account is inactive.")
    user.preferred_language = payload.language
    db.commit()
    db.refresh(user)
    return {"access_token": create_access_token(user), "user": user}


@router.get("/auth/me", response_model=UserOut)
def me(user: User = Depends(current_user)):
    return user


@router.get("/users/me/photo")
def my_profile_photo(user: User = Depends(current_user)):
    return {"photo_data": user.profile_photo_data}


@router.put("/users/me/language", response_model=UserOut)
def update_language(payload: dict, user: User = Depends(current_user), db: Session = Depends(get_db)):
    selected = payload.get("language") if isinstance(payload, dict) else None
    if selected not in {"en", "hi"}:
        raise HTTPException(422, "Choose English or Hindi.")
    user.preferred_language = selected
    db.commit(); db.refresh(user)
    return user


@router.put("/users/me/profile", response_model=UserOut)
def update_profile(payload: ProfileUpdate, user: User = Depends(current_user), db: Session = Depends(get_db)):
    if user.role != "citizen":
        raise HTTPException(403, "Use the staff profile form for this account.")
    user.name, user.gender, user.email = payload.name.strip(), payload.gender.strip(), str(payload.email)
    user.city, user.state = payload.city.strip(), payload.state.strip()
    user.district = payload.district.strip() if payload.district else None
    user.village = payload.village.strip() if payload.village else None
    user.pincode = payload.pincode.strip() if payload.pincode else None
    user.address = payload.address.strip() if payload.address else None
    user.latitude, user.longitude = payload.latitude, payload.longitude
    if payload.remove_profile_photo:
        user.profile_photo_data = None
    elif payload.profile_photo_data is not None:
        if not payload.profile_photo_data.startswith(("data:image/jpeg;base64,", "data:image/png;base64,")):
            raise HTTPException(422, "Profile photo must be a JPEG or PNG image.")
        user.profile_photo_data = payload.profile_photo_data
    user.profile_complete = True
    db.commit(); db.refresh(user)
    return user


@router.put("/users/me/staff-profile", response_model=UserOut)
def update_staff_profile(payload: StaffProfileUpdate, user: User = Depends(require_roles("officer", "admin")), db: Session = Depends(get_db)):
    user.name = payload.name.strip()
    user.email = str(payload.email)
    user.gender = payload.gender.strip()
    user.city, user.state = payload.city.strip(), payload.state.strip()
    user.district = payload.district.strip() if payload.district else None
    user.address = payload.address.strip() if payload.address else None
    user.latitude, user.longitude = payload.latitude, payload.longitude
    if payload.remove_profile_photo:
        user.profile_photo_data = None
    elif payload.profile_photo_data is not None:
        if not payload.profile_photo_data.startswith(("data:image/jpeg;base64,", "data:image/png;base64,")):
            raise HTTPException(422, "Profile photo must be a JPEG or PNG image.")
        user.profile_photo_data = payload.profile_photo_data
    user.profile_complete = True
    db.commit()
    db.refresh(user)
    return user


@router.get("/departments")
def departments():
    return {"departments": [
        "Water Supply Department", "Electricity Department", "Municipal Street Light Department", "Road Department",
        "Health Department", "Sanitation Department", "Drainage Department", "Environment Department",
    ]}


def _evidence_path(payload: ComplaintCreate) -> tuple[str | None, str | None]:
    evidence_name = payload.evidence_file_id.strip() if payload.evidence_file_id else None
    if not evidence_name:
        return None, None
    if Path(evidence_name).name != evidence_name:
        raise HTTPException(422, "Invalid evidence file id.")
    upload_dir = Path(get_settings().upload_dir)
    if not upload_dir.is_absolute():
        upload_dir = Path(__file__).resolve().parents[1] / upload_dir
    path = upload_dir.resolve() / evidence_name
    if not path.is_file():
        raise HTTPException(404, "Evidence file was not found.")
    return evidence_name, str(path)


def _json_safe(value):
    """Convert AI/NumPy values to native JSON types before DB/API output."""
    if isinstance(value, dict):
        return {str(key): _json_safe(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_safe(item) for item in value]
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if hasattr(value, "tolist"):
        return _json_safe(value.tolist())
    if hasattr(value, "item"):
        return _json_safe(value.item())
    return str(value)


def _run_ai(payload: ComplaintCreate) -> dict:
    if (payload.latitude is None) != (payload.longitude is None):
        raise HTTPException(422, "Provide both latitude and longitude for the complaint location.")
    _, image_path = _evidence_path(payload)
    try:
        result = _json_safe(analyze_complaint_with_ai(payload.complaint_text.strip(), city=payload.city, district=payload.district, area=payload.area, image_path=image_path))
    except Exception:
        logger.exception("Complaint AI analysis failed")
        raise HTTPException(500, message("server_error", payload.language)) from None
    if not result.get("problem_detected", True):
        raise HTTPException(422, result.get("clarification_question") or "Please provide more details about the complaint.")
    if result.get("needs_clarification"):
        raise HTTPException(422, result.get("clarification_question") or "Please provide more details about the complaint.")
    if not result.get("category"):
        raise HTTPException(422, "AI could not determine the complaint category.")
    return result


def _new_ticket(db: Session) -> str:
    ticket = "GRV-" + secrets.token_hex(4).upper()
    while db.scalar(select(Complaint.id).where(Complaint.ticket_number == ticket)) or db.scalar(select(ComplaintDraft.id).where(ComplaintDraft.ticket_number == ticket)):
        ticket = "GRV-" + secrets.token_hex(4).upper()
    return ticket


def _preview_out(draft: ComplaintDraft) -> dict:
    p, a = draft.payload_json, draft.ai_json
    dup = a.get("duplicate_result") or {}
    return {
        "preview_token": draft.token, "ticket_number": draft.ticket_number, "complaint_text": p["complaint_text"],
        "category_predicted": a.get("category"), "severity": a.get("severity"), "priority": a.get("priority"),
        "department": a.get("department"), "team": a.get("team"), "city": p.get("city"), "district": p.get("district"),
        "area": p.get("area"), "state": p.get("state"), "latitude": p.get("latitude"), "longitude": p.get("longitude"),
        "language": a.get("language"), "estimated_resolution_hours": a.get("resolution_hours"), "estimated_resolution_days": a.get("resolution_days"),
        "duplicate_flag": bool(dup.get("is_duplicate")), "duplicate_similarity": dup.get("similarity"), "response": a.get("response"),
    }


@router.post("/complaints/preview", response_model=ComplaintPreviewOut)
def preview_complaint(payload: ComplaintCreate, user: User = Depends(require_roles("citizen")), db: Session = Depends(get_db)):
    ai = _run_ai(payload)
    draft = ComplaintDraft(
        token=secrets.token_urlsafe(32), citizen_id=user.id,
        payload_json=payload.model_dump(exclude={"preview_token"}), ai_json=ai,
        ticket_number=_new_ticket(db), expires_at=utcnow() + timedelta(minutes=20),
    )
    db.add(draft); db.commit(); db.refresh(draft)
    return _preview_out(draft)


@router.post("/complaints", response_model=ComplaintOut, status_code=201)
def create_complaint(payload: ComplaintCreate, user: User = Depends(require_roles("citizen")), db: Session = Depends(get_db)):
    draft = None
    if payload.preview_token:
        draft = db.scalar(select(ComplaintDraft).where(ComplaintDraft.token == payload.preview_token, ComplaintDraft.citizen_id == user.id))
        if draft is None or aware(draft.expires_at) <= utcnow():
            raise HTTPException(410, "Complaint preview has expired. Please analyze the complaint again.")
        data = draft.payload_json; ai_result = draft.ai_json; ticket = draft.ticket_number
        payload = ComplaintCreate(**data, preview_token=draft.token)
    else:
        ai_result = _run_ai(payload); ticket = _new_ticket(db)

    evidence_name, _ = _evidence_path(payload)
    duplicate = ai_result.get("duplicate_result") or {}
    resolution_hours, resolution_days = ai_result.get("resolution_hours"), ai_result.get("resolution_days")
    department = ai_result.get("department")
    officer = None
    if department:
        officer = db.scalar(select(User).where(User.role == "officer", User.department == department, User.active.is_(True)).order_by(User.id.asc()).limit(1))
    due_at = utcnow() + timedelta(hours=float(resolution_hours)) if resolution_hours else None
    complaint = Complaint(
        ticket_number=ticket, citizen_id=user.id, complaint_text=payload.complaint_text.strip(),
        category_predicted=ai_result.get("category"), category_source=ai_result.get("category_source"), ml_confidence=ai_result.get("ml_confidence"),
        severity=ai_result.get("severity"), priority=ai_result.get("priority"), department=department, team=ai_result.get("team"), routing_status=ai_result.get("routing_status"),
        city=payload.city, district=payload.district, area=payload.area, state=payload.state, latitude=payload.latitude, longitude=payload.longitude,
        location_source=payload.location_source, language=ai_result.get("language"), estimated_resolution_hours=resolution_hours, estimated_resolution_days=resolution_days,
        evidence_path=evidence_name, ai_response=ai_result.get("response"), duplicate_flag=bool(duplicate.get("is_duplicate")), duplicate_similarity=duplicate.get("similarity"),
        duplicate_existing_id=str(duplicate.get("existing_complaint_id")) if duplicate.get("existing_complaint_id") is not None else None,
        assigned_department=department, assigned_officer_id=officer.id if officer else None, sla_due_at=due_at, status="pending",
    )
    db.add(complaint); db.flush()
    db.add(ComplaintStatusHistory(complaint_id=complaint.id, old_status=None, new_status="pending", note="Complaint registered", changed_by_user_id=user.id))
    notify_user(db, user.id, "Complaint registered", "शिकायत दर्ज हो गई", message("registered", "en", ticket=ticket, category=complaint.category_predicted or "", city=complaint.city or "", area=complaint.area or ""), message("registered", "hi", ticket=ticket, category=complaint.category_predicted or "", city=complaint.city or "", area=complaint.area or ""), complaint.id, language_override=complaint.language)
    notify_department(db, department, ticket, complaint.category_predicted or "", complaint.id)
    if officer:
        notify_user(db, officer.id, "Complaint assigned", "शिकायत सौंपी गई", f"Complaint {ticket} was assigned to you.", f"शिकायत {ticket} आपको सौंपी गई है।", complaint.id)
    if draft:
        db.delete(draft)
    db.commit(); db.refresh(complaint)
    return complaint


@router.post("/complaints/evidence", status_code=201)
async def upload_evidence(file: UploadFile = File(...), user: User = Depends(require_roles("citizen"))):
    return {"file_id": await save_evidence(file, user.preferred_language)}


@router.get("/complaints/evidence/{file_id}")
def get_evidence(file_id: str, user: User = Depends(current_user), db: Session = Depends(get_db)):
    if Path(file_id).name != file_id or not any(c.evidence_path == file_id for c in db.scalars(select(Complaint)).all() if complaint_visible_to(user, c)):
        raise HTTPException(404, message("not_found", lang(user)))
    upload_dir = Path(get_settings().upload_dir)
    if not upload_dir.is_absolute():
        upload_dir = Path(__file__).resolve().parents[1] / upload_dir
    path = upload_dir.resolve() / file_id
    if not path.is_file():
        raise HTTPException(404, message("not_found", lang(user)))
    return FileResponse(path, headers={"Cache-Control": "private, no-store"})


@router.get("/complaints", response_model=list[ComplaintOut])
def my_complaints(user: User = Depends(require_roles("citizen")), db: Session = Depends(get_db)):
    return db.scalars(select(Complaint).where(Complaint.citizen_id == user.id).order_by(Complaint.created_at.desc())).all()


@router.get("/complaints/by-ticket/{ticket_number}", response_model=ComplaintOut)
def complaint_by_ticket(ticket_number: str, user: User = Depends(current_user), db: Session = Depends(get_db)):
    item = db.scalar(select(Complaint).where(Complaint.ticket_number == ticket_number.upper()))
    if item is None or not complaint_visible_to(user, item):
        raise HTTPException(404, message("not_found", lang(user)))
    return item


@router.get("/complaints/{complaint_id}", response_model=ComplaintOut)
def get_complaint(complaint_id: int, user: User = Depends(current_user), db: Session = Depends(get_db)):
    item = db.get(Complaint, complaint_id)
    if item is None or not complaint_visible_to(user, item):
        raise HTTPException(404, message("not_found", lang(user)))
    return item


@router.get("/complaints/{complaint_id}/history", response_model=list[ComplaintHistoryOut])
def complaint_history(complaint_id: int, user: User = Depends(current_user), db: Session = Depends(get_db)):
    complaint = db.get(Complaint, complaint_id)
    if complaint is None or not complaint_visible_to(user, complaint):
        raise HTTPException(404, message("not_found", lang(user)))
    return db.scalars(select(ComplaintStatusHistory).where(ComplaintStatusHistory.complaint_id == complaint_id).order_by(ComplaintStatusHistory.created_at.asc())).all()


@router.get("/officer/complaints", response_model=list[ComplaintOut])
def officer_complaints(user: User = Depends(require_roles("officer", "admin")), db: Session = Depends(get_db)):
    query = select(Complaint)
    if user.role == "officer":
        query = query.where((Complaint.assigned_officer_id == user.id) | (Complaint.assigned_department == user.department))
    return db.scalars(query.order_by(Complaint.created_at.desc())).all()


@router.put("/officer/complaints/{complaint_id}/status", response_model=ComplaintOut)
def update_complaint_status(complaint_id: int, payload: ComplaintStatusUpdate, user: User = Depends(require_roles("officer", "admin")), db: Session = Depends(get_db)):
    complaint = db.get(Complaint, complaint_id)
    if complaint is None or not complaint_visible_to(user, complaint):
        raise HTTPException(404, message("not_found", lang(user)))
    old_status = complaint.status
    if payload.status == "reopened" and user.role != "admin":
        raise HTTPException(403, "Only administrators can reopen complaints.")
    if old_status == "closed" and payload.status != "closed" and user.role != "admin":
        raise HTTPException(409, "Closed complaints can only be reopened by an administrator.")
    complaint.status, complaint.status_note = payload.status, payload.note
    if payload.category_verified:
        complaint.category_verified = payload.category_verified.strip()
    if payload.status == "resolved" and old_status != "resolved":
        created = aware(complaint.created_at) or utcnow(); complaint.resolved_at = utcnow()
        complaint.resolution_hours_actual = round(max(0.0, (complaint.resolved_at - created).total_seconds() / 3600), 2)
    elif payload.status == "reopened":
        complaint.resolved_at = None; complaint.resolution_hours_actual = None
    complaint.updated_at = utcnow()
    db.add(ComplaintStatusHistory(complaint_id=complaint.id, old_status=old_status, new_status=payload.status, note=payload.note, changed_by_user_id=user.id))
    if payload.status == "resolved":
        notify_user(db, complaint.citizen_id, "Complaint resolved", "शिकायत का समाधान हो गया", f"Your complaint {complaint.ticket_number} has been resolved.", f"आपकी शिकायत {complaint.ticket_number} का समाधान हो गया है।", complaint.id, language_override=complaint.language)
    else:
        notify_user(db, complaint.citizen_id, "Complaint status updated", "शिकायत की स्थिति अपडेट हुई", f"Complaint {complaint.ticket_number} status is now {payload.status.replace('_',' ')}.", f"आपकी शिकायत {complaint.ticket_number} की स्थिति अब {payload.status.replace('_',' ')} है।", complaint.id, language_override=complaint.language)
    if payload.status == "resolved":
        try:
            from training.data_collector import save_verified_complaint
            save_verified_complaint(complaint_id=complaint.ticket_number, complaint_text=complaint.complaint_text, language=complaint.language or "en", category_predicted=complaint.category_predicted or "", category_verified=complaint.category_verified or complaint.category_predicted or "", severity=complaint.severity or "", priority=complaint.priority or "", department=complaint.department or "", city=complaint.city or "", district=complaint.district or "", area=complaint.area or "", resolution_hours=complaint.resolution_hours_actual)
        except Exception:
            pass
    db.commit(); db.refresh(complaint)
    return complaint


@router.put("/admin/complaints/{complaint_id}/assign", response_model=ComplaintOut)
def assign_complaint(complaint_id: int, payload: ComplaintAssign, user: User = Depends(require_roles("admin")), db: Session = Depends(get_db)):
    complaint, officer = db.get(Complaint, complaint_id), db.get(User, payload.officer_id)
    if complaint is None: raise HTTPException(404, "Complaint not found.")
    if officer is None or officer.role != "officer" or not officer.active: raise HTTPException(422, "Selected user is not an active officer.")
    if complaint.department and officer.department != complaint.department: raise HTTPException(422, "Officer department does not match complaint department.")
    complaint.assigned_officer_id, complaint.assigned_department, complaint.updated_at = officer.id, officer.department, utcnow()
    notify_user(db, officer.id, "Complaint assigned", "शिकायत सौंपी गई", f"Complaint {complaint.ticket_number} has been assigned to you.", f"शिकायत {complaint.ticket_number} आपको सौंपी गई है।", complaint.id)
    db.commit(); db.refresh(complaint); return complaint


@router.get("/admin/complaints", response_model=list[ComplaintOut])
def admin_complaints(user: User = Depends(require_roles("admin")), db: Session = Depends(get_db)):
    return db.scalars(select(Complaint).order_by(Complaint.created_at.desc())).all()


@router.get("/admin/officers")
def admin_officers(user: User = Depends(require_roles("admin")), db: Session = Depends(get_db)):
    officers = db.scalars(select(User).where(User.role == "officer").order_by(User.department, User.name)).all()
    return [{"id": o.id, "name": o.name, "mobile": o.mobile, "gender": o.gender, "email": o.email, "profile_photo_data": o.profile_photo_data, "department": o.department, "city": o.city, "district": o.district, "state": o.state, "address": o.address, "latitude": o.latitude, "longitude": o.longitude, "active": o.active} for o in officers]


@router.get("/admin/registration-ids")
def admin_registration_ids(user: User = Depends(require_roles("admin"))):
    settings = get_settings()
    return {
        "admin": {"label": "Administrator", "registration_id": settings.admin_registration_id},
        "officers": [
            {"department": "Water Supply Department", "category": "💧 Water Supply", "registration_id": settings.officer_water_id},
            {"department": "Electricity Department", "category": "⚡ Electricity", "registration_id": settings.officer_electricity_id},
            {"department": "Municipal Street Light Department", "category": "💡 Street Light", "registration_id": settings.officer_street_light_id},
            {"department": "Road Department", "category": "🛣️ Road", "registration_id": settings.officer_road_id},
            {"department": "Health Department", "category": "🏥 Healthcare", "registration_id": settings.officer_healthcare_id},
            {"department": "Sanitation Department", "category": "🧹 Sanitation", "registration_id": settings.officer_sanitation_id},
            {"department": "Drainage Department", "category": "🚰 Drainage", "registration_id": settings.officer_drainage_id},
            {"department": "Environment Department", "category": "🌱 Environment", "registration_id": settings.officer_environment_id},
        ],
    }


@router.get("/admin/health-summary")
def admin_summary(user: User = Depends(require_roles("admin")), db: Session = Depends(get_db)):
    total = db.scalar(select(func.count()).select_from(Complaint)) or 0
    status_rows = db.execute(select(Complaint.status, func.count()).group_by(Complaint.status)).all()
    category_rows = db.execute(select(Complaint.category_predicted, func.count()).group_by(Complaint.category_predicted)).all()
    department_rows = db.execute(select(Complaint.department, func.count()).group_by(Complaint.department)).all()
    status_category = db.execute(select(Complaint.status, Complaint.category_predicted, func.count()).group_by(Complaint.status, Complaint.category_predicted)).all()
    avg_resolution = db.scalar(select(func.avg(Complaint.resolution_hours_actual)).where(Complaint.resolution_hours_actual.is_not(None)))
    feedback_rows = db.execute(select(Feedback.rating, func.count()).group_by(Feedback.rating)).all()
    return {
        "complaint_count": total,
        "status_counts": {str(k): int(v) for k, v in status_rows},
        "category_counts": {str(k): int(v) for k, v in category_rows if k is not None},
        "department_counts": {str(k): int(v) for k, v in department_rows if k is not None},
        "status_category_counts": {str(status): {str(cat): int(n) for st, cat, n in status_category if st == status and cat is not None} for status, _cat, _n in status_category},
        "average_actual_resolution_hours": round(float(avg_resolution), 2) if avg_resolution is not None else None,
        "feedback": {"positive": sum(n for r, n in feedback_rows if r >= 4), "neutral": sum(n for r, n in feedback_rows if r == 3), "negative": sum(n for r, n in feedback_rows if r <= 2), "total": sum(n for _r, n in feedback_rows)},
    }


@router.get("/admin/feedback")
def admin_feedback(user: User = Depends(require_roles("admin")), db: Session = Depends(get_db)):
    rows = db.execute(select(Feedback, Complaint, User).join(Complaint, Feedback.complaint_id == Complaint.id).join(User, Feedback.citizen_id == User.id).order_by(Feedback.created_at.desc())).all()
    return [{"id": feedback.id, "complaint_id": complaint.id, "ticket_number": complaint.ticket_number, "citizen_name": citizen.name, "rating": feedback.rating, "comment": feedback.comment, "created_at": feedback.created_at} for feedback, complaint, citizen in rows]


@router.get("/notifications", response_model=list[NotificationOut])
def notifications(user: User = Depends(current_user), db: Session = Depends(get_db)):
    return db.scalars(select(Notification).where(Notification.user_id == user.id).order_by(Notification.created_at.desc()).limit(100)).all()


@router.put("/notifications/{notification_id}/read")
def mark_notification_read(notification_id: int, user: User = Depends(current_user), db: Session = Depends(get_db)):
    item = db.get(Notification, notification_id)
    if item is None or item.user_id != user.id: raise HTTPException(404, "Notification not found.")
    item.is_read = True; db.commit(); return {"success": True}


@router.post("/complaints/{complaint_id}/feedback", response_model=FeedbackOut, status_code=201)
def create_feedback(complaint_id: int, payload: FeedbackCreate, user: User = Depends(require_roles("citizen")), db: Session = Depends(get_db)):
    complaint = db.get(Complaint, complaint_id)
    if complaint is None or complaint.citizen_id != user.id: raise HTTPException(404, "Complaint not found.")
    if complaint.status not in {"resolved", "rejected", "closed"}: raise HTTPException(409, "Feedback can be submitted after resolution or rejection.")
    if db.scalar(select(Feedback.id).where(Feedback.complaint_id == complaint_id)) is not None: raise HTTPException(409, "Feedback has already been submitted for this complaint.")
    feedback = Feedback(complaint_id=complaint_id, citizen_id=user.id, rating=payload.rating, comment=payload.comment)
    db.add(feedback); db.commit(); db.refresh(feedback); return feedback


@router.post("/complaints/{complaint_id}/reminder", status_code=201)
def remind_officer(complaint_id: int, user: User = Depends(require_roles("citizen")), db: Session = Depends(get_db)):
    complaint = db.get(Complaint, complaint_id)
    if complaint is None or complaint.citizen_id != user.id:
        raise HTTPException(404, message("not_found", lang(user)))
    if complaint.status not in {"pending", "in_progress"}:
        raise HTTPException(409, "Reminders are only available for pending or in-progress complaints.")
    officer_ids = set()
    if complaint.assigned_officer_id:
        officer_ids.add(complaint.assigned_officer_id)
    elif complaint.assigned_department:
        officer_ids.update(db.scalars(select(User.id).where(User.role == "officer", User.department == complaint.assigned_department, User.active.is_(True))).all())
    if not officer_ids:
        raise HTTPException(409, "No active officer is assigned to this complaint yet.")
    for officer_id in officer_ids:
        notify_user(db, officer_id, "Citizen reminder", "नागरिक का अनुस्मारक", f"The citizen sent a reminder for complaint {complaint.ticket_number}.", f"नागरिक ने शिकायत {complaint.ticket_number} के लिए अनुस्मारक भेजा है।", complaint.id)
    db.commit()
    return {"success": True, "notified_officers": len(officer_ids)}


@router.get("/complaints/{complaint_id}/feedback", response_model=FeedbackOut | None)
def get_feedback(complaint_id: int, user: User = Depends(current_user), db: Session = Depends(get_db)):
    complaint = db.get(Complaint, complaint_id)
    if complaint is None or not complaint_visible_to(user, complaint): raise HTTPException(404, "Complaint not found.")
    return db.scalar(select(Feedback).where(Feedback.complaint_id == complaint_id))


@router.post("/admin/run-escalation-check")
def run_escalation_check(user: User = Depends(require_roles("admin")), db: Session = Depends(get_db)):
    now = utcnow(); overdue = db.scalars(select(Complaint).where(Complaint.status.in_(["pending", "in_progress", "reopened"]), Complaint.sla_due_at.is_not(None), Complaint.sla_due_at < now)).all(); tickets=[]
    for complaint in overdue:
        complaint.escalation_level = int(complaint.escalation_level or 0) + 1; complaint.escalated_at = now; complaint.priority = "Urgent" if complaint.escalation_level >= 2 else "High"; complaint.status_note = "Automatically escalated because the SLA deadline was exceeded."
        notify_user(db, complaint.citizen_id, "Complaint escalated", "शिकायत एस्केलेट हुई", f"Complaint {complaint.ticket_number} exceeded its SLA and was escalated.", f"आपकी शिकायत {complaint.ticket_number} की SLA समय-सीमा पार हो गई है और उसे एस्केलेट किया गया है।", complaint.id); tickets.append(complaint.ticket_number)
    db.commit(); return {"checked_at": now, "escalated_count": len(tickets), "tickets": tickets}


@router.post("/dev/seed-demo-users")
def seed_demo_users(db: Session = Depends(get_db)):
    if get_settings().environment.lower() not in {"development", "dev", "local"}: raise HTTPException(404, "Not found.")
    demo = [("+919999000001", "admin", None, "Admin", "admin@example.com"), ("+919999000002", "officer", "Water Supply Department", "Water Officer", "water@example.com"), ("+919999000003", "officer", "Road Department", "Road Officer", "road@example.com")]
    result=[]
    for mobile, role, department, name, email in demo:
        u=db.scalar(select(User).where(User.mobile==mobile))
        if u is None:
            u=User(mobile=mobile, password_hash=hash_password("Demo@12345"), role=role, department=department, name=name, email=email, preferred_language="en", profile_complete=True); db.add(u); db.flush()
        elif not u.password_hash:
            u.password_hash = hash_password("Demo@12345")
        result.append({"id":u.id,"mobile":u.mobile,"role":u.role,"department":u.department})
    db.commit(); return {"users":result}
