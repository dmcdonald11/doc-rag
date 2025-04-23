"""
Service for interacting with the LightRAG.
"""
import os
import asyncio
from typing import Dict, Any, Optional
from pydantic import BaseModel
from lightrag import LightRAG, QueryParam
from lightrag.llm.openai import gpt_4o_mini_complete, openai_embed
from lightrag.kg.shared_storage import initialize_pipeline_status
from lightrag.utils import EmbeddingFunc, setup_logger
from dotenv import load_dotenv

class LightRAGResponse(BaseModel):
    """
    Response model for LightRAG service.
    """
    status: str
    message: str
    data: Optional[Dict[str, Any]] = None

class LightRAGService:
    """
    Service for interacting with the LightRAG.
    """
    
    def __init__(self):
        """
        Initialize the LightRAG service with configuration from environment variables.
        """
        load_dotenv()
        self.working_dir = os.getenv("LIGHTRAG_WORKING_DIR", "./local_neo4jWorkDir")
        
            
        # Setup logger for LightRAG
        setup_logger("lightrag", level="INFO")
        
        # Initialize LightRAG instance
        self.rag = None
        
    async def initialize_rag(self):
        """
        Initialize the LightRAG instance with proper configuration.
        """
        if not os.path.exists(self.working_dir):
            os.makedirs(self.working_dir)
            
        self.rag = LightRAG(
            working_dir=self.working_dir,
            llm_model_func=gpt_4o_mini_complete,
            kv_storage="PGKVStorage",
            doc_status_storage="PGDocStatusStorage",
            vector_storage="PGVectorStorage",
            graph_storage="Neo4JStorage",
            auto_manage_storages_states=False,
            embedding_func=EmbeddingFunc(
                embedding_dim=1536,
                max_token_size=8192,
                func=openai_embed
            )
        )
        
        await self.rag.initialize_storages()
        await initialize_pipeline_status()
    
    async def process_text(self, text: str) -> LightRAGResponse:
        """
        Send text to the LightRAG server for processing.

        Args:
            text (str): Text to be processed

        Returns:
            LightRAGResponse: Response from the LightRAG server

        Raises:
            Exception: If LightRAG processing fails
        """
        try:
            # Initialize RAG if not already done
            if not self.rag:
                await self.initialize_rag()
            
            # Insert text into RAG
            await self.rag.ainsert(text)
            
            # Perform a hybrid search to get relevant context
            result = await self.rag.aquery(
                text,
                param=QueryParam(mode="hybrid")
            )
            
            return LightRAGResponse(
                status="success",
                message="Text processed successfully",
                data={"result": result}
            )
            
        except Exception as e:
            return LightRAGResponse(
                status="error",
                message=f"Failed to process text: {str(e)}"
            ) 