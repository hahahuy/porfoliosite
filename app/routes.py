import requests
from flask import Blueprint, request, Response, render_template

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('index.html')

@main.route('/about')
def about():
    return render_template('about.html')

@main.route('/projects/<int:project_id>')
def project(project_id):
    # For now, just redirect to home page since we don't have individual project pages
    return render_template('index.html')

# ------------------------------------------------------------------
# proxy to your GitHub Pages site at /dg
# ------------------------------------------------------------------
@main.route('/dg', defaults={'path': ''})
@main.route('/dg/<path:path>')
def proxy_dg(path):
    # build the upstream URL
    upstream = f'https://hahahuy.github.io/dg/{path}'
    # fetch it (pass along any query-string args)
    resp = requests.get(upstream, params=request.args)
    # strip headers that Flask/WSGI will manage itself
    excluded = ('content-encoding','content-length','transfer-encoding','connection')
    headers = [(h, v) for h, v in resp.raw.headers.items() if h.lower() not in excluded]
    # return a mirrored response
    return Response(resp.content, resp.status_code, headers)
