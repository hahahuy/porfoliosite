# Website Checker Tools

This document explains how to use the website checking functions for your portfolio site.

## Quick Commands

### 1. Full Website Check (Recommended)
```bash
python check_website.py check
```
- ✅ Tests server connection
- ✅ Checks all content sections
- ✅ Verifies static files
- ✅ Opens website in browser
- ✅ Shows detailed status report

### 2. Quick Test (No Browser)
```bash
python check_website.py test
```
- ✅ Same checks as above
- ❌ Doesn't open browser
- ⚡ Faster execution

### 3. Just Open Website
```bash
python check_website.py open
```
- 🌐 Opens website in browser
- ⚡ No testing, just opens browser

### 4. Check Server Status
```bash
python check_website.py status
```
- 📊 Quick server status check
- ⚡ Fast response

### 5. Start Server
```bash
python check_website.py start
```
- 🚀 Starts Flask server
- ⌨️ Press Ctrl+C to stop

## What Gets Checked

### Content Checks
- ✅ Profile name (Hà Quang Huy)
- ✅ Skills section (Python, SQL, etc.)
- ✅ Projects section
- ✅ Education section (Coursera, HCMIU)
- ✅ Social media links (LinkedIn, GitHub)
- ✅ Favicon (favicon.png)
- ✅ CSS files (output.css)
- ✅ Vietnam flag content

### Static Files Check
- ✅ `/static/images/favicon.png`
- ✅ `/static/images/mypic.jpg`
- ✅ `/static/images/header.png`
- ✅ `/static/css/output.css`
- ✅ `/static/css/style.css`

## Example Output

```
🔍 Checking your portfolio website...
📍 URL: http://localhost:5000
--------------------------------------------------
📡 Testing server connection...
✅ Server is running successfully!
📊 Status Code: 200
📏 Content Length: 28082 bytes

📋 Content Checks:
   ✅ Profile
   ✅ Skills
   ✅ Projects
   ✅ Social Links
   ✅ Favicon
   ✅ CSS
   ✅ Vietnam Flag

📁 Static Files Check:
   ✅ /static/images/favicon.png
   ✅ /static/images/mypic.jpg
   ✅ /static/images/header.png
   ✅ /static/css/output.css
   ✅ /static/css/style.css

🎯 Overall Status: ✅ ALL GOOD!

🌐 Opening website in browser...
✅ Browser opened!

📝 Summary:
   • Website is accessible at: http://localhost:5000
   • Server is responding correctly
   • Content checks: 8/8 passed
   • Ready for development and testing!
```

## Troubleshooting

### Server Not Running
If you see "Could not connect to server":
1. Start the server: `python server.py`
2. Or use: `python check_website.py start`

### Missing Files
If static files fail:
1. Check that all files exist in `app/static/`
2. Verify file paths in HTML template
3. Restart Flask server

### Content Issues
If content checks fail:
1. Check HTML template for typos
2. Verify content exists in template
3. Check for encoding issues

## Files Created

- `check_website.py` - Main command-line tool
- `tests/test_local.py` - Comprehensive testing functions
- `tests/test_smoke.py` - Basic smoke tests
- `WEBSITE_CHECKER.md` - This documentation

## Usage Tips

1. **Before making changes**: Run `python check_website.py test`
2. **After making changes**: Run `python check_website.py check`
3. **Quick access**: Use `python check_website.py open`
4. **Development**: Keep server running with `python server.py`

Your website is now fully tested and ready for development! 🎉 