#!/bin/bash
# Red Heifer Watch - Automated News Updates
# This script should be run periodically to keep the news feed updated

# Set the script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd "$SCRIPT_DIR"

# Create log file with timestamp
LOG_FILE="update_log_$(date +%Y%m%d).log"

# Function to log messages
log_message() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" >> "$LOG_FILE"
}

echo "🔄 Starting Red Heifer Watch automated updates..."
log_message "Starting automated news update process"

# Run the Python news update script
python3 update_news.py >> "$LOG_FILE" 2>&1

# Check if the update was successful
if [ $? -eq 0 ]; then
    echo "✅ News update completed successfully!"
    log_message "News update completed successfully"
else
    echo "❌ News update failed!"
    log_message "ERROR: News update failed"
    exit 1
fi

# Optional: Clean up old log files (keep last 7 days)
find . -name "update_log_*.log" -type f -mtime +7 -delete

echo "📊 Update process completed at $(date)"
log_message "Update process completed"