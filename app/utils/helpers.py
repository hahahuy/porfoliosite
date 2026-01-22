"""General helper functions"""
from flask import request
from typing import Optional


def get_client_ip() -> str:
    """
    Get client IP address from request.
    Handles proxy headers (X-Forwarded-For, X-Real-IP).
    
    Returns:
        Client IP address
    """
    if request.headers.get('X-Forwarded-For'):
        # X-Forwarded-For can contain multiple IPs, take the first one
        return request.headers.get('X-Forwarded-For').split(',')[0].strip()
    elif request.headers.get('X-Real-IP'):
        return request.headers.get('X-Real-IP')
    else:
        return request.remote_addr or 'unknown'


def format_error_message(error: Exception) -> str:
    """
    Format error message for logging/display.
    
    Args:
        error: Exception instance
    
    Returns:
        Formatted error message
    """
    error_type = type(error).__name__
    error_msg = str(error)
    return f"{error_type}: {error_msg}"
