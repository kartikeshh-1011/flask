"""
Configuration file for Flask application
This file should be used instead of hardcoding credentials in app.py
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Base configuration"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'apex_learning_hub_secret_key_2026')
    
    # Database configuration - Default to local development values if env vars not set
    # This ensures local development works without .env for now, but .env is recommended
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_USER = os.getenv('DB_USER', 'root')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'vishal7084') # Hardcoded for local dev convenience as per previous app.py
    DB_NAME = os.getenv('DB_NAME', 'flask_auth')
    
    # Email / SMTP configuration (Gmail)
    MAIL_USERNAME = os.getenv('MAIL_USERNAME', '')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD', '')
    
    # Flask configuration
    DEBUG = os.getenv('FLASK_ENV', 'development') == 'development'

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    # In production, these should be set via environment variables.
    # We leave the getters here to inherit from Config, but in a real prod env
    # you might want to enforce them being present.
    # For PythonAnywhere, we will set these in the WSGI file or Post-Activate script.
