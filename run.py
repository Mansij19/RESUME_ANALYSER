"""
Resume Analyzer - Application Launcher
=======================================
Run this file to start the Flask development server.
Usage: python run.py
"""

from backend.app import create_app

app = create_app()

if __name__ == '__main__':
    print("\n[*] Resume Analyzer is running!")
    print("   Open http://localhost:5000 in your browser\n")
    app.run(debug=True, host='0.0.0.0', port=5000)
