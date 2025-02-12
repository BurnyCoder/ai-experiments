import os
import logging
from datetime import datetime
from typing import Dict, Any, List, Optional
from zep_python import ZepClient, Message, Memory, Session

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ZepAPI:
    """Client for interacting with the Zep Memory Store"""
    
    def __init__(self):
        """Initialize Zep client with API key from environment"""
        self.api_key = os.getenv("ZEP_API_KEY")
        if not self.api_key:
            raise ValueError("ZEP_API_KEY environment variable not set")
            
        self.client = ZepClient(api_key=self.api_key)
        
    def create_session(self, session_id: str) -> Session:
        """Create a new memory session
        
        Args:
            session_id: Unique identifier for the session
            
        Returns:
            Session object
        """
        try:
            return self.client.memory.create_session(session_id)
        except Exception as e:
            logger.error(f"Error creating session: {str(e)}")
            raise
            
    def add_memory(self, session_id: str, messages: List[Dict[str, Any]]) -> None:
        """Add messages to a memory session
        
        Args:
            session_id: Session identifier
            messages: List of message dictionaries with role and content
        """
        try:
            zep_messages = [
                Message(
                    role=msg["role"],
                    content=msg["content"]
                ) for msg in messages
            ]
            self.client.memory.add_memory(session_id, zep_messages)
        except Exception as e:
            logger.error(f"Error adding memory: {str(e)}")
            raise
            
    def get_memory(self, session_id: str, last_n: Optional[int] = None) -> Memory:
        """Retrieve memory for a session
        
        Args:
            session_id: Session identifier
            last_n: Optional number of most recent memories to retrieve
            
        Returns:
            Memory object containing session history
        """
        try:
            return self.client.memory.get_memory(session_id, last_n=last_n)
        except Exception as e:
            logger.error(f"Error getting memory: {str(e)}")
            raise
            
    def search_memory(self, session_id: str, query: str, limit: int = 5) -> List[Memory]:
        """Search memories semantically
        
        Args:
            session_id: Session identifier
            query: Search query
            limit: Maximum number of results
            
        Returns:
            List of matching Memory objects
        """
        try:
            return self.client.memory.search_memory(session_id, query, limit=limit)
        except Exception as e:
            logger.error(f"Error searching memory: {str(e)}")
            raise
            
    def delete_session(self, session_id: str) -> None:
        """Delete a memory session
        
        Args:
            session_id: Session identifier to delete
        """
        try:
            self.client.memory.delete_session(session_id)
        except Exception as e:
            logger.error(f"Error deleting session: {str(e)}")
            raise 