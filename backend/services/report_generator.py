"""
PDF Report Generator Service
==============================
Generates a downloadable PDF report of the resume analysis results.
"""

from fpdf import FPDF


class ResumeReport(FPDF):
    """Custom PDF class with header and footer."""

    def header(self):
        self.set_font('Helvetica', 'B', 22)
        self.set_text_color(88, 86, 214)
        self.cell(0, 15, 'Resume Analysis Report', new_x="LMARGIN", new_y="NEXT", align='C')
        self.set_draw_color(88, 86, 214)
        self.set_line_width(0.5)
        self.line(10, 28, 200, 28)
        self.ln(15)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f'Resume Analyzer | Page {self.page_no()}/{{nb}}', align='C')

    def section_title(self, title):
        """Add a styled section title."""
        self.ln(5)
        self.set_font('Helvetica', 'B', 14)
        self.set_text_color(44, 62, 80)
        self.cell(0, 10, title, new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(200, 200, 200)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(3)

    def body_text(self, text):
        """Add body text."""
        self.set_font('Helvetica', '', 10)
        self.set_text_color(60, 60, 60)
        self.multi_cell(0, 6, text)


def generate_pdf(results):
    """
    Generate a PDF report from analysis results.

    Args:
        results (dict): Analysis results containing quality, skills,
                        suggestions, corrections, and jd_match.

    Returns:
        bytes: PDF file content.
    """
    pdf = ResumeReport()
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # --- Quality Score ---
    pdf.section_title('Resume Quality Score')
    quality = results.get('quality', {})
    label = quality.get('label', 'N/A')
    score = quality.get('score', 0)
    conf = quality.get('confidence', 0)
    pdf.set_font('Helvetica', 'B', 12)
    pdf.set_text_color(88, 86, 214)
    pdf.cell(0, 8, f'{label} - {score}/100 (Confidence: {conf}%)',
             new_x="LMARGIN", new_y="NEXT")

    # --- Extracted Skills ---
    pdf.section_title('Extracted Skills')
    skills = results.get('skills', {})
    if skills:
        for category, skill_list in skills.items():
            pdf.set_font('Helvetica', 'B', 10)
            pdf.set_text_color(44, 62, 80)
            pdf.cell(0, 7, f'  {category}:', new_x="LMARGIN", new_y="NEXT")
            pdf.set_font('Helvetica', '', 10)
            pdf.set_text_color(80, 80, 80)
            pdf.cell(0, 6, f'    {", ".join(skill_list)}',
                     new_x="LMARGIN", new_y="NEXT")
    else:
        pdf.body_text('No skills detected.')

    # --- Suggestions ---
    pdf.section_title('Improvement Suggestions')
    for sug in results.get('suggestions', []):
        pdf.set_font('Helvetica', 'B', 10)
        pdf.set_text_color(44, 62, 80)
        pdf.cell(0, 7, f'  {sug.get("icon", ">")} {sug["title"]}',
                 new_x="LMARGIN", new_y="NEXT")
        pdf.set_font('Helvetica', '', 9)
        pdf.set_text_color(100, 100, 100)
        pdf.multi_cell(0, 5, f'    {sug["detail"]}')
        pdf.ln(1)

    # --- Grammar Corrections ---
    corrections = results.get('corrections', [])
    if corrections:
        pdf.section_title('Grammar & Style Issues')
        for c in corrections:
            pdf.set_font('Helvetica', 'B', 10)
            pdf.set_text_color(192, 57, 43)
            pdf.multi_cell(0, 6, f'  Issue: {c["issue"]}')
            pdf.set_font('Helvetica', '', 9)
            pdf.set_text_color(39, 174, 96)
            pdf.multi_cell(0, 5, f'  Fix: {c["suggestion"]}')
            pdf.ln(2)

    # --- JD Match ---
    jd_match = results.get('jd_match')
    if jd_match:
        pdf.section_title('Job Description Match')
        pdf.set_font('Helvetica', 'B', 12)
        pdf.set_text_color(88, 86, 214)
        pdf.cell(0, 8, f'Match Score: {jd_match["score"]}%',
                 new_x="LMARGIN", new_y="NEXT")
        missing = jd_match.get('missing_skills', [])
        if missing:
            pdf.set_font('Helvetica', 'B', 10)
            pdf.set_text_color(192, 57, 43)
            pdf.cell(0, 7, '  Missing Skills from JD:',
                     new_x="LMARGIN", new_y="NEXT")
            pdf.set_font('Helvetica', '', 10)
            pdf.cell(0, 6, f'    {", ".join(missing)}',
                     new_x="LMARGIN", new_y="NEXT")

    return pdf.output()
