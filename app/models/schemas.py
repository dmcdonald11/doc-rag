"""
Pydantic models for the application.
"""
from pydantic import BaseModel
from typing import Optional, Dict, Any
from services.lightrag_service import LightRAGResponse

class FileResponse(BaseModel):
    """
    Response model for file upload and processing.
    """
    filename: str
    status: str
    message: str
    lightrag_response: Optional[LightRAGResponse] = None 