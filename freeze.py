"""
freeze.py — Generate a fully static version of the portfolio site.

Usage:
    python freeze.py

Output:
    ./build/  — static HTML + all assets, ready for GitHub Pages.
"""
import json
from pathlib import Path
from flask_frozen import Freezer
from app import create_app

app = create_app()
app.config["FREEZER_DESTINATION"] = "build"
app.config["FREEZER_RELATIVE_URLS"] = True   # makes all hrefs relative (works on gh-pages sub-path)
app.config["FREEZER_IGNORE_MIMETYPE_WARNINGS"] = True

freezer = Freezer(app)


# Frozen-Flask discovers static routes automatically.
# We only need to enumerate dynamic routes manually.
# The function name must match the blueprint-qualified endpoint: <blueprint>.<view>
@freezer.register_generator
def projects__project_detail():
    projects_file = Path(__file__).parent / "app" / "content" / "projects.json"
    projects = json.loads(projects_file.read_text(encoding="utf-8"))
    for project in projects:
        yield "projects.project_detail", {"project_id": project["id"]}


if __name__ == "__main__":
    freezer.freeze()
    print("✅  Static site built in ./build/")
