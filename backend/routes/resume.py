"""
Resume Routes Blueprint
========================
Handles all main page routes: home, upload, and analysis.
"""

import json
import uuid
from flask import Blueprint, render_template, request, redirect, url_for, flash, session

from backend.utils.helpers import allowed_file
from backend.services.file_parser import extract_text
from backend.services.preprocessor import preprocess
from backend.services.skill_extractor import extract_skills
from backend.services.quality_classifier import classify
from backend.services.grammar_checker import check_grammar, suggest_improvements
from backend.services.jd_matcher import match as jd_match

resume_bp = Blueprint('resume', __name__)

# In-memory store for analysis results (keyed by session result_id)
_results_store = {}


@resume_bp.route('/')
def home():
    """Render the landing / home page."""
    return render_template('index.html')


@resume_bp.route('/upload')
def upload():
    """Render the upload / paste resume page."""
    return render_template('upload.html')


@resume_bp.route('/analyze', methods=['POST'])
def analyze():
    """
    Main analysis endpoint.

    Accepts either a file upload (PDF/DOCX) or pasted text,
    runs all analysis services, and renders the results page.
    """
    resume_text = ""
    input_method = request.form.get('input_method', 'paste')

    # --- 1. Get resume text ---
    if input_method == 'upload':
        file = request.files.get('resume_file')
        if not file or file.filename == '':
            flash('Please select a file to upload.', 'error')
            return redirect(url_for('resume.upload'))
        if not allowed_file(file.filename):
            flash('Invalid file type. Please upload a PDF or DOCX file.', 'error')
            return redirect(url_for('resume.upload'))
        try:
            resume_text = extract_text(file, file.filename)
        except Exception as e:
            flash(f'Error reading file: {str(e)}', 'error')
            return redirect(url_for('resume.upload'))
    else:
        resume_text = request.form.get('resume_text', '').strip()

    if not resume_text or len(resume_text) < 50:
        flash('Please provide a resume with at least 50 characters.', 'error')
        return redirect(url_for('resume.upload'))

    # --- 2. Get optional job description ---
    jd_text = request.form.get('job_description', '').strip()

    # --- 3. Preprocess ---
    cleaned_text, tokens = preprocess(resume_text)

    # --- 4. Extract skills ---
    skills, skill_count = extract_skills(resume_text)

    # --- 5. Classify quality ---
    try:
        quality = classify(cleaned_text)
    except FileNotFoundError:
        quality = {"label": "N/A", "confidence": 0, "score": 50}

    # --- 6. Grammar & suggestions ---
    corrections = check_grammar(resume_text)
    suggestions = suggest_improvements(resume_text)

    # --- 7. JD matching (if provided) ---
    jd_result = None
    if jd_text:
        jd_result = jd_match(resume_text, jd_text)

    # --- 8. Build results ---
    results = {
        "quality": quality,
        "skills": skills,
        "skill_count": skill_count,
        "corrections": corrections,
        "suggestions": suggestions,
        "jd_match": jd_result,
        "resume_preview": resume_text[:500] + ("..." if len(resume_text) > 500 else "")
    }

    # Store results for PDF download
    result_id = str(uuid.uuid4())
    _results_store[result_id] = results

    # Keep only last 20 results in memory
    if len(_results_store) > 20:
        oldest = list(_results_store.keys())[0]
        del _results_store[oldest]

    return render_template('results.html', results=results, result_id=result_id)


def get_stored_results(result_id):
    """Retrieve stored results by ID (used by report route)."""
    return _results_store.get(result_id)
