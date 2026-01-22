import os
from pathlib import Path


class Config:
    """Base configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    BASE_DIR = Path(__file__).parent.parent
    
    # Flask settings
    TEMPLATE_FOLDER = BASE_DIR / 'app' / 'templates'
    STATIC_FOLDER = BASE_DIR / 'app' / 'static'
    
    # Application settings
    SITE_NAME = "Hà Quang Huy Portfolio"
    SITE_URL = os.environ.get('SITE_URL', 'http://localhost:5000')
    
    # Proxy settings
    GITHUB_PAGES_URL = os.environ.get('GITHUB_PAGES_URL', 'https://hahahuy.github.io/dg')
    
    # Analytics (if using)
    ANALYTICS_ENABLED = os.environ.get('ANALYTICS_ENABLED', 'False').lower() == 'true'
    
    # Content Management Settings
    CONTENT_SOURCE = os.environ.get('CONTENT_SOURCE', 'json')  # 'json', 'cms', or 'cms_with_json_fallback'
    
    # Headless CMS Configuration (Option 3)
    CMS_TYPE = os.environ.get('CMS_TYPE', 'none')  # 'strapi', 'contentful', 'sanity', 'none'
    CMS_API_URL = os.environ.get('CMS_API_URL', '')
    CMS_API_KEY = os.environ.get('CMS_API_KEY', '')
    CMS_SPACE_ID = os.environ.get('CMS_SPACE_ID', '')  # For Contentful
    CMS_ENVIRONMENT = os.environ.get('CMS_ENVIRONMENT', 'master')  # For Contentful
    CMS_PROJECT_ID = os.environ.get('CMS_PROJECT_ID', '')  # For Sanity
    CMS_DATASET = os.environ.get('CMS_DATASET', 'production')  # For Sanity
    
    # Database Configuration (Option 2 - for contact forms only)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        f'sqlite:///{BASE_DIR / "instance" / "portfolio.db"}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY')  # Must be set in production
    CONTENT_SOURCE = os.environ.get('CONTENT_SOURCE', 'cms_with_json_fallback')


class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


# Configuration mapping
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
