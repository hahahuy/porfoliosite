#!/usr/bin/env python3
"""Helper script to update JSON content files"""
import json
import sys
from pathlib import Path


def update_project(title, description, tags, image, project_id=None):
    """Add or update a project"""
    projects_path = Path('app/content/projects.json')
    
    with open(projects_path, 'r', encoding='utf-8') as f:
        projects = json.load(f)
    
    if project_id is not None:
        # Update existing project
        for project in projects:
            if project['id'] == project_id:
                project.update({
                    'title': title,
                    'description': description,
                    'tags': tags,
                    'image': image
                })
                break
        else:
            print(f"Project with ID {project_id} not found")
            return False
    else:
        # Add new project
        new_id = max((p['id'] for p in projects), default=-1) + 1
        projects.append({
            'id': new_id,
            'title': title,
            'description': description,
            'tags': tags,
            'image': image,
            'link': f'/projects/{new_id}'
        })
    
    with open(projects_path, 'w', encoding='utf-8') as f:
        json.dump(projects, f, indent=2, ensure_ascii=False)
    
    print(f"✅ {'Updated' if project_id else 'Added'} project: {title}")
    return True


if __name__ == '__main__':
    if len(sys.argv) < 5:
        print("Usage: python update_content.py <title> <description> <tags> <image> [project_id]")
        print("Example: python update_content.py 'My Project' 'Description' '[\"Python\", \"ML\"]' '/static/images/project.png'")
        sys.exit(1)
    
    title = sys.argv[1]
    description = sys.argv[2]
    tags = json.loads(sys.argv[3])
    image = sys.argv[4]
    project_id = int(sys.argv[5]) if len(sys.argv) > 5 else None
    
    update_project(title, description, tags, image, project_id)
