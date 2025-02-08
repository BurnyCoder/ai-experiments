from typing import Any
from typing import List, Dict, Optional
import uuid
from dataclasses import dataclass
from datetime import datetime, timedelta
import html
import logging
from functools import lru_cache

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class Message:
    """
    Represents a single message in a conversation.
    
    Attributes:
        role (str): The role of the message sender ('user' or 'assistant')
        content (str): The content of the message
        timestamp (datetime): When the message was created
        message_id (str): Unique identifier for the message
    """
    role: str
    content: str
    timestamp: datetime = datetime.now()
    message_id: str = uuid.uuid4()

    def __post_init__(self):
        """Validates message attributes after initialization."""
        if not isinstance(self.role, str):
            raise ValueError("Role must be a string")
        
        if self.role not in ['user', 'assistant']:
            raise ValueError("Role must be either 'user' or 'assistant'")
            
        if not isinstance(self.content, str):
            raise ValueError("Content must be a string")
            
        if not self.content.strip():
            raise ValueError("Content cannot be empty")
            
        if len(self.content) > 4096:
            raise ValueError("Content exceeds maximum length of 4096 characters")
            
        self.content = html.escape(self.content.strip())

    def to_dict(self) -> Dict[str, str]:
        """Converts the message to a dictionary representation."""
        return {
            "role": self.role,
            "content": self.content,
            "message_id": str(self.message_id),
            "timestamp": self.timestamp.isoformat()
        }

