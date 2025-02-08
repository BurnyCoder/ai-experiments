
from typing import List, Dict, Optional
import json
import os
from datetime import datetime
import logging
from pathlib import Path
from functools import lru_cache

class ConversationMemory:
    """Simple memory mechanism to store and retrieve conversation history with caching."""
    
    def __init__(self, storage_dir: str = "conversation_history", max_conversations: int = 100):
        self.storage_dir = Path(storage_dir)
        self.max_conversations = max_conversations
        self._ensure_storage_dir()
        
    def _ensure_storage_dir(self):
        """Create storage directory if it doesn't exist."""
        try:
            self.storage_dir.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            logging.error(f"Failed to create storage directory: {e}")
            raise RuntimeError(f"Could not initialize storage: {e}")
    
    @lru_cache(maxsize=100)
    def load_conversation(self, conversation_id: str) -> Optional[List[Dict[str, str]]]:
        """Load a conversation from disk with caching."""
        if not self._validate_conversation_id(conversation_id):
            return None
            
        try:
            filepath = self.storage_dir / f"{conversation_id}.json"
            if filepath.exists():
                with open(filepath, 'r') as f:
                    data = json.load(f)
                    return data['messages']
        except Exception as e:
            logging.error(f"Failed to load conversation {conversation_id}: {e}")
        return None
    
    def search_conversations(self, query: str) -> List[Dict[str, str]]:
        """Search conversations for specific text."""
        results = []
        try:
            conversations = self.list_conversations()
            for conv in conversations:
                messages = self.load_conversation(conv['conversation_id'])
                if messages:
                    # Search in message content
                    for msg in messages:
                        if query.lower() in msg['content'].lower():
                            results.append({
                                **conv,
                                'matching_message': msg['content'][:100] + '...'  # Preview
                            })
                            break
            return results
        except Exception as e:
            logging.error(f"Failed to search conversations: {e}")
            return []
    
    def invalidate_cache(self, conversation_id: str = None):
        """Invalidate the cache for a specific conversation or all conversations."""
        if conversation_id:
            self.load_conversation.cache_clear()
        else:
            # Clear the entire cache
            self.load_conversation.cache_clear()
