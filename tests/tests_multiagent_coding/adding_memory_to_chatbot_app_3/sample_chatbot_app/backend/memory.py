from collections import deque
from datetime import datetime
import streamlit as st

class Memory:
    def __init__(self, max_messages=50):
        """Initialize the memory with a maximum message limit."""
        if 'chat_memory' not in st.session_state:
            st.session_state.chat_memory = deque(maxlen=max_messages)
        self.messages = st.session_state.chat_memory
        
    def add_message(self, role, content):
        """Add a message to memory with timestamp."""
        message = {
            'role': role,
            'content': content,
            'timestamp': datetime.now().isoformat(),
            'message_id': len(self.messages)
        }
        self.messages.append(message)
        return message
    
    def get_recent_messages(self, n=None):
        """Get the n most recent messages. If n is None, return all messages."""
        messages = list(self.messages)
        if n is None:
            return messages
        return messages[-n:]
    
    def get_messages_for_context(self, max_messages=10):
        """Get messages formatted for API context."""
        recent = self.get_recent_messages(max_messages)
        return [{'role': m['role'], 'content': m['content']} for m in recent]
    
    def clear(self):
        """Clear all messages from memory."""
        self.messages.clear()
        
    def get_messages_with_timestamps(self):
        """Get all messages with their timestamps for display."""
        return [
            {**msg, 'time': datetime.fromisoformat(msg['timestamp']).strftime('%H:%M:%S')}
            for msg in self.messages
        ]
        
    def prune_old_messages(self, keep_last=50):
        """Keep only the last n messages."""
        if len(self.messages) > keep_last:
            self.messages = deque(list(self.messages)[-keep_last:], maxlen=self.messages.maxlen)
            
    def search_messages(self, query):
        """Search messages containing the query string."""
        query = query.lower()
        return [
            msg for msg in self.messages 
            if query in msg['content'].lower()
        ]
