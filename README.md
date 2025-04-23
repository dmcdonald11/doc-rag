# File Upload and LightRAG MCP Integration

This application allows users to upload files (including PDFs) and processes them through a LightRAG MCP server for storage in Neo4j and PostgreSQL databases.

## Features

- Modern Streamlit frontend with drag & drop file upload
- PDF text extraction
- Integration with LightRAG MCP server
- Data storage in Neo4j and PostgreSQL
- Real-time upload progress and status updates

## Prerequisites

- Python 3.8+
- Docker (for running LightRAG MCP server)
- Neo4j database
- PostgreSQL database

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd doc-rag
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

## Project Structure

```
doc-rag/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI backend
│   ├── frontend.py      # Streamlit frontend
│   ├── models/
│   ├── services/
│   └── utils/
├── tests/
├── uploads/
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

## Running the Application

1. Start the LightRAG MCP server and databases:
```bash
docker-compose up -d
```

2. Start the FastAPI backend:
```bash
python -m app.main
```

3. Start the Streamlit frontend in a new terminal:
```bash
streamlit run app/frontend.py
```

4. Access the application:
- Frontend: `http://localhost:8501`
- Backend API: `http://localhost:8000`
- API Documentation: `http://localhost:8000/docs`

## Testing

Run the test suite:
```bash
pytest
```

## License

MIT License 