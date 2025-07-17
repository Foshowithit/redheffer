#!/bin/bash

# Auto-update script for Red Heifer Watch news
# This script should be run via cron every 30 minutes

cd "$(dirname "$0")"

echo "$(date): Starting Red Heifer Watch news update..."

# Run the Python news updater
python3 update_news.py

# Check if git repo and commit changes
if [ -d ".git" ]; then
    # Add changes
    git add news.html live_news.json
    
    # Check if there are changes to commit
    if ! git diff --cached --quiet; then
        # Commit with timestamp
        git commit -m "Auto-update: Live news refresh $(date '+%Y-%m-%d %H:%M')"
        
        # Push to remote (optional - uncomment if you want auto-push)
        # git push
        
        echo "$(date): Changes committed to git"
    else
        echo "$(date): No changes to commit"
    fi
else
    echo "$(date): Not a git repository, skipping commit"
fi

echo "$(date): Red Heifer Watch update completed"