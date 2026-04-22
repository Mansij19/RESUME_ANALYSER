"""
File Parser Service
====================
Extracts text content from uploaded PDF and DOCX files.
"""

import PyPDF2
import docx


def extract_text_from_pdf(file_storage):
    """
    Extract text from a PDF file.

    Args:
        file_storage: A file-like object (werkzeug FileStorage or file handle).

    Returns:
        str: Extracted text from all pages.
    """
    reader = PyPDF2.PdfReader(file_storage)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text.strip()


def extract_text_from_docx(file_storage):
    """
    Extract text from a DOCX file.

    Args:
        file_storage: A file-like object (werkzeug FileStorage or file handle).

    Returns:
        str: Extracted text from all paragraphs.
    """
    doc = docx.Document(file_storage)
    text = ""
    for paragraph in doc.paragraphs:
        if paragraph.text.strip():
            text += paragraph.text + "\n"
    return text.strip()


def extract_text(file_storage, filename):
    """
    Extract text from a file based on its extension.

    Args:
        file_storage: The uploaded file object.
        filename: Original filename (used to detect extension).

    Returns:
        str: Extracted text content.

    Raises:
        ValueError: If the file type is not supported.
    """
    ext = filename.rsplit('.', 1)[-1].lower()

    if ext == 'pdf':
        return extract_text_from_pdf(file_storage)
    elif ext in ('docx', 'doc'):
        return extract_text_from_docx(file_storage)
    else:
        raise ValueError(f"Unsupported file type: .{ext}")
