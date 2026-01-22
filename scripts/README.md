# Utility Scripts

This directory contains utility scripts for managing and maintaining the portfolio site.

## Available Scripts

### `update_content.py`

Helper script to add or update projects in JSON content files.

**Usage:**
```bash
python scripts/update_content.py <title> <description> <tags> <image> [project_id]
```

**Examples:**
```bash
# Add a new project
python scripts/update_content.py "My New Project" "Project description" '["Python", "ML"]' "/static/images/project.png"

# Update existing project (ID 0)
python scripts/update_content.py "Updated Title" "New description" '["Python"]' "/static/images/project.png" 0
```

**Parameters:**
- `title`: Project title
- `description`: Project description
- `tags`: JSON array of tags (e.g., `'["Python", "ML"]'`)
- `image`: Path to project image
- `project_id` (optional): ID of project to update (if omitted, creates new)

**What it does:**
- Reads `app/content/projects.json`
- Adds new project or updates existing one
- Automatically assigns next available ID for new projects
- Saves updated JSON file

### `sync_cms.py`

Syncs content from Headless CMS to JSON files for backup/fallback.

**Usage:**
```bash
python scripts/sync_cms.py
```

**Requirements:**
- CMS must be configured in environment variables
- See `docs/CMS_SETUP.md` for CMS configuration

**What it does:**
- Connects to configured CMS (Strapi/Contentful/Sanity)
- Downloads all content (profile, projects, skills, experience)
- Saves to JSON files in `app/content/`
- Creates backups for version control and fallback

**When to use:**
- Regular backups before CMS changes
- Creating local JSON copies for development
- Setting up fallback content when CMS is unavailable

**Output:**
```
✅ Synced profile
✅ Synced 5 projects
✅ Synced 7 skills
✅ Synced 3 experience entries
✅ CMS sync completed
```

### `deploy_check.py`

Pre-deployment health checks and validation.

**Usage:**
```bash
python scripts/deploy_check.py
```

**What it checks:**
1. **Content Files**: Verifies all required JSON files exist
   - `app/content/profile.json`
   - `app/content/projects.json`
   - `app/content/skills.json`
   - `app/content/experience.json`

2. **Templates**: Verifies all required templates exist
   - `app/templates/index.html`
   - `app/templates/about.html`
   - `app/templates/errors/404.html`
   - `app/templates/errors/500.html`

3. **Health Endpoint**: Tests `/health` endpoint
   - Checks if server responds
   - Validates JSON response format

**When to use:**
- Before committing changes
- Before deploying to production
- In CI/CD pipelines
- After major refactoring

**Exit codes:**
- `0`: All checks passed
- `1`: One or more checks failed

**Example output:**
```
Running pre-deployment checks...

Checking content files...
✅ profile.json exists
✅ projects.json exists
✅ skills.json exists
✅ experience.json exists

Checking templates...
✅ index.html exists
✅ about.html exists
✅ errors/404.html exists
✅ errors/500.html exists

Checking health endpoint...
✅ Health check passed

✅ All checks passed!
```

## Running Scripts

### Prerequisites

All scripts require the application to be importable:

```bash
# From project root
python scripts/script_name.py
```

### Environment Variables

Some scripts may require environment variables:
- `sync_cms.py` needs CMS configuration (see `.env.example`)
- `deploy_check.py` may need server running for health check

### Error Handling

All scripts include error handling and will:
- Print clear error messages
- Exit with appropriate status codes
- Not crash on missing files (where applicable)

## Creating New Scripts

When creating new utility scripts:

1. **Add shebang**: `#!/usr/bin/env python3`
2. **Add docstring**: Explain what the script does
3. **Error handling**: Use try/except blocks
4. **Exit codes**: Return 0 on success, 1 on failure
5. **User feedback**: Print status messages
6. **Update this README**: Document new scripts here

**Template:**
```python
#!/usr/bin/env python3
"""Script description"""
import sys
from pathlib import Path

def main():
    """Main function"""
    try:
        # Script logic here
        print("✅ Success")
        return 0
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1

if __name__ == '__main__':
    sys.exit(main())
```

## Integration with CI/CD

These scripts can be integrated into CI/CD pipelines:

```yaml
# Example GitHub Actions step
- name: Run deployment checks
  run: python scripts/deploy_check.py

- name: Sync CMS to JSON
  run: python scripts/sync_cms.py
  env:
    CMS_TYPE: ${{ secrets.CMS_TYPE }}
    CMS_API_KEY: ${{ secrets.CMS_API_KEY }}
```

## Related Documentation

- `docs/CONTENT_GUIDE.md` - Content management guide
- `docs/CMS_SETUP.md` - CMS configuration
- `docs/STRUCTURE_RECOMMENDATIONS.md` - Project structure
