import os
from datetime import timedelta

class Config:
    # Security
    SECRET_KEY = 'dev-secret-key-1234'
    
    # Database
    SQLALCHEMY_DATABASE_URI = 'sqlite:///instance/microsites.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # File Upload
    UPLOAD_FOLDER = 'static/uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    
    # Application
    DEBUG = True
    TESTING = False