#!/usr/bin/env python3
"""Sync content from CMS to JSON files (backup/fallback)"""
import json
import sys
from pathlib import Path
from app import create_app
from app.services.cms_service import CMSService


def sync_cms_to_json():
    """Sync all content from CMS to JSON files"""
    app = create_app()
    
    with app.app_context():
        cms_service = CMSService(app.config)
        
        if not cms_service.is_available():
            print("❌ CMS is not configured or unavailable")
            return False
        
        content_dir = Path('app/content')
        content_dir.mkdir(parents=True, exist_ok=True)
        
        # Sync profile
        try:
            profile = cms_service.get_profile()
            if profile:
                with open(content_dir / 'profile.json', 'w', encoding='utf-8') as f:
                    json.dump(profile, f, indent=2, ensure_ascii=False)
                print("✅ Synced profile")
        except Exception as e:
            print(f"❌ Error syncing profile: {e}")
        
        # Sync projects
        try:
            projects = cms_service.get_projects()
            if projects:
                with open(content_dir / 'projects.json', 'w', encoding='utf-8') as f:
                    json.dump(projects, f, indent=2, ensure_ascii=False)
                print(f"✅ Synced {len(projects)} projects")
        except Exception as e:
            print(f"❌ Error syncing projects: {e}")
        
        # Sync skills
        try:
            skills = cms_service.get_skills()
            if skills:
                with open(content_dir / 'skills.json', 'w', encoding='utf-8') as f:
                    json.dump(skills, f, indent=2, ensure_ascii=False)
                print(f"✅ Synced {len(skills)} skills")
        except Exception as e:
            print(f"❌ Error syncing skills: {e}")
        
        # Sync experience
        try:
            experience = cms_service.get_experience()
            if experience:
                with open(content_dir / 'experience.json', 'w', encoding='utf-8') as f:
                    json.dump(experience, f, indent=2, ensure_ascii=False)
                print(f"✅ Synced {len(experience)} experience entries")
        except Exception as e:
            print(f"❌ Error syncing experience: {e}")
        
        print("✅ CMS sync completed")
        return True


if __name__ == '__main__':
    success = sync_cms_to_json()
    sys.exit(0 if success else 1)
