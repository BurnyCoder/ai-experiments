import os
from typing import Dict, List, Optional, Any
from dotenv import load_dotenv
from zep_cloud import Message
from zep_cloud.client import AsyncZep

# Load environment variables
load_dotenv()

class ZepAPI:
    """Client for interacting with the Zep memory API"""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the Zep API client
        
        Args:
            api_key: Optional API key. If not provided, will look for ZEP_API_KEY env var
        """
        self.api_key = api_key or os.getenv('ZEP_API_KEY')
        if not self.api_key:
            raise ValueError("API key must be provided or set as ZEP_API_KEY environment variable")
            
        self.client = AsyncZep(api_key=self.api_key)

    async def add_memory(self, session_id: str, messages: List[Dict[str, str]]) -> None:
        """Add messages to a session's memory
        
        Args:
            session_id: ID of the session to add memory to
            messages: List of message dicts with role and content
        """
        zep_messages = [
            Message(
                role_type=msg["role"],
                role=msg.get("name", None),
                content=msg["content"]
            )
            for msg in messages
        ]
        
        await self.client.memory.add(
            session_id=session_id,
            messages=zep_messages
        )

    async def search_memory(self, session_id: str, query: str) -> List[Dict[str, Any]]:
        """Search session memory for relevant messages
        
        Args:
            session_id: ID of session to search
            query: Search query text
            
        Returns:
            List of relevant memory messages
        """
        memory = await self.client.memory.get(session_id=session_id)
        return memory.messages

    async def add_session(self, user_id: str, session_id: str) -> None:
        """Create a new memory session for a user
        
        Args:
            user_id: ID of the user
            session_id: ID for the new session
        """
        await self.client.memory.add_session(
            user_id=user_id,
            session_id=session_id
        )

    async def add_user(self, user_id: str, email: str, first_name: str, last_name: str) -> None:
        """Add a new user
        
        Args:
            user_id: ID for the user
            email: User's email address
            first_name: User's first name
            last_name: User's last name
        """
        await self.client.user.add(
            user_id=user_id,
            email=email,
            first_name=first_name,
            last_name=last_name
        )

    async def get_facts(self, user_id: str) -> Dict[str, Any]:
        """Get facts about a user
        
        Args:
            user_id: ID of user to get facts for
            
        Returns:
            Dict containing user facts
        """
        return await self.client.user.get_facts(user_id=user_id)

    async def search_graph(self, user_id: str, query: str, limit: int = 4) -> Dict[str, Any]:
        """Search the knowledge graph
        
        Args:
            user_id: ID of user to search for
            query: Search query text
            limit: Max number of results
            
        Returns:
            Dict containing search results
        """
        return await self.client.graph.search(
            user_id=user_id,
            query=query,
            limit=limit,
            scope="edges"
        )
