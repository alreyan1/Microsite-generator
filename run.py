#!/usr/bin/env python3
"""
Run script for E-commerce Microsite Generator
"""

import os
import sys

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db

def run_app():
    """Run the Flask application"""
    print("🚀 Starting E-commerce Microsite Generator...")
    print("📍 Access the application at: http://127.0.0.1:5000")
    print("🛑 Press Ctrl+C to stop the server")
    print("-" * 50)
    
    # Ensure database is initialized
    with app.app_context():
        db.create_all()
    
    # Run the application
    app.run(host='127.0.0.1', port=5000, debug=True)

if __name__ == "__main__":
    run_app()