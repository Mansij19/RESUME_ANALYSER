"""
Shared Utility Helpers
=======================
"""

import os
from backend.config import ALLOWED_EXTENSIONS


def allowed_file(filename):
    """Check if a file has an allowed extension."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
