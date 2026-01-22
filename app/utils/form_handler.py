"""Contact form validation and database storage"""
from datetime import datetime
from typing import Dict, Tuple, Optional
from flask import current_app
from app.utils.validators import validate_email, sanitize_string
from app.utils.helpers import get_client_ip
from app.database.models import ContactSubmission
from app.database.db import db


def validate_contact_form(data: Dict[str, str]) -> Tuple[bool, Optional[str]]:
    """
    Validate contact form data.
    
    Args:
        data: Dictionary with form fields (name, email, message)
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    name = data.get('name', '').strip()
    email = data.get('email', '').strip()
    message = data.get('message', '').strip()
    
    if not name:
        return False, "Name is required"
    
    if len(name) > 100:
        return False, "Name is too long (max 100 characters)"
    
    if not email:
        return False, "Email is required"
    
    if not validate_email(email):
        return False, "Invalid email address"
    
    if len(email) > 255:
        return False, "Email is too long"
    
    if not message:
        return False, "Message is required"
    
    if len(message) > 5000:
        return False, "Message is too long (max 5000 characters)"
    
    return True, None


def save_contact_submission(name: str, email: str, message: str) -> ContactSubmission:
    """
    Save contact form submission to database.
    
    Args:
        name: Contact name
        email: Contact email
        message: Contact message
    
    Returns:
        ContactSubmission instance
    """
    # Sanitize inputs
    name = sanitize_string(name, max_length=100)
    email = sanitize_string(email, max_length=255)
    message = sanitize_string(message, max_length=5000)
    
    # Get client IP
    ip_address = get_client_ip()
    
    # Create submission
    submission = ContactSubmission(
        name=name,
        email=email,
        message=message,
        ip_address=ip_address,
        created_at=datetime.utcnow()
    )
    
    db.session.add(submission)
    db.session.commit()
    
    return submission
