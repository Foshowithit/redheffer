# Red Heifer Watch - Automation Setup Guide

## Automated News Updates

This guide will help you set up automatic news updates for the Red Heifer Watch website.

### Prerequisites

1. Python 3 installed
2. All required Python packages (install with: `pip install requests feedparser`)
3. The website files in a directory accessible to your system

### Manual Updates

To manually update the news:

```bash
# From the project directory
python3 update_news.py
```

Or use the automated script:

```bash
./run_updates.sh
```

### Automatic Updates (Cron Job)

To set up automatic updates every 2 hours:

1. Open your crontab:
   ```bash
   crontab -e
   ```

2. Add this line (replace `/path/to/red-heifer-watch` with your actual path):
   ```bash
   0 */2 * * * cd /path/to/red-heifer-watch && ./run_updates.sh
   ```

### Recommended Update Schedules

- **Every 2 hours**: `0 */2 * * *`
- **Every 4 hours**: `0 */4 * * *`
- **Every 6 hours**: `0 */6 * * *`
- **Daily at 6 AM**: `0 6 * * *`
- **Twice daily (6 AM & 6 PM)**: `0 6,18 * * *`

### Log Files

The automation script creates daily log files:
- Format: `update_log_YYYYMMDD.log`
- Location: Project directory
- Retention: 7 days (automatically cleaned up)

### Troubleshooting

1. **Permission Issues**: Make sure the script is executable:
   ```bash
   chmod +x run_updates.sh
   ```

2. **Python Path Issues**: If Python isn't found, update the script to use the full path:
   ```bash
   /usr/bin/python3 update_news.py
   ```

3. **Check Logs**: Review the log files for error messages

### Testing

Test the automation before setting up cron:

```bash
# Test manual update
python3 update_news.py

# Test automation script
./run_updates.sh

# Check if cron job would work
cd /path/to/red-heifer-watch && ./run_updates.sh
```

### Security Notes

- The news fetcher uses public RSS feeds
- No sensitive data is stored or transmitted
- All updates are logged for transparency
- The system uses fallback articles if live feeds fail

### Monitoring

Monitor the system by:
1. Checking the website timestamp
2. Reviewing log files
3. Verifying news articles are updating

For questions or issues, check the log files first, then verify your network connection and Python installation.