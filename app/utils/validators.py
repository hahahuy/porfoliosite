"""Input validation utilities"""
from urllib.parse import urlparse
from typing import Tuple, Optional


def validate_proxy_path(path: str) -> Tuple[bool, Optional[str]]:
    """
    Validate proxy path to prevent SSRF attacks.
    
    Args:
        path: The path to validate
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    if '..' in path:
        return False, "Path traversal detected"
    
    if path.startswith('/'):
        return False, "Path cannot start with /"
    
    if '//' in path:
        return False, "Double slashes not allowed"
    
    return True, None


def validate_url(url: str, allowed_domains: list) -> Tuple[bool, Optional[str]]:
    """
    Validate URL to ensure it's from allowed domains.
    
    Args:
        url: The URL to validate
        allowed_domains: List of allowed domain names
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        parsed = urlparse(url)
        
        if parsed.scheme not in ['http', 'https']:
            return False, "Only HTTP and HTTPS schemes allowed"
        
        if parsed.netloc not in allowed_domains:
            return False, f"Domain not allowed: {parsed.netloc}"
        
        return True, None
    except Exception as e:
        return False, f"Invalid URL: {str(e)}"


def validate_email(email: str) -> bool:
    """
    Basic email validation.
    
    Args:
        email: Email address to validate
    
    Returns:
        True if valid, False otherwise
    """
    if not email or '@' not in email:
        return False
    
    parts = email.split('@')
    if len(parts) != 2:
        return False
    
    if not parts[0] or not parts[1]:
        return False
    
    if '.' not in parts[1]:
        return False
    
    return True


def sanitize_string(value: str, max_length: int = 1000) -> str:
    """
    Sanitize string input.
    
    Args:
        value: String to sanitize
        max_length: Maximum allowed length
    
    Returns:
        Sanitized string
    """
    if not value:
        return ''
    
    # Remove null bytes
    value = value.replace('\x00', '')
    
    # Truncate if too long
    if len(value) > max_length:
        value = value[:max_length]
    
    return value.strip()
