#!/bin/bash

echo "========================================="
echo "Fixing Frontend Story Display"
echo "========================================="
echo ""

# Backup
cp frontend/index.html frontend/index.html.backup3
echo "✅ Backup created: frontend/index.html.backup3"

# Fix 1: Simplify x-show condition
echo "Applying Fix 1: Simplifying x-show condition..."
sed -i '' 's/x-show="message\.role === '\''assistant'\'' && message\.results && message\.results\.stories\.length > 0"/x-show="message.role === '\''assistant'\'' \&\& message.results \&\& message.results.stories \&\& message.results.stories.length"/g' frontend/index.html

if [ $? -eq 0 ]; then
    echo "✅ Fix 1 applied"
else
    echo "❌ Fix 1 failed"
fi

# Fix 2: Add debug init to the results div
echo "Applying Fix 2: Adding Alpine.js debug..."
# This is trickier with sed, so we'll create a patch file instead
cat > frontend_debug.patch << 'PATCH'
Find the line (around 192):
    <div 
        x-show="message.role === 'assistant' && message.results && message.results.stories && message.results.stories.length"
        class="space-y-3 mt-4"
        role="region"
        aria-label="Search results"
    >

Add after the opening div:
        <template x-if="message.results">
            <p x-data="{}" x-init="console.log('[Alpine] Results:', message.results); console.log('[Alpine] Stories:', message.results.stories?.length)" 
               style="display:none"></p>
        </template>
PATCH

echo "✅ Debug patch instructions created: frontend_debug.patch"

echo ""
echo "========================================="
echo "Fix Applied!"
echo "========================================="
echo ""
echo "Next steps:"
echo "1. Reload the page with Ctrl+Shift+R (or Cmd+Shift+R)"
echo "2. Search for 'find all marketing stories'"
echo "3. Check browser console for [Alpine] messages"
echo "4. Story cards should now appear"
echo ""
echo "If still not working, check FRONTEND_FIX.md for more solutions"
