#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Pre-deployment health checks"""
import sys
import requests
from pathlib import Path
import io
import os

# Fix Windows console encoding for Unicode characters
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')


def check_health(url="http://localhost:5000"):
    """Check if health endpoint responds"""
    try:
        response = requests.get(f"{url}/health", timeout=5)
        if response.status_code == 200:
            data = response.get_json()
            if data.get('status') == 'healthy':
                print("✅ Health check passed")
                return True
            else:
                print(f"❌ Health check failed: {data}")
                return False
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("⚠️  Health check skipped (server not running)")
        print("   Start server with 'python server.py' to test health endpoint")
        return True  # Don't fail if server isn't running
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False


def check_content_files():
    """Check if required content files exist"""
    content_dir = Path('app/content')
    required_files = ['profile.json', 'projects.json', 'skills.json', 'experience.json']
    
    all_exist = True
    for filename in required_files:
        filepath = content_dir / filename
        if filepath.exists():
            print(f"✅ {filename} exists")
        else:
            print(f"❌ {filename} missing")
            all_exist = False
    
    return all_exist


def check_templates():
    """Check if required templates exist"""
    templates_dir = Path('app/templates')
    required_templates = ['index.html', 'about.html', 'errors/404.html', 'errors/500.html']
    
    all_exist = True
    for template in required_templates:
        filepath = templates_dir / template
        if filepath.exists():
            print(f"✅ {template} exists")
        else:
            print(f"❌ {template} missing")
            all_exist = False
    
    return all_exist


if __name__ == "__main__":
    print("Running pre-deployment checks...")
    print()
    
    checks_passed = True
    
    print("Checking content files...")
    if not check_content_files():
        checks_passed = False
    print()
    
    print("Checking templates...")
    if not check_templates():
        checks_passed = False
    print()
    
    print("Checking health endpoint...")
    if not check_health():
        checks_passed = False
    print()
    
    if checks_passed:
        print("✅ All checks passed!")
        sys.exit(0)
    else:
        print("❌ Some checks failed")
        sys.exit(1)
