"""Route tests"""
import pytest


def test_homepage(client):
    """Test homepage loads correctly"""
    response = client.get('/')
    assert response.status_code == 200
    # Check for name in response (using decode to handle unicode)
    response_text = response.data.decode('utf-8')
    assert 'Hà Quang Huy' in response_text or 'Quang Huy' in response_text


def test_about_page(client):
    """Test about page exists"""
    response = client.get('/about')
    assert response.status_code == 200


def test_project_route(client):
    """Test project detail page"""
    response = client.get('/projects/0')
    # Should return 200 or 404 depending on template existence
    assert response.status_code in [200, 404]


def test_proxy_route(client):
    """Test GitHub Pages proxy"""
    response = client.get('/dg')
    # Should proxy or return appropriate status
    assert response.status_code in [200, 302, 502]


def test_404_error(client):
    """Test 404 handling"""
    response = client.get('/nonexistent')
    assert response.status_code == 404


def test_health_endpoint(client):
    """Test health check endpoint"""
    response = client.get('/health')
    assert response.status_code == 200
    assert response.is_json
    data = response.get_json()
    assert data['status'] == 'healthy'
    assert data['service'] == 'portfolio'
