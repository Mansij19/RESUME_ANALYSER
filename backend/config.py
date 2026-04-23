"""
Configuration settings for the Resume Analyzer application.
"""

import os

# Base directory of the project
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Upload settings
if os.environ.get('VERCEL'):
    UPLOAD_FOLDER = '/tmp/uploads'
else:
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')

MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max file size
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'doc'}

# Model paths
MODEL_DIR = os.path.join(BASE_DIR, 'model')
CLASSIFIER_PATH = os.path.join(MODEL_DIR, 'classifier.pkl')
VECTORIZER_PATH = os.path.join(MODEL_DIR, 'tfidf_vectorizer.pkl')

# Frontend paths
TEMPLATE_FOLDER = os.path.join(BASE_DIR, 'frontend', 'templates')
STATIC_FOLDER = os.path.join(BASE_DIR, 'frontend', 'static')

# Secret key for sessions
SECRET_KEY = 'resume-analyzer-secret-key-change-in-production'
