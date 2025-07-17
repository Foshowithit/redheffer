#!/usr/bin/env python3
"""
Update news and inject into HTML files
This script fetches live news and updates the JavaScript in news.html
"""

import json
import subprocess
import os
from datetime import datetime
from news_fetcher import RedHeiferNewsFetcher

def run_news_fetcher():
    """Run the news fetcher and return the JSON data"""
    try:
        fetcher = RedHeiferNewsFetcher()
        return fetcher.save_to_json()
    except Exception as e:
        print(f"Error running news fetcher: {e}")
        return None

def convert_to_js_format(news_data):
    """Convert news data to JavaScript format"""
    if not news_data or 'articles' not in news_data:
        return None
    
    js_articles = []
    for i, article in enumerate(news_data['articles']):
        js_article = {
            'id': i + 100,  # Start from 100 to avoid conflicts with static articles
            'title': article['title'],
            'date': format_date(article['pub_date']),
            'category': article['category'],
            'excerpt': article['description'],
            'content': article['description'] + f" (Source: {article['source']})",
            'urgency': article['urgency'],
            'source': article['source'],
            'is_live': True
        }
        js_articles.append(js_article)
    
    return js_articles

def format_date(date_str):
    """Format date string for display"""
    try:
        # Try to parse the date and reformat it
        if 'UTC' in date_str:
            dt = datetime.strptime(date_str, '%a, %d %b %Y %H:%M:%S %Z')
        else:
            dt = datetime.strptime(date_str, '%a, %d %b %Y %H:%M:%S UTC')
        return dt.strftime('%B %d, %Y')
    except:
        return date_str.split(',')[1].strip() if ',' in date_str else date_str

def update_news_html():
    """Update the news.html file with live news data"""
    print("📰 Updating news HTML with live data...")
    
    # Fetch live news
    news_data = run_news_fetcher()
    if not news_data:
        print("❌ Failed to fetch news data")
        return False
    
    # Convert to JavaScript format
    js_articles = convert_to_js_format(news_data)
    if not js_articles:
        print("❌ Failed to convert news data")
        return False
    
    # Read current news.html
    try:
        with open('news.html', 'r', encoding='utf-8') as f:
            html_content = f.read()
    except FileNotFoundError:
        print("❌ news.html not found")
        return False
    
    # Find the newsArticles array and replace it
    start_marker = "const newsArticles = ["
    end_marker = "];"
    
    start_idx = html_content.find(start_marker)
    if start_idx == -1:
        print("❌ Could not find newsArticles array in HTML")
        return False
    
    end_idx = html_content.find(end_marker, start_idx)
    if end_idx == -1:
        print("❌ Could not find end of newsArticles array")
        return False
    
    # Generate new JavaScript array
    js_array = "const newsArticles = [\n"
    for article in js_articles:
        js_array += f"""            {{
                id: {article['id']},
                title: "{article['title'].replace('"', '\\"')}",
                date: "{article['date']}",
                category: "{article['category']}",
                excerpt: "{article['excerpt'].replace('"', '\\"')}",
                content: "{article['content'].replace('"', '\\"')}",
                urgency: "{article['urgency']}",
                source: "{article['source']}",
                isLive: {str(article['is_live']).lower()}
            }},
"""
    js_array = js_array.rstrip(',\n') + "\n        ];"
    
    # Replace the array in HTML
    new_html = html_content[:start_idx] + js_array + html_content[end_idx + len(end_marker):]
    
    # Add last updated timestamp
    timestamp = datetime.now().strftime('%B %d, %Y at %I:%M %p')
    timestamp_marker = '<p class="text-center text-gray-400 mt-2">Last updated:'
    if timestamp_marker in new_html:
        # Update existing timestamp
        start = new_html.find(timestamp_marker)
        end = new_html.find('</p>', start) + 4
        new_timestamp = f'<p class="text-center text-gray-400 mt-2">Last updated: {timestamp}</p>'
        new_html = new_html[:start] + new_timestamp + new_html[end:]
    else:
        # Add timestamp after Community Pulse section
        pulse_end = new_html.find('</section>')
        if pulse_end != -1:
            timestamp_html = f'\n        <div class="text-center mt-8"><p class="text-center text-gray-400 mt-2">Last updated: {timestamp}</p></div>'
            new_html = new_html[:pulse_end + 10] + timestamp_html + new_html[pulse_end + 10:]
    
    # Write updated HTML
    try:
        with open('news.html', 'w', encoding='utf-8') as f:
            f.write(new_html)
        print(f"✅ Successfully updated news.html with {len(js_articles)} live articles")
        print(f"📅 Last updated: {timestamp}")
        return True
    except Exception as e:
        print(f"❌ Error writing HTML file: {e}")
        return False

if __name__ == "__main__":
    print("🔄 Starting news update process...")
    success = update_news_html()
    if success:
        print("🎉 News update completed successfully!")
    else:
        print("💥 News update failed!")