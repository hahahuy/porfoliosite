# Tests

This directory contains all tests for the portfolio site application.

## Test Files

### Core Test Files

- **`conftest.py`** - Pytest configuration and fixtures
  - `app` fixture - Creates test application
  - `client` fixture - Creates test client
  - `runner` fixture - Creates CLI test runner
  - `db_session` fixture - Database session for tests

- **`test_routes.py`** - Route endpoint tests
  - Homepage loading
  - About page
  - Project detail pages
  - Proxy route
  - Health endpoint
  - 404 error handling

- **`test_proxy.py`** - Proxy functionality tests
  - Path validation
  - URL validation
  - SSRF protection

- **`test_content_service.py`** - Content service tests
  - JSON content loading
  - CMS fallback behavior
  - Content service abstraction

### Legacy Test Files

- **`test_smoke.py`** - Smoke tests (basic functionality checks)
- **`test_local.py`** - Local testing utilities
- **`check_website.py`** - Website checking script with browser automation

### Website Checker (`check_website.py`)

Interactive tool for checking website functionality:

```bash
# Full check with browser
python tests/check_website.py check

# Quick test (no browser)
python tests/check_website.py test

# Just open browser
python tests/check_website.py open

# Check server status
python tests/check_website.py status

# Start server
python tests/check_website.py start
```

**What it checks:**
- Server connection
- Content sections (profile, skills, projects)
- Static files (images, CSS)
- Social media links
- Favicon and assets

See the existing `tests/README.md` content for detailed usage.

## Running Tests

### Run All Tests

```bash
pytest
```

### Run Specific Test File

```bash
pytest tests/test_routes.py
pytest tests/test_proxy.py
pytest tests/test_content_service.py
```

### Run with Verbose Output

```bash
pytest -v
```

### Run with Coverage

```bash
pip install pytest-cov
pytest --cov=app --cov-report=html
```

### Run Specific Test Function

```bash
pytest tests/test_routes.py::test_homepage
```

### Run Tests Matching Pattern

```bash
pytest -k "route"  # Runs all tests with "route" in name
pytest -k "not proxy"  # Runs all tests except proxy tests
```

## Test Configuration

Configuration is in `pytest.ini` at the project root:

```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    -v
    --strict-markers
    --tb=short
    --disable-warnings
markers =
    smoke: Smoke tests
    integration: Integration tests
    unit: Unit tests
```

## Test Fixtures

Fixtures are defined in `conftest.py`:

### `app` fixture
Creates a Flask application instance for testing:
```python
def test_something(app):
    with app.app_context():
        # Test code here
```

### `client` fixture
Creates a test client for making HTTP requests:
```python
def test_homepage(client):
    response = client.get('/')
    assert response.status_code == 200
```

### `db_session` fixture
Provides a database session for tests:
```python
def test_contact_form(db_session):
    # Database operations here
    submission = ContactSubmission(...)
    db_session.add(submission)
```

## Writing New Tests

### Test Structure

```python
def test_feature_name(client):
    """Test description"""
    # Arrange
    # Act
    response = client.get('/endpoint')
    # Assert
    assert response.status_code == 200
    assert b'expected content' in response.data
```

### Test Markers

Use markers to categorize tests:

```python
import pytest

@pytest.mark.smoke
def test_basic_functionality(client):
    """Smoke test"""
    pass

@pytest.mark.integration
def test_full_workflow(client, db_session):
    """Integration test"""
    pass
```

### Testing with Database

```python
def test_contact_submission(client, db_session):
    """Test contact form submission"""
    response = client.post('/contact', json={
        'name': 'Test User',
        'email': 'test@example.com',
        'message': 'Test message'
    })
    assert response.status_code == 201
    
    # Verify in database
    submission = ContactSubmission.query.first()
    assert submission.email == 'test@example.com'
```

### Testing Content Service

```python
def test_content_loading(client, app):
    """Test content service loads content"""
    with app.app_context():
        from app.services.content_service import ContentService
        service = ContentService(app.config)
        profile = service.get_profile()
        assert 'name' in profile
```

## Test Coverage Goals

Aim for:
- **Routes**: All endpoints tested
- **Services**: Core business logic tested
- **Utilities**: Critical functions tested
- **Error handling**: Error cases covered

## Continuous Integration

Tests are run automatically in CI/CD:

```yaml
# .github/workflows/deploy.yml
- name: Run tests
  run: pytest --maxfail=1 --disable-warnings -q
```

## Troubleshooting

### Import Errors

If tests fail with import errors:
```bash
# Ensure you're in project root
cd /path/to/porfoliosite
# Install dependencies
pip install -r requirements.txt
```

### Database Errors

If database tests fail:
- Check `pytest.ini` configuration
- Verify `conftest.py` fixtures
- Ensure test database is in-memory or separate file

### Fixture Not Found

If fixtures aren't found:
- Check `conftest.py` exists in `tests/` directory
- Verify fixture names match usage
- Run `pytest --fixtures` to see available fixtures

## Best Practices

1. **Isolation**: Each test should be independent
2. **Naming**: Use descriptive test names
3. **Assertions**: One clear assertion per test concept
4. **Fixtures**: Use fixtures for setup/teardown
5. **Mocking**: Mock external services (CMS, APIs)
6. **Documentation**: Add docstrings to test functions

## Related Documentation

- `docs/STRUCTURE_RECOMMENDATIONS.md` - Testing recommendations
- `pytest.ini` - Pytest configuration
- `app/README.md` - Application code structure
