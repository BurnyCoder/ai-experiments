import streamlit as st

# Must be the first Streamlit command
st.set_page_config(page_title="GPT-4 Chat", page_icon="💬")

import os
from dotenv import load_dotenv
from backend.chat_client import ChatClient
from frontend.chat_interface import ChatInterface

# Load environment variables
load_dotenv()

# Initialize the chat client
chat_client = ChatClient(api_key=os.getenv("OPENAI_API_KEY"))

def handle_message(prompt: str) -> str:
    """Handle new messages by getting completions from the chat client."""
    messages = [
        {"role": m["role"], "content": m["content"]}
        for m in st.session_state.messages
    ]
    return chat_client.get_completion(messages)

# Initialize and render the chat interface
chat_interface = ChatInterface(on_message=handle_message)
chat_interface.render() 