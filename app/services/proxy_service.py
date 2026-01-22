"""Proxy service for GitHub Pages with security"""
import requests
from typing import Tuple, Optional
from flask import current_app, request, Response
from app.utils.validators import validate_proxy_path, validate_url


class ProxyService:
    """Service for proxying requests to GitHub Pages"""
    
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/')
    
    def proxy_request(self, path: str) -> Tuple[Optional[Response], Optional[str]]:
        """
        Proxy a request to GitHub Pages.
        
        Args:
            path: The path to proxy
        
        Returns:
            Tuple of (Response, error_message)
        """
        # Validate path
        is_valid, error = validate_proxy_path(path)
        if not is_valid:
            return None, error
        
        # Build upstream URL
        upstream = f'{self.base_url}/{path}'
        
        # Validate URL
        allowed_domains = ['hahahuy.github.io']
        is_valid, error = validate_url(upstream, allowed_domains)
        if not is_valid:
            return None, error
        
        try:
            # Make request with timeout
            resp = requests.get(
                upstream,
                params=request.args,
                timeout=10,
                allow_redirects=True
            )
            resp.raise_for_status()
            
            # Strip headers that Flask/WSGI will manage
            excluded = ('content-encoding', 'content-length', 
                       'transfer-encoding', 'connection')
            headers = [(h, v) for h, v in resp.raw.headers.items() 
                      if h.lower() not in excluded]
            
            # Return mirrored response
            return Response(resp.content, resp.status_code, headers), None
            
        except requests.Timeout:
            try:
                current_app.logger.error(f"Proxy timeout for {upstream}")
            except RuntimeError:
                pass  # Outside app context
            return None, "Request timeout"
        except requests.RequestException as e:
            try:
                current_app.logger.error(f"Proxy error for {upstream}: {e}")
            except RuntimeError:
                pass  # Outside app context
            return None, f"Proxy error: {str(e)}"
        except Exception as e:
            try:
                current_app.logger.error(f"Unexpected proxy error: {e}")
            except RuntimeError:
                pass  # Outside app context
            return None, "Internal proxy error"
