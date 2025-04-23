"""
Streamlit frontend for the file upload application.
"""
import streamlit as st
import requests
import os
from typing import List
import time
from pathlib import Path

# Constants
API_URL = os.getenv("API_URL", "http://localhost:8000")
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

def upload_files(files: List[bytes], filenames: List[str]) -> List[dict]:
    """
    Upload files to the FastAPI backend.

    Args:
        files (List[bytes]): List of file contents
        filenames (List[str]): List of file names

    Returns:
        List[dict]: List of responses from the API
    """
    responses = []
    for file_content, filename in zip(files, filenames):
        try:
            files = {"files": (filename, file_content)}
            response = requests.post(f"{API_URL}/upload", files=files)
            response.raise_for_status()
            responses.extend(response.json())
        except Exception as e:
            responses.append({
                "filename": filename,
                "status": "error",
                "message": str(e)
            })
    return responses

def main():
    """
    Main Streamlit application.
    """
    st.set_page_config(
        page_title="File Upload and Processing",
        page_icon="📄",
        layout="wide"
    )

    st.title("📄 File Upload and Processing")
    st.markdown("""
    Upload your files here. PDF files will be automatically processed and sent to the LightRAG MCP server.
    The extracted text will be stored in Neo4j and PostgreSQL databases.
    """)

    # File upload section
    uploaded_files = st.file_uploader(
        "Choose files to upload",
        accept_multiple_files=True,
        type=["pdf", "txt"]
    )

    if uploaded_files:
        # Display upload progress
        progress_bar = st.progress(0)
        status_text = st.empty()

        # Process files
        files_content = []
        filenames = []
        for i, uploaded_file in enumerate(uploaded_files):
            files_content.append(uploaded_file.getvalue())
            filenames.append(uploaded_file.name)
            progress_bar.progress((i + 1) / len(uploaded_files))
            status_text.text(f"Processing {uploaded_file.name}...")

        # Upload files
        responses = upload_files(files_content, filenames)

        # Display results
        st.subheader("Upload Results")
        for response in responses:
            if response["status"] == "processed":
                st.success(f"✅ {response['filename']}: {response['message']}")
                if response.get("mcp_response"):
                    with st.expander("View MCP Response"):
                        st.json(response["mcp_response"])
            elif response["status"] == "uploaded":
                st.info(f"📄 {response['filename']}: {response['message']}")
            else:
                st.error(f"❌ {response['filename']}: {response['message']}")

        # Reset progress
        progress_bar.empty()
        status_text.empty()

    # Display uploaded files section
    st.sidebar.title("Uploaded Files")
    uploaded_files_list = list(UPLOAD_DIR.glob("*"))
    if uploaded_files_list:
        for file_path in uploaded_files_list:
            st.sidebar.text(file_path.name)
    else:
        st.sidebar.info("No files uploaded yet")

if __name__ == "__main__":
    main() 