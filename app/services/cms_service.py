"""Headless CMS integration service"""
from typing import Dict, List, Any, Optional
from flask import current_app
from app.utils.cms_client import create_cms_client, CMSClient


class CMSService:
    """Service for interacting with Headless CMS"""
    
    def __init__(self, config: Dict[str, str]):
        self.config = config
        self.client: Optional[CMSClient] = None
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize CMS client based on configuration"""
        try:
            self.client = create_cms_client(self.config)
        except Exception as e:
            current_app.logger.warning(f"Failed to initialize CMS client: {e}")
            self.client = None
    
    def is_available(self) -> bool:
        """Check if CMS is configured and available"""
        return self.client is not None
    
    def get_profile(self) -> Optional[Dict[str, Any]]:
        """Get profile from CMS"""
        if not self.is_available():
            return None
        
        try:
            return self.client.get_profile()
        except Exception as e:
            current_app.logger.error(f"Error fetching profile from CMS: {e}")
            return None
    
    def get_projects(self) -> Optional[List[Dict[str, Any]]]:
        """Get projects from CMS"""
        if not self.is_available():
            return None
        
        try:
            return self.client.get_projects()
        except Exception as e:
            current_app.logger.error(f"Error fetching projects from CMS: {e}")
            return None
    
    def get_skills(self) -> Optional[List[str]]:
        """Get skills from CMS"""
        if not self.is_available():
            return None
        
        try:
            return self.client.get_skills()
        except Exception as e:
            current_app.logger.error(f"Error fetching skills from CMS: {e}")
            return None
    
    def get_experience(self) -> Optional[List[Dict[str, Any]]]:
        """Get experience from CMS"""
        if not self.is_available():
            return None
        
        try:
            return self.client.get_experience()
        except Exception as e:
            current_app.logger.error(f"Error fetching experience from CMS: {e}")
            return None
