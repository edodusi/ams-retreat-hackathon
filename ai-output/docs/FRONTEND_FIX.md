# Frontend Display Fix

## Problem
Backend returns stories correctly but frontend doesn't display them.

## Root Cause
The `x-show` condition might not be evaluating correctly in Alpine.js, or there's a timing issue.

## Quick Test

Open browser console (F12) and check for [DEBUG] messages when you search.

You should see:
```
[DEBUG] API Response: {message: "...", results: {...}}
[DEBUG] Has results? true
[DEBUG] Stories count: 10
[DEBUG] First story: {body: "...", name: "...", ...}
```

If you see these, the data is reaching the frontend correctly.

## Fixes to Try

### Fix 1: Simplify the x-show condition

Open `frontend/index.html` and find line ~192:

**Current:**
```html
<div x-show="message.role === 'assistant' && message.results && message.results.stories.length > 0"
```

**Change to:**
```html
<div x-show="message.role === 'assistant' && message.results && message.results.stories && message.results.stories.length"
```

### Fix 2: Force display for debugging

Temporarily change to always show when results exist:

```html
<div x-show="message.results"
```

This will show the section even if stories array is empty, helping debug.

### Fix 3: Add Alpine.js debug

Add this attribute to the div:

```html
<div x-show="message.role === 'assistant' && message.results && message.results.stories.length > 0"
     x-data="{}"
     x-init="console.log('[Alpine] message:', message); console.log('[Alpine] has results:', !!message.results)"
```

### Fix 4: Check Alpine.js version

In browser console, check:
```javascript
Alpine.version
```

Should be 3.x.x. If different, might need version-specific syntax.

## Manual Fix Instructions

1. **Backup the file:**
```bash
cp frontend/index.html frontend/index.html.backup2
```

2. **Edit line 192** (the x-show condition)

3. **Reload the page** (Ctrl+Shift+R / Cmd+Shift+R)

4. **Test again** with "find all marketing stories"

## Automated Fix Script

Run this:

```bash
#!/bin/bash
cp frontend/index.html frontend/index.html.backup2

# Replace the x-show condition with simplified version
sed -i.tmp 's/x-show="message.role === '\''assistant'\'' && message.results && message.results.stories.length > 0"/x-show="message.role === '\''assistant'\'' && message.results \&\& message.results.stories \&\& message.results.stories.length"/g' frontend/index.html

echo "✅ Fixed x-show condition"
echo "Reload the page and test again"
```

Save as `fix_frontend_xshow.sh` and run:
```bash
bash fix_frontend_xshow.sh
```

## Verification

After applying fix:

1. Start server: `python -m uvicorn backend.main:app --reload`
2. Open: http://localhost:8000/frontend/index.html
3. Open DevTools (F12) → Console
4. Search: "find all marketing stories"
5. Look for:
   - [DEBUG] messages in console
   - Story cards appearing below response
   - Any JavaScript errors

## Alternative: Force Render

If Alpine.js is the issue, you can bypass it temporarily by checking if stories render with vanilla JS:

Add this at the end of the sendMessage function (line ~520):

```javascript
// Debug: Force render stories
if (data.results && data.results.stories) {
    console.log('[FORCE RENDER] Attempting to render', data.results.stories.length, 'stories');
}
```

## Common Issues

### Issue: x-show evaluates to false even with data
**Solution:** Alpine.js reactivity issue. Try `x-show` → `x-if` or vice versa.

### Issue: Stories array is undefined
**Check:** Browser console for actual structure of `message.results`

### Issue: Template not rendering
**Check:** Alpine.js loaded correctly (check Network tab)

---

**Next Step:** Try Fix 1 (simplify x-show) and reload the page.
