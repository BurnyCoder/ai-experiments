import streamlit as st
import logging
from typing import Optional
from backend.memory_store import MemoryStore
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Must be the first Streamlit command
st.set_page_config(
    page_title="Chat Interface",
    page_icon="💬",
    layout="wide"
)

import os
from dotenv import load_dotenv
from backend.portkey_chat_client import PortkeyClient
from frontend.chat_interface import ChatInterface

# Load environment variables
load_dotenv()

# Initialize the chat client
def init_chat_client() -> Optional[PortkeyClient]:
    """Initialize and test the chat client connection."""
    try:
        client = PortkeyClient()
        if not client.test_connection():
            st.error("Failed to connect to chat service. Please check your API keys.")
            return None
        return client
    except ValueError as e:
        st.error(f"Configuration error: {e}")
        return None
    except Exception as e:
        logger.error(f"Failed to initialize chat client: {e}")
        st.error("Failed to initialize chat service. Please try again later.")
        return None

chat_client = init_chat_client()
if not chat_client:
    st.stop()

# Initialize memory store with configuration
MEMORY_CONFIG = {
    "max_messages": 1000,
    "max_message_size": 4096
}

if "memory_store" not in st.session_state:
    st.session_state.memory_store = MemoryStore(**MEMORY_CONFIG)
memory_store = st.session_state.memory_store

def handle_message(prompt: str) -> Optional[str]:
    """Handle new messages by getting completions from the chat client."""
    if not prompt or not prompt.strip():
        return None
        
    try:
        # Get messages from memory store
        stored_messages = memory_store.get_messages()
        
        # Format messages for the chat client
        messages = [{"role": "system", "content": "You are a helpful assistant."}]
        messages.extend([
            {"role": m["role"], "content": m["content"]}
            for m in stored_messages
        ])
        messages.append({"role": "user", "content": prompt})
        
        # Get completion from chat client
        response = chat_client.get_completion(messages)
        
        if response:
            return response
        else:
            logger.error("Received empty response from chat client")
            st.error("Failed to get response. Please try again.")
            
    except Exception as e:
        logger.error(f"Error in message handling: {e}")
        st.error("An error occurred while processing your message.")
        
    return None

# Initialize and render the chat interface
try:
    chat_interface = ChatInterface(on_message=handle_message)
    chat_interface.render()
except Exception as e:
    logger.error(f"Failed to render chat interface: {e}")
    st.error("Failed to load chat interface. Please refresh the page.")
