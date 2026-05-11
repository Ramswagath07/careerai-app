"""
CareerAI — Resume Text Extraction
Supports PDF (pdfplumber), DOCX (python-docx), and plain TXT.
"""

import io
import logging
import re
from pathlib import Path

logger = logging.getLogger(__name__)

def extract_text(file_bytes: bytes, filename: str) -> str:
    ext = Path(filename).suffix.lower().lstrip(".")
    try:
        if ext == "pdf":
            return _extract_pdf(file_bytes)
        elif ext in ("doc", "docx"):
            return _extract_docx(file_bytes)
        elif ext == "txt":
            return file_bytes.decode("utf-8", errors="ignore")
        else:
            raise ValueError(f"Unsupported file type: {ext}")
    except Exception as e:
        logger.error(f"Text extraction failed for {filename}: {e}")
        return ""

def _extract_pdf(data: bytes) -> str:
    try:
        import pdfplumber
        text_pages = []
        with pdfplumber.open(io.BytesIO(data)) as pdf:
            for page in pdf.pages:
                t = page.extract_text()
                if t:
                    text_pages.append(t)
        return "\n".join(text_pages)
    except ImportError:
        pass

    # Fallback: PyPDF2
    try:
        import PyPDF2
        reader = PyPDF2.PdfReader(io.BytesIO(data))
        return "\n".join(
            page.extract_text() or "" for page in reader.pages
        )
    except Exception as e:
        logger.error(f"PDF extraction error: {e}")
        return ""

def _extract_docx(data: bytes) -> str:
    try:
        from docx import Document
        doc = Document(io.BytesIO(data))
        return "\n".join(p.text for p in doc.paragraphs if p.text.strip())
    except Exception as e:
        logger.error(f"DOCX extraction error: {e}")
        return ""

def count_pages(file_bytes: bytes, filename: str) -> int:
    ext = Path(filename).suffix.lower().lstrip(".")
    if ext == "pdf":
        try:
            import pdfplumber
            with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
                return len(pdf.pages)
        except:
            pass
    return 1
