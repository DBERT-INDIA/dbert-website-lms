from typing import Dict, Any
import logging

def dispatch_event(event_type: str, payload: Dict[str, Any]) -> bool:
    """
    Consumes outbox events and dispatches actual emails/notifications.
    Returns True on success, False/Exception on failure.
    """
    # Import app.py functions locally to avoid circular dependencies
    try:
        from app import (
            send_application_received_email,
            send_status_update_email,
            send_enrollment_confirmation_email,
            notify_course_payment_verified,
            send_paid_payment_rejected_email,
            notify_cert_issued,
            app_logger,
            send_email_async
        )
    except ImportError as e:
        logging.error(f"Failed to import app email handlers: {e}")
        return False
        
    app_logger.info(f"[dispatch] Processing outbox event: {event_type} | payload: {payload.keys()}")
    
    email = payload.get("email")
    name = payload.get("name", "Candidate")
    domain = payload.get("domain", "DBERT Internship")
    
    if not email:
        app_logger.warning(f"No email in payload for {event_type}, skipping.")
        return True

    try:
        if event_type == "application.submitted":
            send_application_received_email(name, email, domain)
            
        elif event_type == "application.selected":
            send_status_update_email(name, email, domain, "Selected")
            
        elif event_type == "application.rejected":
            send_status_update_email(name, email, domain, "Rejected")
            
        elif event_type == "enrollment.created":
            send_enrollment_confirmation_email(name, email, domain, joining_date=None)
            
        elif event_type == "payment.accepted":
            notify_course_payment_verified(name, email, domain, is_portal_course=True, link_url="https://internship.dbert.online/portal")
            
        elif event_type == "payment.rejected":
            send_paid_payment_rejected_email(name, email, domain)
            
        elif event_type == "certificate.issued":
            cert_url = f"https://internship.dbert.online/cert/{payload.get('certificate_id', '')}"
            notify_cert_issued(name, email, payload.get("title", domain), cert_url)
            
        elif event_type == "task.reviewed":
            decision = payload.get("decision", "reviewed")
            coins = payload.get("coins_awarded", 0)
            subject = f"DBERT Task Update: {decision.title()}"
            body = f"<p>Your task submission was <b>{decision}</b>. You were awarded {coins} coins.</p>"
            send_email_async(email, subject, body, name)
            
        elif event_type == "mentor.assigned":
            subject = "A Mentor has been assigned to your internship!"
            body = f"<p>A mentor has been assigned for your {domain} track. Check your portal for details!</p>"
            send_email_async(email, subject, body, name)
            
        else:
            app_logger.info(f"No specific handler for event {event_type}, marking as processed.")
            
        return True
        
    except Exception as e:
        app_logger.error(f"[dispatch] Failed to process {event_type}: {e}")
        return False
