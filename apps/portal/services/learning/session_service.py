"""
Session Resume and Streaming Safety Service for Guided Learning 2.0.
Manages session persistence, browser reload resilience, turn idempotency keys,
and atomic commit lifecycle preventing partial state mutation during streaming.
"""
import uuid
import json
from datetime import datetime, timezone
from typing import Optional, Dict, Any, Tuple
from services.database.connection_pool import transaction
from services.learning.learning_models import LearningSession, Concept
from services.learning.concept_service import ConceptService
from services.learning.mastery_policy import MasteryPolicy
from services.learning.evaluator import StructuredEvaluator, EvaluationResult
from services.learning.adaptive_engine import AdaptiveActionEngine, NextActionRecommendation
from services.learning.spaced_review import SpacedReviewScheduler

class SessionResumeError(Exception):
    """Raised when resuming a session fails authorization or data integrity."""
    pass

class DuplicateTurnError(Exception):
    """Raised when an existing submission key is reused for a different answer."""


class SessionChangedError(SessionResumeError):
    """Raised when another turn advanced the lesson during evaluation."""

class LearningSessionService:
    @staticmethod
    def get_or_create_session(
        conn,
        student_id: int,
        course_id: int,
        subtopic_id: Optional[int] = None
    ) -> LearningSession:
        """
        Retrieves active session for student and course, or initializes a new persistent session.
        """
        # Find active session
        row = conn.execute(
            """
            SELECT * FROM gl_learning_sessions
            WHERE student_id = ? AND course_id = ? AND status = 'active'
            ORDER BY updated_at DESC LIMIT 1
            """,
            (student_id, course_id)
        ).fetchone()

        now_iso = datetime.now(timezone.utc).isoformat()

        if row:
            # Update heartbeat
            conn.execute(
                "UPDATE gl_learning_sessions SET last_heartbeat_at = ?, updated_at = ? WHERE session_id = ?",
                (now_iso, now_iso, row["session_id"])
            )
            conn.commit()
            return LearningSessionService._row_to_session(row)

        # Determine initial concept
        initial_concept_id = None
        if subtopic_id:
            c = ConceptService.get_concept_by_subtopic(conn, subtopic_id)
            if c:
                initial_concept_id = c.concept_id

        if not initial_concept_id:
            # Fallback to first concept of course domain
            course = conn.execute("SELECT domain FROM courses WHERE id = ?", (course_id,)).fetchone()
            domain = course["domain"] if course else "AI Agent Development"
            domain_concepts = ConceptService.list_concepts_for_domain(conn, domain)
            if domain_concepts:
                initial_concept_id = domain_concepts[0].concept_id

        new_session_id = f"gl_sess_{uuid.uuid4().hex[:16]}"
        conn.execute(
            """
            INSERT INTO gl_learning_sessions (
                session_id, student_id, course_id, subtopic_id,
                current_concept_id, current_action, action_state_json,
                idempotency_key, status, last_heartbeat_at, created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, 'EXPLAIN', '{}', NULL, 'active', ?, ?, ?)
            RETURNING session_id
            """,
            (new_session_id, student_id, course_id, subtopic_id, initial_concept_id, now_iso, now_iso, now_iso)
        ).fetchone()
        conn.commit()

        # Record session_started event
        if initial_concept_id:
            MasteryPolicy._record_event(
                conn, student_id, initial_concept_id, new_session_id,
                "session_started", {"course_id": course_id, "subtopic_id": subtopic_id}
            )

        return LearningSession(
            session_id=new_session_id,
            student_id=student_id,
            course_id=course_id,
            subtopic_id=subtopic_id,
            current_concept_id=initial_concept_id,
            current_action="EXPLAIN",
            action_state={},
            status="active",
            last_heartbeat_at=now_iso,
            created_at=now_iso,
            updated_at=now_iso
        )

    @staticmethod
    def resume_session_state(conn, session_id: str, student_id: int) -> Dict[str, Any]:
        """
        Builds a complete, idempotent resume payload for returning learners or page reloads.
        """
        row = conn.execute(
            "SELECT * FROM gl_learning_sessions WHERE session_id = ? AND student_id = ?",
            (session_id, student_id)
        ).fetchone()

        if not row:
            raise SessionResumeError(f"Session {session_id} not found for student {student_id}")

        session = LearningSessionService._row_to_session(row)
        now_iso = datetime.now(timezone.utc).isoformat()

        # Update heartbeat
        conn.execute(
            "UPDATE gl_learning_sessions SET last_heartbeat_at = ? WHERE session_id = ?",
            (now_iso, session_id)
        )
        conn.commit()

        # Fetch current concept details
        concept_data = None
        mastery_data = None
        if session.current_concept_id:
            concept = ConceptService.get_concept(conn, session.current_concept_id)
            if concept:
                concept_data = concept.to_dict()
                mastery = MasteryPolicy.get_or_create_mastery(conn, student_id, concept.concept_id)
                mastery_data = mastery.to_dict()

        # Fetch last completed event
        last_event_row = conn.execute(
            """
            SELECT * FROM gl_learning_events
            WHERE session_id = ? ORDER BY id DESC LIMIT 1
            """,
            (session_id,)
        ).fetchone()
        last_event = dict(last_event_row) if last_event_row else None
        if last_event and last_event.get("payload_json"):
            try:
                last_event["payload"] = json.loads(last_event["payload_json"])
            except Exception:
                pass

        # Record session_resumed event
        if session.current_concept_id:
            MasteryPolicy._record_event(
                conn, student_id, session.current_concept_id, session_id,
                "session_resumed", {"resumed_at": now_iso}
            )

        # Check due reviews
        due_reviews = SpacedReviewScheduler.get_due_reviews_for_student(conn, student_id)

        return {
            "session": session.to_dict(),
            "concept": concept_data,
            "mastery": mastery_data,
            "last_event": last_event,
            "due_reviews_count": len(due_reviews),
            "due_reviews": due_reviews[:3],
            "resumed_at": now_iso
        }

    @staticmethod
    def process_turn_atomic(
        conn,
        session_id: str,
        student_id: int,
        student_input: str,
        idempotency_key: Optional[str] = None,
        llm_caller=None,
    ) -> Dict[str, Any]:
        """Evaluate outside the write lock, then persist the entire turn or roll it back."""
        if idempotency_key is not None and (
            not isinstance(idempotency_key, str) or not 1 <= len(idempotency_key) <= 128
        ):
            raise ValueError("The idempotency key must contain 1 to 128 characters.")

        session = LearningSessionService._load_owned_session(conn, session_id, student_id)
        replay = LearningSessionService._replay_turn(conn, session, student_input, idempotency_key)
        if replay is not None:
            return replay

        concept = ConceptService.get_concept(conn, session.current_concept_id)
        if concept is None:
            raise SessionResumeError("This session has no active lesson concept.")

        evaluation = StructuredEvaluator.evaluate(
            student_response=student_input, concept=concept, llm_caller=llm_caller
        )
        with transaction(conn):
            # UPDATE locks the existing session in PostgreSQL and opens a write transaction in SQLite.
            conn.execute(
                "UPDATE gl_learning_sessions SET updated_at = updated_at WHERE session_id = ? AND student_id = ?",
                (session_id, student_id),
            )
            session = LearningSessionService._load_owned_session(conn, session_id, student_id)
            replay = LearningSessionService._replay_turn(conn, session, student_input, idempotency_key)
            if replay is not None:
                return replay
            if session.current_concept_id != concept.concept_id:
                raise SessionChangedError("Your active concept changed. Reload before retrying.")

            now = datetime.now(timezone.utc).isoformat()
            # Separate sessions for this learner share the same mastery and review records.
            conn.execute(
                """INSERT INTO gl_student_learning_profile (student_id, created_at, updated_at)
                   VALUES (?, ?, ?) ON CONFLICT(student_id) DO UPDATE SET student_id = excluded.student_id
                   RETURNING student_id""",
                (student_id, now, now),
            )
            return LearningSessionService._save_turn(
                conn, session, concept, student_input, idempotency_key, evaluation, now
            )

    @staticmethod
    def _load_owned_session(conn, session_id, student_id):
        row = conn.execute(
            "SELECT * FROM gl_learning_sessions WHERE session_id = ? AND student_id = ?",
            (session_id, student_id),
        ).fetchone()
        if row is None:
            raise SessionResumeError("Learning session not found.")
        return LearningSessionService._row_to_session(row)

    @staticmethod
    def _replay_turn(conn, session, student_input, idempotency_key):
        if idempotency_key is None:
            return None
        row = conn.execute(
            """SELECT student_input, evaluation_json, recommendation_json, result_json
               FROM gl_learning_turns WHERE student_id = ? AND session_id = ? AND idempotency_key = ?""",
            (session.student_id, session.session_id, idempotency_key),
        ).fetchone()
        if row is None:
            return None
        if row["student_input"] != student_input:
            raise DuplicateTurnError("This submission key already belongs to a different answer.")
        if row["result_json"]:
            result = json.loads(row["result_json"])
        else:
            # Old turns retain their evaluation and recommendation even before result snapshots existed.
            recommendation = json.loads(row["recommendation_json"])
            result = {
                "session": session.to_dict(),
                "evaluation": json.loads(row["evaluation_json"]),
                "recommendation": recommendation,
                "action": recommendation.get("action"),
            }
        return {**result, "idempotent_replay": True}

    @staticmethod
    def _save_turn(conn, session, concept, student_input, idempotency_key, evaluation, now):
        student_id, session_id, concept_id = session.student_id, session.session_id, concept.concept_id
        evaluation_data = evaluation.to_dict()
        MasteryPolicy._record_event(
            conn, student_id, concept_id, session_id,
            "answer_submitted", {"input_length": len(student_input)}, commit=False
        )
        MasteryPolicy._record_event(
            conn, student_id, concept_id, session_id, "answer_evaluated", evaluation_data, commit=False
        )
        mastery, _ = MasteryPolicy.evaluate_and_update_mastery(
            conn, student_id, concept, evaluation, session_id, student_input, commit=False
        )
        due_reviews = SpacedReviewScheduler.get_due_reviews_for_student(conn, student_id)
        recommendation = AdaptiveActionEngine.select_next_action(
            conn=conn,
            student_id=student_id,
            concept=concept,
            mastery=mastery,
            latest_evaluation=evaluation,
            review_due=any(review["concept_id"] == concept_id for review in due_reviews),
        )
        if mastery.total_attempts <= 1:
            category = "NEW"
        elif evaluation.detected_misconceptions:
            category = "REMEDIATION"
        elif mastery.mastery_score >= 0.85:
            category = "MASTERY_VALIDATION"
        else:
            category = "REINFORCEMENT"
        next_review, interval = SpacedReviewScheduler.schedule_next_review(
            conn, student_id, concept_id, category, evaluation.correctness, commit=False
        )
        recommendation_data = recommendation.to_dict()
        action_state = {
            "evaluation": evaluation_data,
            "recommendation": recommendation_data,
            "next_review_at": next_review,
            "review_interval_days": interval,
        }
        if recommendation.action == "ADVANCE" and recommendation.next_concept_id:
            session.current_concept_id = recommendation.next_concept_id
        session.current_action = recommendation.action
        session.action_state = action_state
        session.idempotency_key = idempotency_key
        session.last_heartbeat_at = now
        session.updated_at = now

        result = {
            "session": session.to_dict(),
            "evaluation": evaluation_data,
            "mastery": mastery.to_dict(),
            "recommendation": recommendation_data,
            "next_review_at": next_review,
            "action": session.current_action,
            "action_state": action_state,
        }
        conn.execute(
            """INSERT INTO gl_learning_turns (
                turn_uuid, session_id, student_id, concept_id, idempotency_key,
                student_input, evaluation_json, recommendation_json, result_json,
                status, created_at, completed_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'completed', ?, ?)""",
            (
                str(uuid.uuid4()), session_id, student_id, concept_id, idempotency_key,
                student_input, json.dumps(evaluation_data), json.dumps(recommendation_data),
                json.dumps(result) if idempotency_key else None, now, now,
            ),
        )
        conn.execute(
            """UPDATE gl_learning_sessions
               SET current_concept_id = ?, current_action = ?, action_state_json = ?,
                   idempotency_key = ?, last_heartbeat_at = ?, updated_at = ?
               WHERE session_id = ? AND student_id = ?""",
            (
                session.current_concept_id, session.current_action, json.dumps(action_state),
                idempotency_key, now, now, session_id, student_id,
            ),
        )
        MasteryPolicy.update_student_profile(conn, student_id, commit=False)
        return result

    @staticmethod
    def _row_to_session(row) -> LearningSession:
        return LearningSession(
            session_id=row["session_id"],
            student_id=row["student_id"],
            course_id=row["course_id"],
            subtopic_id=row["subtopic_id"],
            current_concept_id=row["current_concept_id"],
            current_action=row["current_action"] or "EXPLAIN",
            action_state=json.loads(row["action_state_json"] or "{}"),
            idempotency_key=row["idempotency_key"],
            status=row["status"] or "active",
            last_heartbeat_at=row["last_heartbeat_at"],
            created_at=row["created_at"],
            updated_at=row["updated_at"]
        )
