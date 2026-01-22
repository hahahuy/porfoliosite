"""JSON content loader utility"""
import json
from pathlib import Path
from typing import Dict, List, Any


def load_content(filename: str) -> Any:
    """
    Load content from a JSON file in the app/content directory.
    
    Args:
        filename: Name of the JSON file (e.g., 'profile.json')
    
    Returns:
        Parsed JSON content (dict or list)
    
    Raises:
        FileNotFoundError: If the file doesn't exist
        json.JSONDecodeError: If the file contains invalid JSON
    """
    content_path = Path(__file__).parent.parent / 'content' / filename
    
    if not content_path.exists():
        raise FileNotFoundError(f"Content file not found: {content_path}")
    
    with open(content_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def load_profile() -> Dict[str, Any]:
    """Load profile information"""
    return load_content('profile.json')


def load_projects() -> List[Dict[str, Any]]:
    """Load projects list"""
    return load_content('projects.json')


def load_skills() -> List[str]:
    """Load skills list"""
    return load_content('skills.json')


def load_experience() -> List[Dict[str, Any]]:
    """Load experience entries"""
    return load_content('experience.json')


def get_project_by_id(project_id: int) -> Dict[str, Any] | None:
    """
    Get a specific project by ID.
    
    Args:
        project_id: The project ID to retrieve
    
    Returns:
        Project dictionary or None if not found
    """
    projects = load_projects()
    return next((p for p in projects if p.get('id') == project_id), None)
