
# 📄 Project Planning Document: File Upload and LightRAG MCP Integration

## Objective
Build an application that allows users to upload one or more files. If a file is a PDF, it should be converted into text. The extracted text should then be sent to a LightRAG MCP server, which processes and stores it into Neo4j and PostgreSQL databases.

## 📁 High-Level Architecture
1. **Frontend**
   - UI for file upload (drag & drop, browse)
   - Progress indicators and status messages

2. **Backend**
   - File handling and storage in a designated `upload/` directory
   - PDF text extraction logic
   - Client integration with LightRAG MCP server
   - Error handling and logging

3. **LightRAG MCP Server**
   - Accepts text input from backend
   - Parses and stores data into:
     - Neo4j (for graph-based storage)
     - PostgreSQL (for structured storage)

## 🛠️ Tech Stack
- **Frontend**: Gradio with a menu bar for seperate pages for each operation
- **Backend**: Python (Flask/FastAPI).
- **PDF Parsing**: Use the best available pdf parser (consult context7)
- **Storage**: File system (`/upload`)
- **Databases**: Neo4j, PostgreSQL
- **MCP Server**: LightRAG MCP API
- **Containerization** Docker container for the MCP server seperate from the application
