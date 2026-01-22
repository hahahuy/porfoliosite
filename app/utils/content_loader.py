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
    # Try multiple paths to handle different working directories
    base_paths = [
        Path(__file__).parent.parent / 'content' / filename,  # Relative to utils/
        Path.cwd() / 'app' / 'content' / filename,  # From project root
        Path(__file__).parent.parent.parent / 'app' / 'content' / filename,  # Alternative
    ]
    
    content_path = None
    for path in base_paths:
        if path.exists():
            content_path = path
            break
    
    if not content_path:
        # Try to find it by searching
        possible_paths = [str(p) for p in base_paths]
        raise FileNotFoundError(f"Content file not found: {filename}. Tried: {possible_paths}")
    
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
