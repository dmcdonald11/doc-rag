"""
Streamlit application for file upload and processing with LightRAG MCP integration.
"""
import streamlit as st
from pathlib import Path
import os
import asyncio
from typing import List, Optional
from dotenv import load_dotenv

from services.pdf_service import PDFService
from services.mcp_service import MCPService

# Load environment variables
load_dotenv()

# Create upload directory if it doesn't exist
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

# Initialize services
pdf_service = PDFService()
mcp_service = MCPService()

def process_pdf_file(file_path: Path) -> Optional[str]:
    """
    Process a PDF file and return the extracted text.

    Args:
        file_path (Path): Path to the PDF file

    Returns:
        Optional[str]: Extracted text if successful, None otherwise
    """
    try:
        return pdf_service.extract_text(file_path)
    except Exception as e:
        st.error(f"Error processing PDF: {str(e)}")
        return None

async def process_with_lightrag(text: str) -> Optional[dict]:
    """
    Process text with LightRAG MCP.

    Args:
        text (str): Text to process

    Returns:
        Optional[dict]: MCP response if successful, None otherwise
    """
    try:
        return await mcp_service.process_text(text)
    except Exception as e:
        st.error(f"Error processing with LightRAG: {str(e)}")
        return None

async def main():
    st.set_page_config(
        page_title="File Processing with LightRAG",
        page_icon="📄",
        layout="wide"
    )

    st.title("📄 File Processing with LightRAG")
    st.markdown("""
    Upload your files to process them with LightRAG MCP. PDF files will be automatically 
    converted to text and processed through the LightRAG system.
    """)

    # File uploader
    uploaded_files = st.file_uploader(
        "Choose files to upload",
        accept_multiple_files=True,
        type=['pdf', 'txt']
    )

    if uploaded_files:
        for file in uploaded_files:
            with st.expander(f"Processing {file.name}", expanded=True):
                # Save the file
                file_path = UPLOAD_DIR / file.name
                with open(file_path, "wb") as buffer:
                    buffer.write(file.getvalue())

                if file.name.lower().endswith('.pdf'):
                    # Process PDF
                    st.write(f"Processing PDF: {file.name}")
                    extracted_text = process_pdf_file(file_path)
                    
                    if extracted_text:
                        st.success("PDF processed successfully!")
                        st.subheader("Extracted Text")
                        st.text_area("Extracted Text Content", extracted_text, height=200, key=f"text_{file.name}")
                        
                        # Process with LightRAG
                        st.write("Processing with LightRAG...")
                        mcp_response = await process_with_lightrag(extracted_text)
                        
                        if mcp_response:
                            st.success("LightRAG processing complete!")
                            st.subheader("LightRAG Response")
                            st.json(mcp_response)
                else:
                    st.info(f"File {file.name} uploaded successfully")
                    st.write("Note: Only PDF files are processed with LightRAG")

if __name__ == "__main__":
    asyncio.run(main()) 