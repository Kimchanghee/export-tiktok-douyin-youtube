"""
Simple script to start the web server on a specific port
"""
import os
import sys

# Set port before importing the app
os.environ['PORT'] = '8081'

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import and run the app
from web.app import app, cleanup_old_downloads

if __name__ == '__main__':
    # Run cleanup before starting
    cleanup_old_downloads()

    # Get port from environment
    port = int(os.environ.get('PORT', 8081))

    print(f"Starting server on port {port}...")

    # Run app
    app.run(
        host='0.0.0.0',
        port=port,
        debug=False
    )
