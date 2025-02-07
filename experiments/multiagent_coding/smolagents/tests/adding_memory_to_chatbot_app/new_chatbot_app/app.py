
import streamlit as st
import os
from dotenv import load_dotenv
from backend.portkey_chat_client import PortkeyClient
from frontend.chat_interface import ChatInterface
from backend.chat_memory import ChatMemory
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Initialize the chat client
chat_client = PortkeyClient()

# Initialize chat memory in session state
if 'chat_memory' not in st.session_state:
    st.session_state.chat_memory = ChatMemory()
    logger.info("Initialized new chat memory in session state")
    
# Initialize conversation ID
if 'conversation_id' not in st.session_state:
    st.session_state.conversation_id = st.session_state.chat_memory.create_conversation()
    logger.info(f"Created new conversation: {st.session_state.conversation_id}")

def handle_message(prompt: str) -> str:
    try:
        # Add user message to memory
        message_id = st.session_state.chat_memory.add_message(
            st.session_state.conversation_id,
            "user",
            prompt
        )
        logger.info(f"Added user message {message_id}")
        
        # Get all messages for the current conversation
        messages = st.session_state.chat_memory.get_messages(st.session_state.conversation_id)
        
        # Get response from chat client
        response = chat_client.get_completion(messages)
        
        # Add assistant response to memory
        if response:
            response_id = st.session_state.chat_memory.add_message(
                st.session_state.conversation_id,
                "assistant",
                response
            )
            logger.info(f"Added assistant response {response_id}")
            return response
        else:
            error_msg = "Failed to get response from the assistant."
            logger.error(error_msg)
            return "I apologize, but I couldn't generate a response at this time."
            
    except ValueError as e:
        error_msg = f"Error processing message: {str(e)}"
        logger.error(error_msg)
        return "I encountered an error processing your message. Please try again."
    except Exception as e:
        error_msg = f"An unexpected error occurred: {str(e)}"
        logger.error(error_msg)
        return "I apologize, but something went wrong. Please try again later."

# Initialize and render the chat interface
chat_interface = ChatInterface(on_message=handle_message)

# Sidebar information and controls
st.sidebar.title("Chat Controls")

# Add a clear conversation button
if st.sidebar.button("Clear Conversation", key="clear_conv"):
    st.session_state.chat_memory.clear_conversation(st.session_state.conversation_id)
    st.session_state.messages = []
    logger.info("Cleared conversation")
    st.experimental_rerun()

# Display conversation statistics
stats = st.session_state.chat_memory.get_conversation_stats(st.session_state.conversation_id)
if stats:
    st.sidebar.subheader("Conversation Stats")
    st.sidebar.text(f"Messages: {stats['message_count']}")
    st.sidebar.text(f"Created: {stats['created_at'].strftime('%Y-%m-%d %H:%M')}")
    st.sidebar.text(f"Last activity: {stats['last_activity'].strftime('%Y-%m-%d %H:%M')}")

# Warning about memory limitations
st.sidebar.warning(
    "This is a simple in-memory chat. "
    "Messages will be lost when you close the browser. "
    f"Maximum {ChatMemory.MAX_MESSAGES_PER_CONVERSATION} messages per conversation."
)

chat_interface.render()
