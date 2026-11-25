"""Mentor booking, calendar and reserved-session workspace endpoints."""

from flask import Blueprint, Response, abort, flash, jsonify, redirect, request, url_for

from app import current_intern, current_mentor, current_staff, get_db, is_enrolled_or_accepted, log_error
from services.mentor_schedule import (
    BookingError,
    release_slot,
    reserve_slot,
    session_calendar,
    student_reservations,
    update_learner_question,
    update_session_details,
)


mentor_bp = Blueprint("mentor", __name__)


@mentor_bp.post("/mentors/slots/<int:slot_id>/book")
def intern_book_slot(slot_id):
    intern = current_intern()
    if not intern:
        return jsonify({"status": "error", "message": "Authentication required."}), 401
    if not is_enrolled_or_accepted(intern["email"]):
        return jsonify({"status": "error", "message": "Internship enrollment required to book mentor sessions."}), 403

    try:
        with get_db() as conn:
            meeting_link = reserve_slot(conn, intern_id=intern["id"], slot_id=slot_id)
    except BookingError as error:
        return jsonify({"status": "error", "message": str(error)}), error.status
    except Exception as error:
        log_error("intern-book-slot", error)
        return jsonify({"status": "error", "message": "Could not book this session."}), 500
    return jsonify({"status": "success", "message": "Seat reserved.", "meeting_link": meeting_link})


@mentor_bp.post("/mentors/slots/<int:slot_id>/cancel")
def intern_cancel_slot(slot_id):
    intern = current_intern()
    if not intern:
        return jsonify({"status": "error", "message": "Authentication required."}), 401

    try:
        with get_db() as conn:
            release_slot(conn, intern_id=intern["id"], slot_id=slot_id)
    except BookingError as error:
        return jsonify({"status": "error", "message": str(error)}), error.status
    except Exception as error:
        log_error("intern-cancel-slot", error)
        return jsonify({"status": "error", "message": "Could not cancel this reservation."}), 500
    return jsonify({"status": "success", "message": "Reservation cancelled and seat released."})


@mentor_bp.get("/mentors/slots/<int:slot_id>/calendar.ics")
def intern_mentor_calendar(slot_id):
    intern = current_intern()
    if not intern:
        abort(401)

    with get_db() as conn:
        bookings = student_reservations(conn, intern["id"], slot_id)
    if not bookings:
        abort(404)
    return Response(
        session_calendar(bookings[0]),
        content_type="text/calendar; charset=utf-8",
        headers={"Content-Disposition": f'attachment; filename="dbert-mentor-{slot_id}.ics"'},
    )


@mentor_bp.post("/mentors/slots/<int:slot_id>/question")
def intern_mentor_question(slot_id):
    intern = current_intern()
    if not intern:
        return redirect("/#signin", code=303)

    try:
        with get_db() as conn:
            update_learner_question(
                conn, intern_id=intern["id"], slot_id=slot_id, question=request.form.get("question", ""),
            )
        flash("Your question was saved for the mentor.", "success")
    except BookingError as error:
        if error.status == 404:
            abort(404)
        flash(str(error), "error")
    return redirect(url_for("intern_mentor_slots", _anchor=f"mentor-reservation-{slot_id}"), code=303)


@mentor_bp.post("/staff/mentor-slots/<int:slot_id>/details")
def staff_mentor_details(slot_id):
    staff = current_staff()
    mentor = current_mentor() if not staff else None
    if not staff and not mentor:
        abort(401)

    try:
        with get_db() as conn:
            update_session_details(
                conn, staff_id=staff["id"] if staff else None, mentor_id=mentor["id"] if mentor else None,
                slot_id=slot_id, agenda=request.form.get("agenda", ""),
                follow_up=request.form.get("follow_up", ""), meeting_link=request.form.get("meeting_link", ""),
            )
        flash("Session materials updated.", "success")
    except BookingError as error:
        if error.status == 404:
            abort(404)
        flash(str(error), "error")
    return redirect(url_for("staff_mentor_slots", _anchor=f"mentor-session-{slot_id}"), code=303)
