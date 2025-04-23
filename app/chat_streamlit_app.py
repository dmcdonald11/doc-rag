"""
Streamlit application for chat interface with LightRAG integration.
"""
import streamlit as st
import asyncio
import os
from dotenv import load_dotenv
from contextlib import asynccontextmanager
import nest_asyncio

from lightrag import LightRAG, QueryParam
from lightrag.llm.openai import gpt_4o_mini_complete, openai_embed
from lightrag.kg.shared_storage import initialize_pipeline_status

# Load environment variables
load_dotenv()

# Apply nest_asyncio to allow nested event loops
nest_asyncio.apply()

WORKING_DIR = "lightrag_working_dir"

# Initialize a single event loop for the entire application
if "loop" not in st.session_state:
    st.session_state.loop = asyncio.new_event_loop()
    asyncio.set_event_loop(st.session_state.loop)

@asynccontextmanager
async def get_rag():
    """
    Context manager for LightRAG instance.
    """
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
    try:
        yield rag
    finally:
        # Cleanup if needed
        pass

async def process_query(rag: LightRAG, query: str) -> str:
    """
    Process a user query using LightRAG.
    
    Args:
        rag (LightRAG): Initialized LightRAG instance
        query (str): User's question
        
    Returns:
        str: Response from LightRAG
    """
    try:
        results = await rag.aquery(
            query,
            param=QueryParam(mode="mix")
        )
        return str(results)
    except Exception as e:
        return f"Error processing query: {str(e)}"

def main():
    st.set_page_config(
        page_title="Chat with LightRAG",
        page_icon="💬",
        layout="wide"
    )

    st.title("💬 Chat with LightRAG")
    st.markdown("""
    Ask questions and get answers using the LightRAG system. The system will search through
    the available knowledge base to provide relevant responses.
    """)

    # Initialize session state for chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("What would you like to know?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Get response from LightRAG
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    async def get_response():
                        async with get_rag() as rag:
                            return await process_query(rag, prompt)
                    
                    response = st.session_state.loop.run_until_complete(get_response())
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                except Exception as e:
                    error_msg = f"Error: {str(e)}"
                    st.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})

if __name__ == "__main__":
    main() 