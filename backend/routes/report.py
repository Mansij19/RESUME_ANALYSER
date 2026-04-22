"""
Report Download Route
======================
Generates and serves a PDF report of the analysis results.
"""

from flask import Blueprint, send_file, abort
import io

from backend.services.report_generator import generate_pdf
from backend.routes.resume import get_stored_results

report_bp = Blueprint('report', __name__)


@report_bp.route('/download-report/<result_id>')
def download_report(result_id):
    """
    Generate and download a PDF report for a given result ID.

    Args:
        result_id: UUID of the stored analysis results.
    """
    results = get_stored_results(result_id)
    if not results:
        abort(404, description="Analysis results not found or expired.")

    pdf_bytes = generate_pdf(results)
    pdf_buffer = io.BytesIO(pdf_bytes)
    pdf_buffer.seek(0)

    return send_file(
        pdf_buffer,
        mimetype='application/pdf',
        as_attachment=True,
        download_name='resume_analysis_report.pdf'
    )
