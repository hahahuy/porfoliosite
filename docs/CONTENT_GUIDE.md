# Content Update Guide

This guide explains how to update content on your portfolio site.

## Current Content Structure

Currently, all content is embedded directly in the HTML template (`app/templates/index.html`). This guide covers both the current approach and the recommended JSON-based approach.

---

## Quick Updates (Current Method)

### Updating Profile Information

1. Open `app/templates/index.html`
2. Find the profile section (around line 115)
3. Update the following fields:

```html
<p class="text-2xl font-semibold mb-1 text-gray-900">Your Name</p>
<p class="text-md text-gray-900 mb-1"> Your Title | Skills | Education </p>
<p class="flex text-sm text-gray-600">Based in Your Location</p>
```

### Updating Social Links

Find the social links section (around line 125-200) and update URLs:

```html
<a href="YOUR_LINKEDIN_URL" class="...">
<a href="YOUR_GITHUB_URL" class="...">
<a href="YOUR_KAGGLE_URL" class="...">
<a href="mailto:YOUR_EMAIL" class="...">
```

### Updating Skills

Find the skills section (around line 217) and add/remove skill buttons:

```html
<button class="px-2.5 py-1 rounded-full text-sm font-sm bg-ds_blue_light text-ds_blue ring- mr-1 mb-1 cursor-default">
    Your Skill
</button>
```

### Adding/Updating Projects

Find the projects section (around line 327) and add a new project card:

```html
<div class=" bg-white shadow-lg shadow-gray-50 border border-gray-200 rounded-2xl ">
    <a href="/projects/PROJECT_ID" class="group">
        <img class="w-full mb-2 rounded-t-2xl border-0 border-gray-200" 
             src="/static/images/PROJECT_IMAGE.png" 
             alt="Project photo">
        <div class="sm:px-4 px-2 sm:pb-4 pb-2">
            <p class="text-md text-gray-900 mb-1 mt-2 font-semibold group-hover:underline group-hover:underline-offset-4">
                Project Title
            </p>
            
            <div class="mt-2">
                <button class="px-2.5 py-0.5 rounded-full text-sm font-sm bg-ds_blue_light text-ds_blue ring- mr-1 mb-1">
                    Tag 1
                </button>
                <!-- Add more tags -->
            </div>
            
            <p class="text-sm text-gray-600 mb-1 mt-2">
                Project description...
            </p>
            
            <div class="flex items-center mt-1 text-sm border-ds_blue border-0 text-ds_blue py-0.5 pr-1">
                Read more
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 20 20" stroke-width="1.5" stroke="currentColor" class=" w-3 h-3 ml-0.5">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M4.5 12h15m0 0l-6.75-6.75M19.5 12l-6.75 6.75"></path>
                </svg>
            </div>
        </div>
    </a>
</div>
```

### Updating About Section

Find the about section (around line 209) and update:

```html
<p class="text-sm text-gray-900 mb-10">
    Your bio text here...
</p>
```

---

## Recommended Method: JSON Content Files

Once you implement the JSON-based content system (see `STRUCTURE_RECOMMENDATIONS.md`), updating content becomes much easier.

### Profile Updates

Edit `app/content/profile.json`:

```json
{
  "name": "Hà Quang Huy",
  "title": "Entry Level Data analysis | MLOps",
  "location": "Hồ Chí Minh, VN",
  "bio": "Your bio text here...",
  "social": {
    "linkedin": "https://www.linkedin.com/in/your-profile/",
    "github": "https://github.com/yourusername",
    "kaggle": "https://www.kaggle.com/yourusername",
    "email": "your.email@example.com"
  }
}
```

### Project Updates

Edit `app/content/projects.json`:

```json
[
  {
    "id": 0,
    "title": "Your Project Title",
    "description": "Project description that appears on the card...",
    "image": "/static/images/your-image.png",
    "tags": ["Python", "Machine Learning", "Data Analysis"],
    "link": "/projects/0",
    "full_description": "Full project description for detail page..."
  },
  {
    "id": 1,
    "title": "Another Project",
    "description": "Another project description...",
    "image": "/static/images/another-image.png",
    "tags": ["R", "Statistics"],
    "link": "/projects/1"
  }
]
```

### Skills Updates

Edit `app/content/skills.json`:

```json
[
  "Python",
  "SQL",
  "R",
  "PowerBI",
  "Tableau",
  "Computer Vision",
  "PyTorch",
  "TensorFlow"
]
```

### Experience Updates

Edit `app/content/experience.json`:

```json
[
  {
    "title": "Job Title",
    "company": "Company Name",
    "location": "Location",
    "start_date": "2020-01",
    "end_date": "2022-12",
    "description": "Job description and achievements..."
  }
]
```

---

## Adding New Images

1. Place images in `app/static/images/`
2. Reference them in your content:
   - HTML: `/static/images/filename.png`
   - JSON: `"/static/images/filename.png"`

### Image Best Practices

- **Format:** Use PNG for logos/icons, JPG for photos
- **Size:** Optimize images (aim for < 500KB)
- **Dimensions:** 
  - Profile photo: 200x200px (square)
  - Project images: 1200x600px (2:1 ratio)
  - Header images: 1920x400px

### Image Optimization Tools

- Online: TinyPNG, Squoosh
- Command line: `pip install pillow` then use Python script

---

## Testing Your Changes

### Local Testing

1. Start the server:
   ```bash
   python server.py
   ```

2. Open browser:
   ```bash
   python tests/check_website.py open
   ```

3. Or run tests:
   ```bash
   python tests/check_website.py test
   ```

### Before Deploying

1. Check for broken links
2. Verify images load correctly
3. Test on mobile viewport
4. Run smoke tests:
   ```bash
   pytest tests/test_smoke.py
   ```

---

