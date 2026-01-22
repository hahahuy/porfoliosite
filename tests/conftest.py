"""Pytest fixtures"""
import pytest
from app import create_app
from app.database.db import db


@pytest.fixture
def app():
    """Create application for testing"""
    app = create_app('testing')
    return app


@pytest.fixture
def client(app):
    """Create test client"""
    return app.test_client()


@pytest.fixture
def runner(app):
    """Create test CLI runner"""
    return app.test_cli_runner()


@pytest.fixture
def db_session(app):
    """Create database session for testing"""
    with app.app_context():
        db.create_all()
        yield db
        db.session.remove()
        db.drop_all()
