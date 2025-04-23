from dotenv import load_dotenv
#import streamlit as st
import asyncio
import os

# Import all the message part classes
from pydantic_ai.messages import (
    ModelMessage,
    ModelRequest,
    ModelResponse,
    SystemPromptPart,
    UserPromptPart,
    TextPart,
    ToolCallPart,
    ToolReturnPart,
    RetryPromptPart,
    ModelMessagesTypeAdapter
)

from lightrag import LightRAG, QueryParam
from lightrag.llm.openai import gpt_4o_mini_complete, openai_embed
from lightrag.kg.shared_storage import initialize_pipeline_status

#from agents.rag_agent import agent, RAGDeps

load_dotenv()

WORKING_DIR = "lightrag_working_dir"

async def initialize_rag():

    rag = LightRAG(
        working_dir=WORKING_DIR,
        llm_model_func=gpt_4o_mini_complete,
        kv_storage="PGKVStorage",
        doc_status_storage="PGDocStatusStorage",
        vector_storage="PGVectorStorage",
        graph_storage="Neo4JStorage",
        auto_manage_storages_states=False,
        embedding_func=openai_embed
    )

    await rag.initialize_storages()
    #await initialize_pipeline_status()

    return rag


async def main():
    # Initialize RAG instance
    rag = await initialize_rag()

    # Get user input for the question
    user_question = input("Please enter your question: ")
    
    results = await rag.aquery(
        user_question, 
        param=QueryParam(mode="mix")
    )
    print(results)
 
if __name__ == "__main__":
    asyncio.run(main())