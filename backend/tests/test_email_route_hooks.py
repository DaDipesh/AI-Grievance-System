from datetime import timedelta
import unittest
from unittest.mock import patch

from fastapi import BackgroundTasks
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base
from app.models import Complaint, ComplaintDraft, User
from app.routes import create_complaint, update_complaint_status, utcnow
from app.schemas import ComplaintCreate, ComplaintStatusUpdate


class EmailRouteHookTests(unittest.TestCase):
    def setUp(self):
        engine = create_engine(
            "sqlite://",
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
        )
        Base.metadata.create_all(engine)
        self.addCleanup(engine.dispose)
        self.Session = sessionmaker(bind=engine, expire_on_commit=False)
        self.db = self.Session()
        self.addCleanup(self.db.close)

        self.citizen = User(
            mobile="+919000000001", role="citizen", name="Asha Citizen",
            email="asha@example.test", preferred_language="en", active=True,
        )
        self.admin = User(
            mobile="+919000000002", role="admin", name="Test Admin",
            email="admin@example.test", preferred_language="en", active=True,
        )
        self.db.add_all([self.citizen, self.admin])
        self.db.commit()

    def add_complaint(self, status="pending"):
        complaint = Complaint(
            ticket_number="GRV-TEST-1", citizen_id=self.citizen.id,
            complaint_text="Water supply is unavailable in my area.",
            status=status, updated_at=utcnow(), created_at=utcnow(),
        )
        self.db.add(complaint)
        self.db.commit()
        return complaint

    def test_submission_queues_one_email_after_commit_and_retry_does_not_queue_again(self):
        token = "test-preview-token"
        payload = ComplaintCreate(
            complaint_text="Water supply is unavailable in my area.",
            city="Bhopal", preview_token=token,
        )
        ai_result = {
            "category": "Water Supply", "category_source": "Rule-Based",
            "severity": "Medium", "priority": "Medium",
            "department": "Water Supply Department", "team": "Water Supply Team",
            "routing_status": "Success", "resolution_hours": 24.0,
            "resolution_days": 1.0, "duplicate_result": {}, "response": "Received",
        }
        draft = ComplaintDraft(
            token=token, citizen_id=self.citizen.id,
            payload_json=payload.model_dump(exclude={"preview_token"}),
            ai_json=ai_result, ticket_number="GRV-TEST-1",
            expires_at=utcnow() + timedelta(minutes=20),
        )
        self.db.add(draft)
        self.db.commit()

        tasks = BackgroundTasks()
        with patch("app.routes._run_ai", return_value=ai_result):
            created = create_complaint(payload, tasks, self.citizen, self.db)
            retried = create_complaint(payload, tasks, self.citizen, self.db)

        self.assertEqual(created.id, retried.id)
        self.assertEqual(len(tasks.tasks), 1)
        self.assertEqual(tasks.tasks[0].args[0], "submitted")
        self.assertEqual(created.status, "pending")

    def test_status_transition_emails_only_for_first_in_progress_and_resolved_changes(self):
        complaint = self.add_complaint()

        in_progress_tasks = BackgroundTasks()
        update_complaint_status(
            complaint.id, ComplaintStatusUpdate(status="in_progress"),
            in_progress_tasks, self.admin, self.db,
        )
        self.assertEqual(len(in_progress_tasks.tasks), 1)
        self.assertEqual(in_progress_tasks.tasks[0].args[0], "in_progress")

        repeated_tasks = BackgroundTasks()
        update_complaint_status(
            complaint.id, ComplaintStatusUpdate(status="in_progress"),
            repeated_tasks, self.admin, self.db,
        )
        self.assertEqual(len(repeated_tasks.tasks), 0)

        resolved_tasks = BackgroundTasks()
        with patch("training.data_collector.save_verified_complaint"):
            update_complaint_status(
                complaint.id, ComplaintStatusUpdate(status="resolved"),
                resolved_tasks, self.admin, self.db,
            )
        self.assertEqual(len(resolved_tasks.tasks), 1)
        self.assertEqual(resolved_tasks.tasks[0].args[0], "resolved")

        repeated_resolved_tasks = BackgroundTasks()
        update_complaint_status(
            complaint.id, ComplaintStatusUpdate(status="resolved"),
            repeated_resolved_tasks, self.admin, self.db,
        )
        self.assertEqual(len(repeated_resolved_tasks.tasks), 0)

    def test_rejected_transition_does_not_queue_email(self):
        complaint = self.add_complaint()
        tasks = BackgroundTasks()
        update_complaint_status(
            complaint.id, ComplaintStatusUpdate(status="rejected"),
            tasks, self.admin, self.db,
        )
        self.assertEqual(len(tasks.tasks), 0)


if __name__ == "__main__":
    unittest.main()