## Common Updates

### Adding a New Project

**Current Method:**
1. Add project card HTML to `index.html`
2. Ensure project image exists in `app/static/images/`
3. Update project ID in link (`/projects/N`)

**JSON Method (Recommended):**
1. Add new entry to `app/content/projects.json`
2. Ensure project image exists
3. (Optional) Create detail page template

### Updating Bio

**Current Method:**
- Edit the `<p>` tag in the About section

**JSON Method:**
- Edit `bio` field in `app/content/profile.json`

### Changing Skills

**Current Method:**
- Add/remove skill button HTML elements

**JSON Method:**
- Add/remove items in `app/content/skills.json` array

---

## Content Guidelines

### Writing Project Descriptions

- **Card Description:** 150-200 characters (brief overview)
- **Full Description:** 500-1000 words (for detail pages)
- **Include:**
  - Problem statement
  - Approach/methodology
  - Key technologies used
  - Results/outcomes
  - Links to code/demo (if available)

### Writing Bio

- Keep it concise (2-3 sentences)
- Highlight key achievements
- Mention your interests/passion
- Include relevant education/background

### Choosing Tags/Skills

- Use consistent naming (e.g., "Python" not "python" or "Python Programming")
- Group related skills together
- Limit to 5-7 skills for clarity
- Use tags that match your projects

---

## Troubleshooting

### Images Not Showing

1. Check file path is correct
2. Verify file exists in `app/static/images/`
3. Check file permissions
4. Clear browser cache

### Changes Not Appearing

1. Restart Flask server
2. Hard refresh browser (Ctrl+Shift+R / Cmd+Shift+R)
3. Check for syntax errors in JSON (if using JSON method)
4. Check server logs for errors

### JSON Syntax Errors

If using JSON method and getting errors:

1. Validate JSON at jsonlint.com
2. Check for trailing commas
3. Ensure all strings are in quotes
4. Check for missing brackets/braces

---

## Version Control Best Practices

### Before Making Changes

```bash
git pull  # Get latest changes
git checkout -b update-content  # Create branch
```

### After Making Changes

```bash
git add app/content/  # or app/templates/index.html
git commit -m "Update: Added new project X"
git push origin update-content
```

### Commit Messages

Use clear, descriptive messages:
- ✅ `Update: Added machine learning project`
- ✅ `Fix: Updated LinkedIn URL`
- ❌ `Updated stuff`
- ❌ `Changes`

---

## Automation Ideas

### Content Update Script

Create `scripts/update_content.py`:

```python
#!/usr/bin/env python3
"""Helper script to update content"""
import json
import sys
from pathlib import Path

def update_project(title, description, tags, image):
    """Add a new project"""
    projects_path = Path('app/content/projects.json')
    with open(projects_path, 'r') as f:
        projects = json.load(f)
    
    new_id = max(p['id'] for p in projects) + 1
    projects.append({
        'id': new_id,
        'title': title,
        'description': description,
        'tags': tags,
        'image': image,
        'link': f'/projects/{new_id}'
    })
    
    with open(projects_path, 'w') as f:
        json.dump(projects, f, indent=2)
    
    print(f"✅ Added project: {title}")

if __name__ == '__main__':
    # Example usage
    update_project(
        title="New Project",
        description="Project description",
        tags=["Python", "ML"],
        image="/static/images/new-project.png"
    )
```

---

## Quick Reference

### File Locations

- **Current HTML:** `app/templates/index.html`
- **Profile Section:** Lines ~115-212
- **Projects Section:** Lines ~327-586
- **Skills Section:** Lines ~217-250
- **About Section:** Lines ~209-212

### Image Locations

- **Profile Photo:** `app/static/images/mypic.jpg`
- **Project Images:** `app/static/images/header.png` (currently reused)
- **Favicon:** `app/static/images/favicon.png`

### Deployment

After making changes:

1. Test locally
2. Commit changes
3. Push to GitHub
4. GitHub Actions will auto-deploy
5. Check site at https://hahuy.site

---

## Headless CMS Integration (Option 3)

The site now supports Headless CMS integration for advanced content management. Supported CMS platforms:

- **Strapi** (self-hosted)
- **Contentful** (hosted)
- **Sanity** (hosted)

### Configuration

Set the following environment variables:

```bash
CONTENT_SOURCE=cms_with_json_fallback  # or 'cms' for CMS-only
CMS_TYPE=strapi  # or 'contentful', 'sanity', 'none'
CMS_API_URL=https://your-cms-url.com
CMS_API_KEY=your-api-key
```

### CMS-Specific Configuration

**For Contentful:**
```bash
CMS_SPACE_ID=your-space-id
CMS_ENVIRONMENT=master
```

**For Sanity:**
```bash
CMS_PROJECT_ID=your-project-id
CMS_DATASET=production
```

### Content Priority

When `CONTENT_SOURCE=cms_with_json_fallback`:
1. Try to load from CMS
2. If CMS fails or is unavailable, fallback to JSON files
3. This ensures the site always works even if CMS is down

### Syncing CMS to JSON

Use the sync script to backup CMS content to JSON:

```bash
python scripts/sync_cms.py
```

This creates JSON backups of all CMS content, useful for:
- Version control
- Fallback when CMS is unavailable
- Local development

---

## Contact Form (Option 2 - SQLite)

The contact form uses SQLite database to store submissions.

### Submitting Contact Forms

Send POST request to `/contact`:

```json
{
  "name": "Your Name",
  "email": "your@email.com",
  "message": "Your message here"
}
```

### Viewing Submissions

Submissions are stored in the database. Access via:
- Database file: `instance/portfolio.db`
- Model: `ContactSubmission` in `app/database/models.py`

---

*For structural improvements, see `STRUCTURE_RECOMMENDATIONS.md`*

