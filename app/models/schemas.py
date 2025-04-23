"""
Pydantic models for the application.
"""
from pydantic import BaseModel
from typing import Optional, Dict, Any
from services.mcp_service import MCPResponse

class FileResponse(BaseModel):
    """
    Response model for file upload and processing.
    """
    filename: str
    status: str
    message: str
    mcp_response: Optional[MCPResponse] = None 