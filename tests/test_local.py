#!/usr/bin/env python3
"""
Comprehensive test script to verify the portfolio site is working locally
"""

import requests
import time
import webbrowser
import os
from urllib.parse import urljoin

def check_website(url="http://localhost:5000", open_browser=True):
    """
    Comprehensive function to check if your website is working properly
    
    Args:
        url (str): The URL to check (default: localhost:5000)
        open_browser (bool): Whether to open the website in browser
    
    Returns:
        bool: True if website is working, False otherwise
    """
    print("🔍 Checking your portfolio website...")
    print(f"📍 URL: {url}")
    print("-" * 50)
    
    try:
        # Test main page
        print("📡 Testing server connection...")
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            print("✅ Server is running successfully!")
            print(f"📊 Status Code: {response.status_code}")
            print(f"📏 Content Length: {len(response.content)} bytes")
            
            # Check for important content
            content = response.text.lower()
            checks = [
                ("Profile", "hà quang huy" in content),
                ("Skills", "python" in content and "sql" in content),
                ("Projects", "projects" in content),
                ("Education", "coursera" in content or "hcmiu" in content),
                ("Social Links", "linkedin" in content and "github" in content),
                ("Favicon", "favicon.png" in content),
                ("CSS", "output.css" in content),
                ("Vietnam Flag", "vietnam" in content)
            ]
            
            print("\n📋 Content Checks:")
            all_passed = True
            for check_name, passed in checks:
                status = "✅" if passed else "❌"
                print(f"   {status} {check_name}")
                if not passed:
                    all_passed = False
            
            # Check static files
            print("\n📁 Static Files Check:")
            static_files = [
                "/static/images/favicon.png",
                "/static/images/mypic.jpg", 
                "/static/images/header.png",
                "/static/css/output.css",
                "/static/css/style.css"
            ]
            
            for file_path in static_files:
                try:
                    file_url = urljoin(url, file_path)
                    file_response = requests.get(file_url, timeout=5)
                    status = "✅" if file_response.status_code == 200 else "❌"
                    print(f"   {status} {file_path}")
                except:
                    print(f"   ❌ {file_path}")
            
            print(f"\n🎯 Overall Status: {'✅ ALL GOOD!' if all_passed else '⚠️ Some issues found'}")
            
            if open_browser:
                print(f"\n🌐 Opening website in browser...")
                webbrowser.open(url)
                print("✅ Browser opened!")
            
            print(f"\n📝 Summary:")
            print(f"   • Website is accessible at: {url}")
            print(f"   • Server is responding correctly")
            print(f"   • Content checks: {sum(1 for _, passed in checks if passed)}/{len(checks)} passed")
            print(f"   • Ready for development and testing!")
            
            return True
            
        else:
            print(f"❌ Server returned unexpected status code: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server!")
        print("💡 Make sure your Flask server is running:")
        print("   python server.py")
        return False
    except Exception as e:
        print(f"❌ Error checking website: {e}")
        return False

def test_server():
    """Legacy function for backward compatibility"""
    return check_website(open_browser=False)

def quick_check():
    """Quick check without opening browser"""
    return check_website(open_browser=False)

def open_website():
    """Just open the website in browser"""
    url = "http://localhost:5000"
    print(f"🌐 Opening {url} in browser...")
    webbrowser.open(url)
    print("✅ Browser opened!")

if __name__ == "__main__":
    # Run comprehensive check
    check_website()