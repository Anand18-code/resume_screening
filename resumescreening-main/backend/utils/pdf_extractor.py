"""PDF text extraction utility using pdfplumber."""

import io
from typing import Any, Union
import pdfplumber


def extract_text_from_pdf(file_obj: Any) -> str:
    """Extracts raw text from a PDF file-like object or file path.
    
    Args:
        file_obj: A file path, UploadFile.file, BytesIO, or file-like object.
        
    Returns:
        Extracted text as a string.
        
    Raises:
        ValueError: If PDF parsing fails or results in empty text.
    """
    text = ""
    try:
        with pdfplumber.open(file_obj) as pdf:
            if not pdf.pages:
                raise ValueError("The uploaded PDF has 0 pages.")
            for idx, page in enumerate(pdf.pages):
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        if isinstance(e, ValueError):
            raise
        raise ValueError(f"Failed to read PDF: {str(e)}")

    if not text.strip():
        raise ValueError(
            "No readable text could be extracted from the PDF. "
            "Please ensure the PDF contains selectable text (not scanned images)."
        )

    return text.strip()


def extract_text_from_pdf_bytes(pdf_bytes: bytes) -> str:
    """Extracts text from PDF raw bytes.
    
    Args:
        pdf_bytes: Raw binary bytes of the PDF file.
        
    Returns:
        Extracted text string.
    """
    if not pdf_bytes:
        raise ValueError("Uploaded PDF file is empty (0 bytes).")
    stream = io.BytesIO(pdf_bytes)
    return extract_text_from_pdf(stream)
