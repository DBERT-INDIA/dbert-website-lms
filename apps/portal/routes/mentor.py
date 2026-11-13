"""
routes/mentor.py - Mentor Portal & Availability Routing Blueprint
Fulfills Phase 23 (Monolith Modularization) of INTERNSHIPPORTAL4_LOCAL_AI_AGENT_MASTER_PLAN.md

Endpoints:
- POST /mentors/slots/<int:slot_id>/book
- POST /mentors/slots/<int:slot_id>/cancel
"""
from flask import Blueprint, jsonify, request
from services.auth_service import AuthService
from app import (
    get_db, current_intern, is_enrolled_or_accepted,
    check_mentor_pacing, log_error
)

mentor_bp = Blueprint("mentor", __name__)


@mentor_bp.route("/mentors/slots/<int:slot_id>/book", methods=["POST"])
def intern_book_slot(slot_id):
    """Enrolls an active intern into a mentor session with group capacity of up to 30 interns."""
    with get_db() as conn:
        intern = AuthService.current_intern(conn)
    if not intern:
        return jsonify({"status": "error", "message": "Authentication required"}), 401
    if not is_enrolled_or_accepted(intern["email"]):
        return jsonify({"status": "error", "message": "Internship enrollment required to book mentor sessions."}), 403

    try:
        with get_db() as conn:
            # Check if already booked
            already = conn.execute(
                "SELECT 1 FROM mentor_session_bookings WHERE slot_id = ? AND intern_id = ? AND status = 'booked'",
                (slot_id, intern["id"])
            ).fetchone()
            if already:
                return jsonify({"status": "error", "message": "You have already reserved a seat in this mentorship session."}), 400

            meeting_link = f"https://meet.google.com/dbert-mentor-slot-{slot_id}"
            res = conn.execute(
                "UPDATE mentor_availability_slots "
                "SET seats_booked = seats_booked + 1, "
                "    is_booked = CASE WHEN seats_booked + 1 >= COALESCE(capacity, 30) THEN 1 ELSE 0 END "
                "WHERE id = ? AND seats_booked < COALESCE(capacity, 30)",
                (slot_id,)
            )
            if res.rowcount == 0:
                return jsonify({"status": "error", "message": "This session has reached its full capacity of 30 interns."}), 400

            conn.execute(
                "INSERT INTO mentor_session_bookings (slot_id, intern_id, meeting_link, status) VALUES (?, ?, ?, 'booked')",
                (slot_id, intern["id"], meeting_link)
            )
            conn.commit()

        return jsonify({
            "status": "success",
            "message": "Seat reserved successfully in group mentorship session!",
            "meeting_link": meeting_link
        })
    except Exception as e:
        log_error("intern-book-slot", e)
        return jsonify({"status": "error", "message": "Failed to book mentor slot"}), 500


@mentor_bp.route("/mentors/slots/<int:slot_id>/cancel", methods=["POST"])
def intern_cancel_slot(slot_id):
    """Cancels an intern's seat reservation and increments available seats."""
    with get_db() as conn:
        intern = AuthService.current_intern(conn)
    if not intern:
        return jsonify({"status": "error", "message": "Authentication required"}), 401

    try:
        with get_db() as conn:
            res = conn.execute(
                "UPDATE mentor_session_bookings SET status = 'cancelled' "
                "WHERE slot_id = ? AND intern_id = ? AND status = 'booked'",
                (slot_id, intern["id"])
            )
            if res.rowcount == 0:
                return jsonify({"status": "error", "message": "No active reservation found for this session."}), 404

            conn.execute(
                "UPDATE mentor_availability_slots "
                "SET seats_booked = CASE WHEN seats_booked > 0 THEN seats_booked - 1 ELSE 0 END, "
                "    is_booked = 0 "
                "WHERE id = ?",
                (slot_id,)
            )
            conn.commit()

        return jsonify({
            "status": "success",
            "message": "Session reservation cancelled. Seat released back to cohort."
        })
    except Exception as e:
        log_error("intern-cancel-slot", e)
        return jsonify({"status": "error", "message": "Failed to cancel reservation"}), 500
