import os
import pytest
from unittest.mock import patch, MagicMock
from app.services.lightrag_service import LightRAGService
from app.models.schemas import LightRAGResponse

def test_lightrag_service_initialization():
    """
    Test LightRAG service initialization with environment variables.
    """
    with patch.dict(os.environ, {
        "LIGHTRAG_WORKING_DIR": "./test_work_dir"
    }):
        service = LightRAGService()
        assert service.working_dir == "./test_work_dir"

def test_lightrag_service_initialization_missing_env():
    """
    Test LightRAG service initialization with missing environment variables.
    """
    with patch.dict(os.environ, {}, clear=True):
        service = LightRAGService()
        assert service.working_dir == "./local_neo4jWorkDir"  # Default value

@pytest.mark.asyncio
async def test_process_text_success():
    """
    Test successful text processing.
    """
    with patch.dict(os.environ, {
        "LIGHTRAG_WORKING_DIR": "./test_work_dir"
    }):
        service = LightRAGService()
        response = await service.process_text("Test text")
        assert isinstance(response, LightRAGResponse)
        assert response.status == "success"

@pytest.mark.asyncio
async def test_process_text_error():
    """
    Test text processing with error.
    """
    with patch.dict(os.environ, {
        "LIGHTRAG_WORKING_DIR": "./test_work_dir"
    }):
        service = LightRAGService()
        # Mock the RAG initialization to fail
        with patch.object(service, 'initialize_rag', side_effect=Exception("Test error")):
            response = await service.process_text("Test text")
            assert isinstance(response, LightRAGResponse)
            assert response.status == "error"
            assert "Test error" in response.message 