#!/usr/bin/env python3
"""
Test script for the E-commerce Microsite Generator
"""

import os
import sys
sys.path.append('/Users/muhammadusafbaig/site generator')

from app import app, db

def init_database():
    """Initialize the database with tables"""
    with app.app_context():
        # Create all tables
        db.create_all()
        print("✓ Database initialized successfully!")
        
def test_application():
    """Test basic application functionality"""
    print("🚀 Testing E-commerce Microsite Generator...")
    
    # Test 1: Initialize database
    try:
        init_database()
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        return False
    
    # Test 2: Check required directories
    required_dirs = [
        'templates',
        'static/css',
        'static/js', 
        'static/uploads',
        'sites',
        'templates/microsite_themes/minimal',
        'templates/microsite_themes/modern', 
        'templates/microsite_themes/fancy'
    ]
    
    for directory in required_dirs:
        if os.path.exists(directory):
            print(f"✓ Directory exists: {directory}")
        else:
            print(f"❌ Missing directory: {directory}")
            return False
    
    # Test 3: Check required template files
    required_templates = [
        'templates/index.html',
        'templates/preview.html',
        'templates/microsite_themes/minimal/index.html',
        'templates/microsite_themes/minimal/products.html',
        'templates/microsite_themes/minimal/about.html',
        'templates/microsite_themes/minimal/style.css',
        'templates/microsite_themes/modern/index.html',
        'templates/microsite_themes/fancy/index.html'
    ]
    
    for template in required_templates:
        if os.path.exists(template):
            print(f"✓ Template exists: {template}")
        else:
            print(f"❌ Missing template: {template}")
            return False
    
    # Test 4: Check static files
    static_files = [
        'static/css/main.css',
        'static/js/main.js'
    ]
    
    for static_file in static_files:
        if os.path.exists(static_file):
            print(f"✓ Static file exists: {static_file}")
        else:
            print(f"❌ Missing static file: {static_file}")
            return False
    
    print("\n🎉 All tests passed! The application is ready to run.")
    print("\nTo start the application:")
    print('1. Run: "/Users/muhammadusafbaig/site generator/.venv/bin/python" app.py')
    print("2. Open your browser and go to: http://127.0.0.1:5000")
    print("\nFeatures available:")
    print("• Create microsites with business information and products")
    print("• Upload logos and product images")
    print("• Choose from 3 themes: Minimal, Modern, and Fancy")
    print("• Preview generated microsites")
    print("• Download microsites as ZIP files")
    
    return True

if __name__ == "__main__":
    test_application()