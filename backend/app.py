"""
Flask Application Factory
===========================
Creates and configures the Flask app instance,
registers blueprints, and sets up required directories.
"""

import os
from flask import Flask
from backend.config import (
    UPLOAD_FOLDER, MAX_CONTENT_LENGTH, SECRET_KEY,
    TEMPLATE_FOLDER, STATIC_FOLDER
)
import streamlit as st

st.title("My Project")
st.write("Hello, this is my app")


def create_app():
    """Create and configure the Flask application."""

    app = Flask(
        __name__,
        template_folder=TEMPLATE_FOLDER,
        static_folder=STATIC_FOLDER
    )

    # --- Configuration ---
    app.config['SECRET_KEY'] = SECRET_KEY
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

    # --- Ensure upload directory exists ---
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    # --- Register Blueprints ---
    from backend.routes.resume import resume_bp
    from backend.routes.report import report_bp

    app.register_blueprint(resume_bp)
    app.register_blueprint(report_bp)

    return app
