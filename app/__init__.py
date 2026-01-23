import os
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, render_template
from pathlib import Path


def create_app(config_name=None):
    """Application factory pattern"""
    # Get base directory
    from .config import Config
    base_dir = Config.BASE_DIR
    
    app = Flask(__name__,
                template_folder=str(base_dir / 'app' / 'templates'),
                static_folder=str(base_dir / 'app' / 'static'))
    
    # Load configuration
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    from .config import config
    app.config.from_object(config.get(config_name, config['default']))
    
    # Initialize database
    from .database.db import db
    db.init_app(app)
    
    # Create database tables
    with app.app_context():
        try:
            # Create instance directory if it doesn't exist
            instance_path = Path(app.instance_path)
            instance_path.mkdir(parents=True, exist_ok=True)
            
            # Create tables
            db.create_all()
        except Exception as e:
            # Log error but don't fail app startup
            import sys
            print(f"Warning: Database initialization error: {e}", file=sys.stderr)
            # App will still start, database will be created on first use
    
    # Register blueprints
    from .routes.main import main_bp
    from .routes.projects import projects_bp
    from .routes.proxy import proxy_bp
    from .routes.contact import contact_bp
    from .routes.ml_api import ml_api_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(projects_bp)
    app.register_blueprint(proxy_bp)
    app.register_blueprint(contact_bp)
    app.register_blueprint(ml_api_bp)
    
    # Register error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('errors/500.html'), 500
    
    # Setup logging
    if not app.debug and not app.testing:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/portfolio.log',
                                         maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('Portfolio site startup')
    
    return app

# For simple deployment using a global app variable, you can create one instance:
app = create_app()
