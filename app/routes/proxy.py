"""GitHub Pages proxy route with security"""
from flask import Blueprint, request, abort, current_app
from app.services.proxy_service import ProxyService

proxy_bp = Blueprint('proxy', __name__)


@proxy_bp.route('/dg', defaults={'path': ''})
@proxy_bp.route('/dg/<path:path>')
def proxy_dg(path):
    """Proxy requests to GitHub Pages site"""
    try:
        base_url = current_app.config.get('GITHUB_PAGES_URL', 'https://hahahuy.github.io/dg')
        proxy_service = ProxyService(base_url)
        
        response, error = proxy_service.proxy_request(path)
        
        if error:
            current_app.logger.warning(f"Proxy error: {error}")
            abort(502)
        
        return response
    except Exception as e:
        current_app.logger.error(f"Unexpected proxy error: {e}")
        abort(500)
