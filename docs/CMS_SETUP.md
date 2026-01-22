# Headless CMS Setup Guide

This guide explains how to set up and configure Headless CMS integration for the portfolio site.

## Overview

The portfolio site supports three Headless CMS platforms:
- **Strapi** (self-hosted)
- **Contentful** (hosted)
- **Sanity** (hosted)

## Configuration

### Environment Variables

Add these to your `.env` file:

```bash
# Content source priority
CONTENT_SOURCE=cms_with_json_fallback  # Options: 'json', 'cms', 'cms_with_json_fallback'

# CMS Type
CMS_TYPE=strapi  # Options: 'strapi', 'contentful', 'sanity', 'none'

# Base CMS Configuration
CMS_API_URL=https://your-cms-url.com
CMS_API_KEY=your-api-key-or-token
```

### Strapi Configuration

1. Set up Strapi instance (self-hosted or cloud)
2. Create content types:
   - `profile` (single)
   - `projects` (collection)
   - `skills` (collection)
   - `experiences` (collection)
3. Configure API permissions
4. Get API token from Settings > API Tokens

```bash
CMS_TYPE=strapi
CMS_API_URL=https://your-strapi-instance.com
CMS_API_KEY=your-strapi-api-token
```

### Contentful Configuration

1. Create Contentful account and space
2. Create content models:
   - `profile` (single entry)
   - `project` (content type)
   - `skill` (content type)
   - `experience` (content type)
3. Get Space ID and Access Token

```bash
CMS_TYPE=contentful
CMS_SPACE_ID=your-space-id
CMS_ENVIRONMENT=master
CMS_API_KEY=your-contentful-access-token
```

### Sanity Configuration

1. Create Sanity project
2. Define schema for:
   - `profile` (document)
   - `project` (document)
   - `skill` (document)
   - `experience` (document)
3. Get Project ID and API token

```bash
CMS_TYPE=sanity
CMS_PROJECT_ID=your-project-id
CMS_DATASET=production
CMS_API_KEY=your-sanity-api-token
```

## Content Structure

### Profile (Single Entry)

```json
{
  "name": "Hà Quang Huy",
  "title": "Entry Level Data analysis | MLOps",
  "location": "Hồ Chí Minh, VN",
  "bio": "Your bio text...",
  "social": {
    "linkedin": "https://...",
    "github": "https://...",
    "kaggle": "https://...",
    "email": "email@example.com"
  },
  "profile_image": "/static/images/mypic.jpg"
}
```

### Projects (Collection)

```json
[
  {
    "id": 0,
    "title": "Project Title",
    "description": "Short description...",
    "image": "/static/images/project.png",
    "tags": ["Python", "ML"],
    "link": "/projects/0"
  }
]
```

### Skills (Collection)

```json
["Python", "SQL", "R", "PowerBI"]
```

### Experience (Collection)

```json
[
  {
    "title": "Job Title",
    "company": "Company Name",
    "start_date": "2020-01",
    "end_date": "2022-12",
    "description": "Job description..."
  }
]
```

## Testing CMS Connection

1. Set `CONTENT_SOURCE=cms` (temporary, for testing)
2. Start the application
3. Check logs for CMS connection status
4. Visit homepage - should load from CMS
5. If errors, check:
   - API URL is correct
   - API key is valid
   - Content types match expected structure

## Fallback Strategy

Recommended: Use `CONTENT_SOURCE=cms_with_json_fallback`

This ensures:
- Primary: Load from CMS
- Fallback: Use JSON files if CMS fails
- Site always works even if CMS is down

## Syncing CMS to JSON

Regularly sync CMS content to JSON for backup:

```bash
python scripts/sync_cms.py
```

This creates JSON backups in `app/content/` directory.

## Troubleshooting

### CMS Not Loading

1. Check `CMS_TYPE` is set correctly
2. Verify `CMS_API_URL` and `CMS_API_KEY`
3. Check CMS-specific settings (Space ID, Project ID, etc.)
4. Review application logs for errors
5. Test CMS API directly with curl/Postman

### Content Not Appearing

1. Verify content exists in CMS
2. Check content type names match expected structure
3. Ensure API permissions allow read access
4. Check field names match expected structure

### Fallback Not Working

1. Ensure JSON files exist in `app/content/`
2. Verify JSON structure matches expected format
3. Check file permissions

## Best Practices

1. **Always use fallback**: Set `CONTENT_SOURCE=cms_with_json_fallback`
2. **Regular backups**: Run `sync_cms.py` regularly
3. **Version control**: Commit JSON files to git
4. **Test locally**: Use JSON for local development
5. **Monitor logs**: Watch for CMS connection errors

---

For more information, see `CONTENT_GUIDE.md` and `STRUCTURE_RECOMMENDATIONS.md`.
