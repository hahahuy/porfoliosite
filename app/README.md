# Application Code

This directory contains the main Flask application code for the portfolio site.

## Directory Structure

```
app/
├── __init__.py          # Flask app factory and initialization
├── config.py            # Configuration classes (dev, prod, test)
├── routes.py            # Legacy routes (backward compatibility)
│
├── content/             # JSON content files (Option 1)
│   ├── profile.json     # Profile information
│   ├── projects.json    # Projects list
│   ├── skills.json      # Skills list
│   └── experience.json  # Experience entries
│
├── database/            # Database models (Option 2 - contact forms only)
│   ├── db.py           # SQLAlchemy database instance
│   └── models.py       # ContactSubmission model
│
├── routes/              # Route blueprints (organized by feature)
│   ├── main.py         # Homepage, about, health routes
│   ├── projects.py     # Project detail routes
│   ├── proxy.py        # GitHub Pages proxy (with security)
│   └── contact.py      # Contact form submission routes
│
├── services/            # Business logic layer
│   ├── content_service.py  # Content abstraction (JSON/CMS)
│   ├── cms_service.py      # Headless CMS integration
│   └── proxy_service.py    # Proxy business logic
│
├── utils/               # Utility functions
│   ├── content_loader.py   # JSON content loading
│   ├── cms_client.py       # CMS API clients (Strapi/Contentful/Sanity)
│   ├── form_handler.py     # Contact form validation and storage
│   ├── validators.py        # Input validation utilities
│   └── helpers.py          # General helper functions
│
├── static/              # Static assets
│   ├── css/            # Stylesheets
│   ├── images/         # Images
│   └── js/             # JavaScript files
│
└── templates/           # Jinja2 templates
    ├── base.html       # Base template
    ├── index.html      # Homepage template
    ├── about.html      # About page template
    └── errors/         # Error page templates
        ├── 404.html
        └── 500.html
```

## Key Components

### Application Factory (`__init__.py`)

The Flask application is created using a factory pattern:

```python
from app import create_app
app = create_app('development')  # or 'production', 'testing'
```

Features:
- Environment-based configuration
- Database initialization
- Blueprint registration
- Error handlers
- Logging setup

### Configuration (`config.py`)

Three configuration classes:
- `DevelopmentConfig` - For local development
- `ProductionConfig` - For production deployment
- `TestingConfig` - For running tests

Configuration includes:
- Flask settings
- Content source (JSON/CMS)
- CMS credentials
- Database URI

### Routes (`routes/`)

Routes are organized by feature:

- **main.py**: Core pages (home, about, health check)
- **projects.py**: Project detail pages
- **proxy.py**: Secure GitHub Pages proxy
- **contact.py**: Contact form handling

### Services (`services/`)

Business logic abstraction:

- **content_service.py**: Unified interface for loading content from JSON or CMS
- **cms_service.py**: Headless CMS integration (Strapi/Contentful/Sanity)
- **proxy_service.py**: Secure proxy functionality with validation

### Utilities (`utils/`)

Helper functions:

- **content_loader.py**: Load JSON content files
- **cms_client.py**: CMS API clients
- **form_handler.py**: Contact form processing
- **validators.py**: Input validation (SSRF protection, email validation)
- **helpers.py**: General utilities

### Content Management

The application supports three content management approaches:

1. **JSON Files** (`content/`) - Primary/fallback
2. **Headless CMS** - Strapi, Contentful, or Sanity
3. **Database** (`database/`) - Only for contact form submissions

See `docs/CONTENT_GUIDE.md` for details.

### Database Models

Currently only one model:
- `ContactSubmission` - Stores contact form submissions

Database is SQLite by default, configurable via `DATABASE_URL`.

## Usage Examples

### Loading Content

```python
from app.services.content_service import ContentService

# In a route
content_service = ContentService(current_app.config)
profile = content_service.get_profile()
projects = content_service.get_projects()
```

### Using CMS

```python
from app.services.cms_service import CMSService

cms_service = CMSService(app.config)
if cms_service.is_available():
    profile = cms_service.get_profile()
```

### Contact Form Submission

```python
from app.utils.form_handler import validate_contact_form, save_contact_submission

# Validate
is_valid, error = validate_contact_form(data)
if is_valid:
    submission = save_contact_submission(name, email, message)
```

## Testing

See `tests/README.md` for testing information.

## Related Documentation

- `docs/STRUCTURE_RECOMMENDATIONS.md` - Architecture details
- `docs/CONTENT_GUIDE.md` - Content management guide
- `docs/CMS_SETUP.md` - CMS configuration
