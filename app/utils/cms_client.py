"""Headless CMS API clients for Strapi, Contentful, and Sanity"""
import requests
from typing import Dict, List, Any, Optional
from flask import current_app


class CMSClient:
    """Base class for CMS clients"""
    
    def __init__(self, config: Dict[str, str]):
        self.config = config
    
    def get_profile(self) -> Dict[str, Any]:
        """Get profile information"""
        raise NotImplementedError
    
    def get_projects(self) -> List[Dict[str, Any]]:
        """Get projects list"""
        raise NotImplementedError
    
    def get_skills(self) -> List[str]:
        """Get skills list"""
        raise NotImplementedError
    
    def get_experience(self) -> List[Dict[str, Any]]:
        """Get experience entries"""
        raise NotImplementedError


class StrapiClient(CMSClient):
    """Strapi CMS client"""
    
    def __init__(self, config: Dict[str, str]):
        super().__init__(config)
        self.base_url = config.get('CMS_API_URL', '').rstrip('/')
        self.api_key = config.get('CMS_API_KEY', '')
        self.headers = {
            'Authorization': f'Bearer {self.api_key}' if self.api_key else '',
            'Content-Type': 'application/json'
        }
    
    def _get(self, endpoint: str) -> Dict[str, Any]:
        """Make GET request to Strapi API"""
        url = f"{self.base_url}/api/{endpoint}"
        response = requests.get(url, headers=self.headers, timeout=10)
        response.raise_for_status()
        return response.json()
    
    def get_profile(self) -> Dict[str, Any]:
        """Get profile from Strapi"""
        data = self._get('profile?populate=*')
        return data.get('data', {}).get('attributes', {})
    
    def get_projects(self) -> List[Dict[str, Any]]:
        """Get projects from Strapi"""
        data = self._get('projects?populate=*')
        items = data.get('data', [])
        return [item.get('attributes', {}) for item in items]
    
    def get_skills(self) -> List[str]:
        """Get skills from Strapi"""
        data = self._get('skills?populate=*')
        items = data.get('data', [])
        return [item.get('attributes', {}).get('name', '') for item in items]
    
    def get_experience(self) -> List[Dict[str, Any]]:
        """Get experience from Strapi"""
        data = self._get('experiences?populate=*')
        items = data.get('data', [])
        return [item.get('attributes', {}) for item in items]


class ContentfulClient(CMSClient):
    """Contentful CMS client"""
    
    def __init__(self, config: Dict[str, str]):
        super().__init__(config)
        self.space_id = config.get('CMS_SPACE_ID', '')
        self.environment = config.get('CMS_ENVIRONMENT', 'master')
        self.access_token = config.get('CMS_API_KEY', '')
        self.base_url = f"https://cdn.contentful.com/spaces/{self.space_id}/environments/{self.environment}"
        self.headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }
    
    def _get(self, endpoint: str) -> Dict[str, Any]:
        """Make GET request to Contentful API"""
        url = f"{self.base_url}/{endpoint}"
        response = requests.get(url, headers=self.headers, timeout=10)
        response.raise_for_status()
        return response.json()
    
    def get_profile(self) -> Dict[str, Any]:
        """Get profile from Contentful"""
        data = self._get('entries?content_type=profile&limit=1')
        items = data.get('items', [])
        if items:
            return items[0].get('fields', {})
        return {}
    
    def get_projects(self) -> List[Dict[str, Any]]:
        """Get projects from Contentful"""
        data = self._get('entries?content_type=project')
        return [item.get('fields', {}) for item in data.get('items', [])]
    
    def get_skills(self) -> List[str]:
        """Get skills from Contentful"""
        data = self._get('entries?content_type=skill')
        return [item.get('fields', {}).get('name', '') for item in data.get('items', [])]
    
    def get_experience(self) -> List[Dict[str, Any]]:
        """Get experience from Contentful"""
        data = self._get('entries?content_type=experience')
        return [item.get('fields', {}) for item in data.get('items', [])]


class SanityClient(CMSClient):
    """Sanity CMS client using GROQ"""
    
    def __init__(self, config: Dict[str, str]):
        super().__init__(config)
        self.project_id = config.get('CMS_PROJECT_ID', '')
        self.dataset = config.get('CMS_DATASET', 'production')
        self.api_key = config.get('CMS_API_KEY', '')
        self.base_url = f"https://{self.project_id}.api.sanity.io/v2021-10-21/data/query/{self.dataset}"
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
    
    def _query(self, groq_query: str) -> Dict[str, Any]:
        """Execute GROQ query"""
        params = {'query': groq_query}
        response = requests.get(self.base_url, params=params, headers=self.headers, timeout=10)
        response.raise_for_status()
        return response.json()
    
    def get_profile(self) -> Dict[str, Any]:
        """Get profile from Sanity"""
        query = '*[_type == "profile"][0]'
        result = self._query(query)
        return result.get('result', {})
    
    def get_projects(self) -> List[Dict[str, Any]]:
        """Get projects from Sanity"""
        query = '*[_type == "project"] | order(_createdAt desc)'
        result = self._query(query)
        return result.get('result', [])
    
    def get_skills(self) -> List[str]:
        """Get skills from Sanity"""
        query = '*[_type == "skill"] | order(name asc)'
        result = self._query(query)
        return [item.get('name', '') for item in result.get('result', [])]
    
    def get_experience(self) -> List[Dict[str, Any]]:
        """Get experience from Sanity"""
        query = '*[_type == "experience"] | order(startDate desc)'
        result = self._query(query)
        return result.get('result', [])


def create_cms_client(config: Dict[str, str]) -> Optional[CMSClient]:
    """
    Factory function to create appropriate CMS client based on configuration.
    
    Args:
        config: Configuration dictionary with CMS settings
    
    Returns:
        CMSClient instance or None if CMS_TYPE is 'none'
    """
    cms_type = config.get('CMS_TYPE', 'none').lower()
    
    if cms_type == 'strapi':
        return StrapiClient(config)
    elif cms_type == 'contentful':
        return ContentfulClient(config)
    elif cms_type == 'sanity':
        return SanityClient(config)
    elif cms_type == 'none':
        return None
    else:
        raise ValueError(f"Unknown CMS type: {cms_type}")
