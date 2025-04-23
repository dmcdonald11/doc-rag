"""
Tests for the MCP service.
"""
import pytest
import os
from unittest.mock import patch, MagicMock
from app.services.mcp_service import MCPService
from app.models.schemas import MCPResponse

def test_mcp_service_initialization():
    """
    Test MCP service initialization with environment variables.
    """
    with patch.dict(os.environ, {
        "MCP_SERVER_URL": "http://test-server",
        "MCP_API_KEY": "test-key"
    }):
        service = MCPService()
        assert service.mcp_url == "http://test-server"
        assert service.api_key == "test-key"

def test_mcp_service_initialization_missing_env():
    """
    Test MCP service initialization with missing environment variables.
    """
    with patch.dict(os.environ, {}, clear=True):
        with pytest.raises(ValueError) as exc_info:
            MCPService()
        assert "environment variable is not set" in str(exc_info.value)

@patch('requests.post')
def test_process_text_success(mock_post):
    """
    Test successful text processing through MCP service.
    """
    # Mock the response
    mock_response = MagicMock()
    mock_response.json.return_value = {"result": "success"}
    mock_response.raise_for_status.return_value = None
    mock_post.return_value = mock_response
    
    with patch.dict(os.environ, {
        "MCP_SERVER_URL": "http://test-server",
        "MCP_API_KEY": "test-key"
    }):
        service = MCPService()
        response = service.process_text("Test text")
        
        assert isinstance(response, MCPResponse)
        assert response.status == "success"
        assert response.message == "Text processed successfully"
        assert response.data == {"result": "success"}
        
        # Verify the request was made correctly
        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args
        assert args[0] == "http://test-server/process"
        assert kwargs["headers"]["Authorization"] == "Bearer test-key"
        assert kwargs["json"]["text"] == "Test text"

@patch('requests.post')
def test_process_text_failure(mock_post):
    """
    Test failed text processing through MCP service.
    """
    # Mock the exception
    mock_post.side_effect = Exception("Connection error")
    
    with patch.dict(os.environ, {
        "MCP_SERVER_URL": "http://test-server",
        "MCP_API_KEY": "test-key"
    }):
        service = MCPService()
        response = service.process_text("Test text")
        
        assert isinstance(response, MCPResponse)
        assert response.status == "error"
        assert "Connection error" in response.message
        assert response.data is None 