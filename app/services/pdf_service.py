"""
Service for handling PDF text extraction.
"""
from pathlib import Path
from PyPDF2 import PdfReader
from typing import Optional
import unicodedata

class PDFService:
    """
    Service for handling PDF operations.
    """
    
    def extract_text(self, file_path: Path) -> str:
        """
        Extract text from a PDF file.

        Args:
            file_path (Path): Path to the PDF file

        Returns:
            str: Extracted text from the PDF

        Raises:
            Exception: If PDF processing fails
        """
        try:
            reader = PdfReader(file_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"

            text =text.replace("�", "ti")
            return text.strip()
        except Exception as e:
            raise Exception(f"Failed to extract text from PDF: {str(e)}") 