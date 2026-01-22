"""Project routes"""
from flask import Blueprint, render_template, abort, current_app
from app.services.content_service import ContentService

projects_bp = Blueprint('projects', __name__)


@projects_bp.route('/projects/<int:project_id>')
def project_detail(project_id):
    """Project detail page"""
    try:
        content_service = ContentService(current_app.config)
        project = content_service.get_project_by_id(project_id)
        
        if not project:
            abort(404)
        
        return render_template('projects/detail.html', project=project)
    except Exception as e:
        current_app.logger.error(f"Error loading project {project_id}: {e}")
        abort(404)
