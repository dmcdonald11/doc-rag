"""
Tests for the PDF service.
"""
import pytest
from pathlib import Path
from app.services.pdf_service import PDFService

def test_extract_text_success(tmp_path):
    """
    Test successful text extraction from a PDF.
    """
    # Create a temporary PDF file with some text
    pdf_path = tmp_path / "test.pdf"
    with open(pdf_path, "wb") as f:
        f.write(b"%PDF-1.4\n1 0 obj\n<</Type /Catalog /Pages 2 0 R>>\nendobj\n2 0 obj\n<</Type /Pages /Kids [3 0 R] /Count 1>>\nendobj\n3 0 obj\n<</Type /Page /Parent 2 0 R /Resources <<>> /Contents 4 0 R>>\nendobj\n4 0 obj\n<</Length 44>>\nstream\nBT\n/F1 12 Tf\n100 700 Td\n(Hello World) Tj\nET\nendstream\nendobj\nxref\n0 5\n0000000000 65535 f\n0000000010 00000 n\n0000000056 00000 n\n0000000106 00000 n\n0000000176 00000 n\ntrailer\n<</Size 5/Root 1 0 R>>\nstartxref\n242\n%%EOF")
    
    service = PDFService()
    text = service.extract_text(pdf_path)
    
    assert "Hello World" in text

def test_extract_text_invalid_pdf(tmp_path):
    """
    Test text extraction from an invalid PDF file.
    """
    # Create an invalid PDF file
    pdf_path = tmp_path / "invalid.pdf"
    with open(pdf_path, "wb") as f:
        f.write(b"Not a PDF file")
    
    service = PDFService()
    with pytest.raises(Exception) as exc_info:
        service.extract_text(pdf_path)
    
    assert "Failed to extract text from PDF" in str(exc_info.value)

def test_extract_text_nonexistent_file():
    """
    Test text extraction from a nonexistent file.
    """
    service = PDFService()
    with pytest.raises(Exception) as exc_info:
        service.extract_text(Path("nonexistent.pdf"))
    
    assert "Failed to extract text from PDF" in str(exc_info.value) 