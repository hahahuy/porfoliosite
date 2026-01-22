"""Main routes - homepage, about, health"""
from flask import Blueprint, render_template, jsonify, current_app
from app.services.content_service import ContentService

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def home():
    """Homepage"""
    try:
        content_service = ContentService(current_app.config)
        profile = content_service.get_profile()
        projects = content_service.get_projects()
        skills = content_service.get_skills()
        experience = content_service.get_experience()
        
        return render_template(
            'index.html',
            profile=profile,
            projects=projects,
            skills=skills,
            experience=experience
        )
    except Exception as e:
        current_app.logger.error(f"Error loading homepage: {e}")
        # Fallback to basic template
        return render_template('index.html', 
                             profile={}, 
                             projects=[], 
                             skills=[], 
                             experience=[])


@main_bp.route('/about')
def about():
    """About page"""
    try:
        content_service = ContentService(current_app.config)
        profile = content_service.get_profile()
        return render_template('about.html', profile=profile)
    except Exception as e:
        current_app.logger.error(f"Error loading about page: {e}")
        return render_template('about.html', profile={})


@main_bp.route('/health')
def health():
    """Health check endpoint for monitoring"""
    return jsonify({
        'status': 'healthy',
        'service': 'portfolio'
    }), 200
