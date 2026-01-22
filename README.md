# Portfolio Site

A modern, flexible portfolio website built with Flask, featuring multiple content management options and automated deployment.

## Features

- 🎨 **Modern UI** - Clean, responsive design
- 📝 **Flexible Content Management** - JSON files, Headless CMS, or both
- 🔒 **Secure** - SSRF protection, input validation, error handling
- 🚀 **Automated Deployment** - GitHub Actions CI/CD to EC2
- 📊 **Health Monitoring** - Health check endpoints
- 📧 **Contact Forms** - Database-backed contact submissions
- 🧪 **Tested** - Comprehensive test suite

## Quick Start

### Prerequisites

- Python 3.10+
- pip
- (Optional) Virtual environment

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd porfoliosite

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Configuration

1. Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

2. Edit `.env` with your settings:
```bash
SECRET_KEY=your-secret-key-here
FLASK_ENV=development
CONTENT_SOURCE=json  # or 'cms', 'cms_with_json_fallback'
```

### Run Locally

```bash
python server.py
```

Visit `http://localhost:5000`

## Project Structure

```
porfoliosite/
├── app/                    # Application code
│   ├── content/           # JSON content files
│   ├── database/          # Database models
│   ├── routes/            # Route blueprints
│   ├── services/          # Business logic
│   ├── templates/         # Jinja2 templates
│   ├── utils/             # Utility functions
│   └── static/            # Static assets
├── docs/                  # Documentation
├── scripts/               # Utility scripts
├── tests/                 # Test suite
├── .github/               # GitHub Actions workflows
└── requirements.txt       # Python dependencies
```

## Documentation

### Getting Started

- **[docs/README.md](docs/README.md)** - Documentation index and navigation
- **[docs/CONTENT_GUIDE.md](docs/CONTENT_GUIDE.md)** - How to update content
- **[docs/CMS_SETUP.md](docs/CMS_SETUP.md)** - Headless CMS configuration

### Architecture

- **[docs/STRUCTURE_RECOMMENDATIONS.md](docs/STRUCTURE_RECOMMENDATIONS.md)** - Complete architecture guide
- **[app/README.md](app/README.md)** - Application code structure
- **[tests/README.md](tests/README.md)** - Testing guide
- **[scripts/README.md](scripts/README.md)** - Utility scripts

### Deployment

- **[docs/HANDOUT.md](docs/HANDOUT.md)** - Deployment and infrastructure guide

## Content Management

The site supports three content management approaches:

### Option 1: JSON Files (Default)

Edit JSON files in `app/content/`:
- `profile.json` - Profile information
- `projects.json` - Projects list
- `skills.json` - Skills list
- `experience.json` - Experience entries

See [docs/CONTENT_GUIDE.md](docs/CONTENT_GUIDE.md) for details.

### Option 2: Headless CMS

Integrate with Strapi, Contentful, or Sanity:
- Configure in `.env`
- CMS serves as primary source
- JSON files as fallback

See [docs/CMS_SETUP.md](docs/CMS_SETUP.md) for setup.

### Option 3: Database (Contact Forms)

SQLite database stores contact form submissions:
- Automatic validation
- IP address tracking
- Database model in `app/database/models.py`

## Development

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_routes.py
```

See [tests/README.md](tests/README.md) for more.

### Utility Scripts

```bash
# Update content
python scripts/update_content.py "Title" "Description" '["Tag"]' "/static/image.png"

# Sync CMS to JSON
python scripts/sync_cms.py

# Pre-deployment checks
python scripts/deploy_check.py
```

See [scripts/README.md](scripts/README.md) for details.

## Deployment

### Automated Deployment

The site uses GitHub Actions for automated deployment to EC2:

1. Push to `main` branch
2. Tests run automatically
3. On success, deploys to EC2 via SSH
4. Application restarts

See `.github/workflows/deploy.yml` for configuration.

### Manual Deployment

1. SSH to EC2 instance
2. Navigate to application directory
3. Pull latest changes: `git pull`
4. Install dependencies: `pip install -r requirements.txt`
5. Restart service: `sudo systemctl restart myapp`

See [docs/HANDOUT.md](docs/HANDOUT.md) for infrastructure details.

## Testing Before Commit

```bash
# 1. Run test suite
pytest

# 2. Start server
python server.py

# 3. Test endpoints
curl http://localhost:5000/health
curl http://localhost:5000/

# 4. Run deployment checks
python scripts/deploy_check.py
```

## Configuration

### Environment Variables

Key environment variables (see `.env.example`):

- `SECRET_KEY` - Flask secret key (required in production)
- `FLASK_ENV` - Environment (development/production/testing)
- `CONTENT_SOURCE` - Content source (json/cms/cms_with_json_fallback)
- `CMS_TYPE` - CMS type (strapi/contentful/sanity/none)
- `CMS_API_URL` - CMS API URL
- `CMS_API_KEY` - CMS API key
- `DATABASE_URL` - Database connection string

### Configuration Classes

Configuration is managed in `app/config.py`:
- `DevelopmentConfig` - Local development
- `ProductionConfig` - Production deployment
- `TestingConfig` - Test environment

## Features

### Routes

- `/` - Homepage with portfolio content
- `/about` - About page
- `/projects/<id>` - Project detail pages
- `/dg` - GitHub Pages proxy
- `/contact` - Contact form submission (POST)
- `/health` - Health check endpoint

### Security

- SSRF protection on proxy route
- Input validation on contact forms
- Path traversal prevention
- URL validation
- Error handling with custom pages

### Error Handling

- Custom 404 page
- Custom 500 page
- Logging to `logs/portfolio.log`
- Graceful fallbacks

## Contributing

1. Create a feature branch
2. Make your changes
3. Run tests: `pytest`
4. Run checks: `python scripts/deploy_check.py`
5. Commit and push

## License

[Your License Here]

## Contact

- Website: [https://hahuy.site](https://hahuy.site)
- Email: quanghuyha098@gmail.com

## Related Links

- [Documentation Index](docs/README.md)
- [Content Guide](docs/CONTENT_GUIDE.md)
- [CMS Setup](docs/CMS_SETUP.md)
- [Architecture Guide](docs/STRUCTURE_RECOMMENDATIONS.md)
