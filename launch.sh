#!/bin/bash
# Red Heifer Watch - Launch Script

echo "🔥 Launching Red Heifer Watch..."
echo "📍 Starting from: $(pwd)"
echo ""

# Check if index.html exists
if [ ! -f "index.html" ]; then
    echo "❌ index.html not found!"
    exit 1
fi

# Start the server
echo "🚀 Starting Python HTTP server on port 8000..."
echo "🌐 Open your browser and go to: http://localhost:8000"
echo ""
echo "🎯 What you'll see:"
echo "   • Cyberpunk landing page with 'PROPHECY UNFOLDS'"
echo "   • Floating particles and glitch effects"
echo "   • Real-time countdown and live stats"
echo "   • Click 'ENTER SITE' to access main application"
echo ""
echo "🛑 Press Ctrl+C to stop the server"
echo ""

# Start the server
python3 -m http.server 8000