"""Content service tests"""
import pytest
from app.services.content_service import ContentService
from app.utils.content_loader import load_profile, load_projects, load_skills


def test_content_service_loads_json(client, app):
    """Test content service loads from JSON"""
    with app.app_context():
        config = app.config
        service = ContentService(config)
        
        profile = service.get_profile()
        assert profile is not None
        assert 'name' in profile
        
        projects = service.get_projects()
        assert isinstance(projects, list)
        
        skills = service.get_skills()
        assert isinstance(skills, list)


def test_content_service_fallback_to_json(client, app):
    """Test content service falls back to JSON when CMS unavailable"""
    with app.app_context():
        config = app.config.copy()
        config['CONTENT_SOURCE'] = 'cms_with_json_fallback'
        config['CMS_TYPE'] = 'none'
        
        service = ContentService(config)
        
        # Should fallback to JSON
        profile = service.get_profile()
        assert profile is not None
        assert 'name' in profile
