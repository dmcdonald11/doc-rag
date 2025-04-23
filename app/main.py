"""
Main application module for the file upload and processing service.
"""
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import os
from typing import List
from dotenv import load_dotenv

from app.services.pdf_service import PDFService
from app.services.mcp_service import MCPService
from app.models.schemas import FileResponse

# Load environment variables
load_dotenv()

# Create upload directory if it doesn't exist
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

app = FastAPI(
    title="File Upload and LightRAG MCP Integration",
    description="API for uploading files and processing them through LightRAG MCP",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
pdf_service = PDFService()
mcp_service = MCPService()

@app.post("/upload", response_model=List[FileResponse])
async def upload_files(files: List[UploadFile] = File(...)):
    """
    Upload one or more files and process them through the LightRAG MCP server.

    Args:
        files (List[UploadFile]): List of files to upload

    Returns:
        List[FileResponse]: List of processed file responses
    """
    responses = []
    
    for file in files:
        try:
            # Save the file
            file_path = UPLOAD_DIR / file.filename
            with open(file_path, "wb") as buffer:
                content = await file.read()
                buffer.write(content)
            
            # Process PDF files
            if file.filename.lower().endswith('.pdf'):
                text = pdf_service.extract_text(file_path)
                # Send to MCP server
                mcp_response = mcp_service.process_text(text)
                responses.append(FileResponse(
                    filename=file.filename,
                    status="processed",
                    message="PDF processed successfully",
                    mcp_response=mcp_response
                ))
            else:
                responses.append(FileResponse(
                    filename=file.filename,
                    status="uploaded",
                    message="File uploaded successfully"
                ))
                
        except Exception as e:
            responses.append(FileResponse(
                filename=file.filename,
                status="error",
                message=str(e)
            ))
    
    return responses

@app.get("/health")
async def health_check():
    """
    Health check endpoint.
    """
    return {"status": "healthy"} 