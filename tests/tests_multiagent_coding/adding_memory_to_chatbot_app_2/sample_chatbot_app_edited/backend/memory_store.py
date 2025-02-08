from typing import List, Dict, Optional, Union
import streamlit as st
from datetime import datetime
import logging
import uuid

logger = logging.getLogger(__name__)

class MemoryStore:
    """A robust memory store for chat messages with safety features and validation."""
    
    def __init__(self, max_messages: int = 1000, max_message_size: int = 4096):
        """Initialize the memory store with configurable limits.
        
        Args:
            max_messages: Maximum number of messages to store
            max_message_size: Maximum size of individual messages in characters
        """
        self.max_messages = max_messages
        self.max_message_size = max_message_size
        
        # Initialize session state if needed
        if "messages" not in st.session_state:
            st.session_state.messages = []
            logger.info("Initialized empty message history in session state")
            
        if "conversation_id" not in st.session_state:
            st.session_state.conversation_id = str(uuid.uuid4())
            logger.info("Generated new conversation ID")

    def _validate_message(self, role: str, content: str) -> None:
        """Validate message format and content.
        
        Args:
            role: Message role (user/assistant/system)
            content: Message content
            
        Raises:
            ValueError: If message format is invalid
        """
        if not isinstance(role, str) or not isinstance(content, str):
            raise ValueError("Role and content must be strings")
        
        valid_roles = {"user", "assistant", "system"}
        if role not in valid_roles:
            raise ValueError(f"Invalid role. Must be one of: {valid_roles}")
            
        if len(content) > self.max_message_size:
            raise ValueError(f"Message content exceeds maximum size of {self.max_message_size} characters")

    def add_message(self, role: str, content: str) -> bool:
        """Add a message to memory with validation and safety checks.
        
        Args:
            role: Message role
            content: Message content
            
        Returns:
            bool: True if message was added successfully
        """
        try:
            self._validate_message(role, content)
            
            message = {
                "role": role,
                "content": content,
                "timestamp": datetime.now().timestamp(),
                "id": len(st.session_state.messages)
            }
            
            if len(st.session_state.messages) >= self.max_messages:
                st.session_state.messages.pop(0)  # Remove oldest message
                logger.info("Removed oldest message due to size limit")
                
            st.session_state.messages.append(message)
            logger.info(f"Added new {role} message (id: {message['id']})")
            return True
            
        except Exception as e:
            logger.error(f"Failed to add message: {e}")
            return False

    def get_messages(self, limit: Optional[int] = None) -> List[Dict]:
        """Retrieve messages from memory with optional limit.
        
        Args:
            limit: Optional maximum number of messages to return
            
        Returns:
            List of message dictionaries
        """
        messages = st.session_state.messages
        if limit and limit > 0:
            return messages[-limit:]
        return messages.copy()  # Return copy to prevent direct modification

    def clear_memory(self) -> bool:
        """Clear all messages from memory.
        
        Returns:
            bool: True if operation was successful
        """
        try:
            st.session_state.messages = []
            st.session_state.conversation_id = str(uuid.uuid4())
            logger.info("Cleared message history and generated new conversation ID")
            return True
        except Exception as e:
            logger.error(f"Failed to clear memory: {e}")
            return False

    def get_message_count(self) -> int:
        """Get total number of messages in memory."""
        return len(st.session_state.messages)

    def search_messages(self, query: str) -> List[Dict]:
        """Search messages for specific content.
        
        Args:
            query: Search string
            
        Returns:
            List of matching message dictionaries
        """
        if not query:
            return []
            
        return [msg for msg in st.session_state.messages 
                if query.lower() in msg["content"].lower()]

    def get_conversation_id(self) -> str:
        """Get the current conversation ID."""
        return st.session_state.conversation_id
