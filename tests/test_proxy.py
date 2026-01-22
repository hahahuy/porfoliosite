"""Proxy functionality tests"""
import pytest
from unittest.mock import patch, Mock
from app.services.proxy_service import ProxyService


def test_proxy_path_validation(app):
    """Test proxy path validation"""
    with app.app_context():
        service = ProxyService('https://hahahuy.github.io/dg')
        
        # Invalid path with .. (should fail validation before making request)
        response, error = service.proxy_request('../etc/passwd')
        assert error is not None
        assert 'traversal' in error.lower() or 'invalid' in error.lower() or 'path' in error.lower()


def test_proxy_url_validation(app):
    """Test proxy URL validation"""
    with app.app_context():
        service = ProxyService('https://hahahuy.github.io/dg')
        
        # Valid path should pass validation (may fail on actual request, but validation should pass)
        response, error = service.proxy_request('test')
        # Error should be None (validation passed) or a request error, not a validation error
        # If error exists, it shouldn't be about path validation
        if error:
            assert 'traversal' not in error.lower()
            assert 'path' not in error.lower() or 'cannot start' not in error.lower()
