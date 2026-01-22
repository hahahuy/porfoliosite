"""Content service that abstracts JSON and CMS content sources"""
from typing import Dict, List, Any, Optional
from flask import current_app
from app.utils.content_loader import (
    load_profile as load_profile_json,
    load_projects as load_projects_json,
    load_skills as load_skills_json,
    load_experience as load_experience_json,
    get_project_by_id as get_project_by_id_json
)
from app.services.cms_service import CMSService


class ContentService:
    """Service for loading content from JSON or CMS with fallback"""
    
    def __init__(self, config: Dict[str, str]):
        self.config = config
        self.content_source = config.get('CONTENT_SOURCE', 'json')
        self.cms_service = CMSService(config)
    
    def _should_use_cms(self) -> bool:
        """Check if CMS should be used based on configuration"""
        return self.content_source in ['cms', 'cms_with_json_fallback'] and self.cms_service.is_available()
    
    def get_profile(self) -> Dict[str, Any]:
        """Get profile, trying CMS first if configured, then falling back to JSON"""
        if self._should_use_cms():
            profile = self.cms_service.get_profile()
            if profile:
                return profile
        
        # Fallback to JSON
        try:
            return load_profile_json()
        except Exception as e:
            current_app.logger.error(f"Error loading profile from JSON: {e}")
            return {}
    
    def get_projects(self) -> List[Dict[str, Any]]:
        """Get projects, trying CMS first if configured, then falling back to JSON"""
        if self._should_use_cms():
            projects = self.cms_service.get_projects()
            if projects is not None:
                return projects
        
        # Fallback to JSON
        try:
            return load_projects_json()
        except Exception as e:
            current_app.logger.error(f"Error loading projects from JSON: {e}")
            return []
    
    def get_skills(self) -> List[str]:
        """Get skills, trying CMS first if configured, then falling back to JSON"""
        if self._should_use_cms():
            skills = self.cms_service.get_skills()
            if skills is not None:
                return skills
        
        # Fallback to JSON
        try:
            return load_skills_json()
        except Exception as e:
            current_app.logger.error(f"Error loading skills from JSON: {e}")
            return []
    
    def get_experience(self) -> List[Dict[str, Any]]:
        """Get experience, trying CMS first if configured, then falling back to JSON"""
        if self._should_use_cms():
            experience = self.cms_service.get_experience()
            if experience is not None:
                return experience
        
        # Fallback to JSON
        try:
            return load_experience_json()
        except Exception as e:
            current_app.logger.error(f"Error loading experience from JSON: {e}")
            return []
    
    def get_project_by_id(self, project_id: int) -> Optional[Dict[str, Any]]:
        """Get a specific project by ID"""
        # Try CMS first if configured
        if self._should_use_cms():
            projects = self.cms_service.get_projects()
            if projects:
                project = next((p for p in projects if p.get('id') == project_id), None)
                if project:
                    return project
        
        # Fallback to JSON
        try:
            return get_project_by_id_json(project_id)
        except Exception as e:
            current_app.logger.error(f"Error loading project {project_id} from JSON: {e}")
            return None
