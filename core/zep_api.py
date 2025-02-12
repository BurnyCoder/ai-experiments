import os
from typing import Dict, List, Optional, Any
from dotenv import load_dotenv
from zep_cloud import Message
from zep_cloud.client import AsyncZep
import uuid
import json

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

    async def create_sample_user_and_session(self) -> tuple[str, str]:
        """Create a sample user and session for testing
        
        Returns:
            Tuple containing user_id and session_id
        """
        
        await self.add_user(
            user_id="0",
            email="0", 
            first_name="0",
            last_name="0"
        )
        
        # Create session
        await self.add_session(
            user_id="0",
            session_id="0"
        )
        
        # Add sample chat history
        chat_history = [
            {
                "role": "assistant",
                "content": "How can I assist you today?"
            },
            {
                "role": "user",
                "content": "I dont need anything now."
            }
        ]
        
        await self.add_memory(session_id=0, messages=chat_history)
        
        # Add sample data to graph
        # sample_data = {
        #     "account_status": {
        #         "status": "active",
        #         "subscription": "pro"
        #     }
        # }
        
        # await self.client.graph.add(
        #     user_id="0",
        #     data=json.dumps(sample_data),
        #     type="json"
        # )
        

    async def add_a_lot_of_memory(self):
        """Add multiple sample memories about random topics"""
        memories = [
            {
                "role": "user",
                "content": "Tell me about black holes."
            },
            {
                "role": "assistant", 
                "content": "Black holes are regions of spacetime where gravity is so strong that nothing, not even light, can escape from them. They are formed when massive stars collapse at the end of their life cycle."
            },
            {
                "role": "user",
                "content": "What's the deepest part of the ocean?"
            },
            {
                "role": "assistant",
                "content": "The Mariana Trench is the deepest known part of the ocean, reaching a depth of approximately 36,000 feet (11,000 meters) below sea level."
            },
            {
                "role": "user",
                "content": "How do bees make honey?"
            },
            {
                "role": "assistant",
                "content": "Bees make honey by collecting nectar from flowers, which they store in their honey stomach. The nectar mixes with enzymes and is then regurgitated into honeycomb cells where it's fanned by bee wings until it thickens into honey."
            },
            {
                "role": "user",
                "content": "What causes the Northern Lights?"
            },
            {
                "role": "assistant",
                "content": "The Northern Lights (Aurora Borealis) are caused by charged particles from the sun colliding with atoms in Earth's atmosphere, creating colorful displays of light in the sky."
            },
            {
                "role": "user",
                "content": "Tell me about the Great Wall of China."
            },
            {
                "role": "assistant",
                "content": "The Great Wall of China is over 13,000 miles long and was built over many centuries by different dynasties. Construction began over 2,000 years ago as a series of walls to protect Chinese territories."
            }
        ]

        for memory_pair in zip(memories[::2], memories[1::2]):
            await self.add_memory(
                session_id="0",
                messages=list(memory_pair)
            )

    async def test(self):
        await self.add_a_lot_of_memory()
        
        # Search memory
        results = await ZepAPI().search_memory(
            session_id="0",
            query="Facts about physics"
        )
            
        print("Search results:", results)

if __name__ == "__main__":
    zep = ZepAPI()
    import asyncio
    asyncio.run(zep.test())