class ChatMemory:
    """
    Manages chat conversations with automatic cleanup and message limiting.
    
    This class handles the storage, retrieval, and cleanup of chat conversations.
    It automatically manages conversation lifecycles and implements limits to
    prevent memory overflow.

    Attributes:
        MAX_MESSAGES_PER_CONVERSATION (int): Maximum messages allowed per conversation
        MAX_CONVERSATIONS (int): Maximum number of active conversations allowed
        CONVERSATION_TIMEOUT (timedelta): Time after which inactive conversations are cleaned up
        CLEANUP_INTERVAL (timedelta): Minimum time between cleanup operations
    """
    
    MAX_MESSAGES_PER_CONVERSATION = 100
    MAX_CONVERSATIONS = 1000
    CONVERSATION_TIMEOUT = timedelta(hours=24)
    CLEANUP_INTERVAL = timedelta(minutes=5)
    
    def __init__(self):
        """Initialize a new ChatMemory instance."""
        self._conversations: Dict[str, List[Message]] = {}
        self._metadata: Dict[str, Dict] = {}
        self._last_cleanup: datetime = datetime.now()
        logger.info("Initialized new ChatMemory instance")
    
    @property

    def active_conversations(self) -> int:
        """Returns the number of active conversations."""
        return len(self._conversations)
    

    def _validate_conversation_id(self, conversation_id: str) -> None:
        """
        Validates a conversation ID.
        
        Args:
            conversation_id: The ID to validate
            
        Raises:
            ValueError: If the conversation ID is invalid
        """
        if not isinstance(conversation_id, str):
            raise ValueError("Conversation ID must be a string")
        if not conversation_id:
            raise ValueError("Conversation ID cannot be empty")
    

    def _should_cleanup(self) -> bool:
        """Determines if cleanup should be performed based on the cleanup interval."""
        return datetime.now() - self._last_cleanup > self.CLEANUP_INTERVAL
    

    def _cleanup_old_conversations(self) -> None:
        """
        Clean up old conversations based on timeout and maximum limits.
        
        This method removes conversations that have been inactive for longer than
        CONVERSATION_TIMEOUT and ensures the total number of conversations doesn't
        exceed MAX_CONVERSATIONS.
        """
        try:
            if not self._should_cleanup():
                return
                
            current_time = datetime.now()
            self._last_cleanup = current_time
            
            # Remove conversations older than timeout
            expired_conversations = [
                conv_id for conv_id, metadata in self._metadata.items()
                if current_time - metadata['last_activity'] > self.CONVERSATION_TIMEOUT
            ]
            
            for conv_id in expired_conversations:
                del self._conversations[conv_id]
                del self._metadata[conv_id]
                logger.info(f"Removed expired conversation: {conv_id}")
                
            # If still over limit, remove oldest conversations
            if len(self._conversations) > self.MAX_CONVERSATIONS:
                conversations_by_activity = sorted(
                    self._metadata.items(),
                    key=lambda x: x[1]['last_activity']
                )
                
                excess_count = len(self._conversations) - self.MAX_CONVERSATIONS
                for conv_id, _ in conversations_by_activity[:excess_count]:
                    del self._conversations[conv_id]
                    del self._metadata[conv_id]
                    logger.info(f"Removed old conversation: {conv_id}")
                    
        except Exception as e:
            logger.error(f"Error during conversation cleanup: {str(e)}")
            raise
        

    def create_conversation(self) -> str:
        """
        Creates a new conversation and returns its ID.
        
        Returns:
            str: The ID of the newly created conversation
            
        Raises:
            RuntimeError: If maximum number of conversations is reached
        """
        try:
            self._cleanup_old_conversations()
            
            if len(self._conversations) >= self.MAX_CONVERSATIONS:
                raise RuntimeError("Maximum number of conversations reached")
                
            conversation_id = str(uuid.uuid4())
            self._conversations[conversation_id] = []
            self._metadata[conversation_id] = {
                'created_at': datetime.now(),
                'last_activity': datetime.now(),
                'message_count': 0
            }
            return conversation_id
            
        except Exception as e:
            logger.error(f"Error creating conversation: {str(e)}")
            raise


    def add_message(self, conversation_id: str, role: str, content: str) -> str:
        """
        Adds a message to a conversation.
        
        Args:
            conversation_id: ID of the conversation
            role: Role of the message sender
            content: Content of the message
            
        Returns:
            str: ID of the created message
            
        Raises:
            ValueError: If input parameters are invalid
        """
        try:
            self._validate_conversation_id(conversation_id)
            
            if conversation_id not in self._conversations:
                conversation_id = self.create_conversation()
                
            self._metadata[conversation_id]['last_activity'] = datetime.now()
            self._metadata[conversation_id]['message_count'] += 1
                
            message = Message(role=role, content=content)
            
            if len(self._conversations[conversation_id]) >= self.MAX_MESSAGES_PER_CONVERSATION:
                self._conversations[conversation_id].pop(0)
                
            self._conversations[conversation_id].append(message)
            return str(message.message_id)
            
        except Exception as e:
            logger.error(f"Error adding message: {str(e)}")
            raise
        

    def get_messages(self, conversation_id: str) -> List[Dict[str, str]]:
        """
        Retrieves all messages from a conversation.
        
        Args:
            conversation_id: ID of the conversation
            
        Returns:
            List[Dict[str, str]]: List of messages in dictionary format
        """
        try:
            self._validate_conversation_id(conversation_id)
            if conversation_id not in self._conversations:
                return []
            return [msg.to_dict() for msg in self._conversations[conversation_id]]
        except Exception as e:
            logger.error(f"Error retrieving messages: {str(e)}")
            raise
        

    def clear_conversation(self, conversation_id: str) -> None:
        """
        Clears all messages from a conversation.
        
        Args:
            conversation_id: ID of the conversation to clear
            
        Raises:
            ValueError: If conversation ID is invalid
        """
        try:
            self._validate_conversation_id(conversation_id)
            if conversation_id in self._conversations:
                self._conversations[conversation_id] = []
                self._metadata[conversation_id]['message_count'] = 0
                self._metadata[conversation_id]['last_activity'] = datetime.now()
        except Exception as e:
            logger.error(f"Error clearing conversation: {str(e)}")
            raise


    def get_conversation_stats(self, conversation_id: str) -> Dict[str, Any]:
        """
        Get statistics for a specific conversation.
        
        Args:
            conversation_id (str): ID of the conversation to retrieve statistics for
            
        Returns:
            Dict[str, Any]: Dictionary containing conversation statistics with fields:
                - message_count (int): Number of messages in the conversation
                - created_at (datetime): When the conversation was created
                - last_activity (datetime): Time of the last message
                - duration (timedelta): Time elapsed since conversation creation
                
        Raises:
            ValueError: If conversation_id is invalid (empty or wrong type)
            KeyError: If conversation_id doesn't exist
        """
        try:
            self._validate_conversation_id(conversation_id)
            
            if not conversation_id.strip():
                raise ValueError("Conversation ID cannot be empty")
                
            if conversation_id not in self._metadata:
                raise KeyError(f"Conversation with ID {conversation_id} not found")
                
            metadata = self._metadata[conversation_id]
            created_at = metadata.get('created_at')
            last_activity = metadata.get('last_activity')
            
            if not created_at or not last_activity:
                logger.error(f"Invalid metadata for conversation {conversation_id}")
                raise ValueError("Invalid conversation metadata")
                
            return {
                'message_count': int(metadata.get('message_count', 0)),
                'created_at': created_at,
                'last_activity': last_activity,
                'duration': last_activity - created_at
            }
            
        except (ValueError, KeyError) as e:
            logger.error(f"Error getting conversation stats for {conversation_id}: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error in get_conversation_stats: {str(e)}")
            raise
