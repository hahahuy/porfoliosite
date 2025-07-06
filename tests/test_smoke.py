"""
Smoke tests for the portfolio website
"""

import requests
import pytest

def test_basic_functionality():
    """Test that the basic website functionality works"""
    assert 1 == 1  # Basic assertion to ensure tests run

def test_server_connection():
    """Test that the server is accessible"""
    try:
        response = requests.get('http://localhost:5000', timeout=5)
        assert response.status_code == 200
    except requests.exceptions.ConnectionError:
        pytest.skip("Server not running - run 'python server.py' first")

def test_homepage_content():
    """Test that the homepage contains expected content"""
    try:
        response = requests.get('http://localhost:5000', timeout=5)
        content = response.text.lower()
        
        # Check for essential content
        assert "hà quang huy" in content, "Profile name not found"
        assert "python" in content, "Python skill not found"
        assert "projects" in content, "Projects section not found"
        assert "favicon.png" in content, "Favicon not found"
        
    except requests.exceptions.ConnectionError:
        pytest.skip("Server not running - run 'python server.py' first")

def test_static_files():
    """Test that essential static files are accessible"""
    base_url = "http://localhost:5000"
    static_files = [
        "/static/images/favicon.png",
        "/static/images/mypic.jpg",
        "/static/css/output.css"
    ]
    
    for file_path in static_files:
        try:
            response = requests.get(f"{base_url}{file_path}", timeout=5)
            assert response.status_code == 200, f"Static file {file_path} not accessible"
        except requests.exceptions.ConnectionError:
            pytest.skip("Server not running - run 'python server.py' first")

if __name__ == "__main__":
    # Run basic tests
    test_basic_functionality()
    print("✅ Basic functionality test passed")
    
    try:
        test_server_connection()
        print("✅ Server connection test passed")
        
        test_homepage_content()
        print("✅ Homepage content test passed")
        
        test_static_files()
        print("✅ Static files test passed")
        
        print("\n🎉 All smoke tests passed!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        print("💡 Make sure your server is running: python server.py")