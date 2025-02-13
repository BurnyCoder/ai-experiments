import os
from typing import Dict, List, Optional, Any
from dotenv import load_dotenv
from zep_cloud import Message
from zep_cloud.client import Zep
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
            
        self.client = Zep(api_key=self.api_key)

    def add_memory(self, session_id: str, messages: List[Dict[str, str]]) -> None:
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
        
        self.client.memory.add(
            session_id=session_id,
            messages=zep_messages
        )

    def search_memory(self, session_id: str) -> List[Dict[str, Any]]:
        """Search session memory for relevant messages
        
        Args:
            session_id: ID of session to search
            
        Returns:
            List of relevant memory messages
        """
        memory = self.client.memory.get(session_id=session_id)
        return memory.context

    def add_session(self, user_id: str, session_id: str) -> None:
        """Create a new memory session for a user
        
        Args:
            user_id: ID of the user
            session_id: ID for the new session
        """
        self.client.memory.add_session(
            user_id=user_id,
            session_id=session_id
        )

    def add_user(self, user_id: str, email: str, first_name: str, last_name: str) -> None:
        """Add a new user
        
        Args:
            user_id: ID for the user
            email: User's email address
            first_name: User's first name
            last_name: User's last name
        """
        self.client.user.add(
            user_id=user_id,
            email=email,
            first_name=first_name,
            last_name=last_name
        )

    def get_facts(self, user_id: str) -> Dict[str, Any]:
        """Get facts about a user
        
        Args:
            user_id: ID of user to get facts for
            
        Returns:
            Dict containing user facts
        """
        return self.client.user.get_facts(user_id=user_id)

    def search_graph(self, user_id: str, query: str, limit: int = 4) -> Dict[str, Any]:
        """Search the knowledge graph
        
        Args:
            user_id: ID of user to search for
            query: Search query text
            limit: Max number of results
            
        Returns:
            Dict containing search results
        """
        return self.client.graph.search(
            user_id=user_id,
            query=query,
            limit=limit,
            scope="edges"
        )

    def create_sample_user_and_session(self) -> tuple[str, str]:
        """Create a sample user and session for testing
        
        Returns:
            Tuple containing user_id and session_id
        """
        
        self.add_user(
            user_id="1",
            email="1", 
            first_name="1",
            last_name="1"
        )
        
        # Create session
        self.add_session(
            user_id="1",
            session_id="1"
        )
        
        # # Add sample chat history
        # chat_history = [
        #     {
        #         "role": "assistant",
        #         "content": "How can I assist you today?"
        #     },
        #     {
        #         "role": "user",
        #         "content": "I dont need anything now."
        #     }
        # ]
        
        # self.add_memory(session_id=0, messages=chat_history)
        
        # Add sample data to graph
        # sample_data = {
        #     "account_status": {
        #         "status": "active",
        #         "subscription": "pro"
        #     }
        # }
        
        # self.client.graph.add(
        #     user_id="0",
        #     data=json.dumps(sample_data),
        #     type="json"
        # )
        

    def add_a_lot_of_memory(self):
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
            self.add_memory(
                session_id="0",
                messages=list(memory_pair)
            )

    def test(self):
        #self.add_a_lot_of_memory()
        # Test getting user facts
        #facts = self.get_facts("0")
        #print("User facts:", facts)
        #self.create_sample_user_and_session()
        memory = self.search_memory("1")
        print(memory)
        
def main():
    zep = ZepAPI()
    zep.test()
    
if __name__ == "__main__":
    main()