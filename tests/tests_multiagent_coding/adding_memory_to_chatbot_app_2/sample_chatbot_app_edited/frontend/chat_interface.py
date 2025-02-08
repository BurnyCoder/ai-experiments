import streamlit as st
from typing import Callable, Optional
from backend.memory_store import MemoryStore
import uuid
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class ChatInterface:
    """A Streamlit-based chat interface with enhanced message display and controls."""

    def __init__(self, on_message: Callable[[str], Optional[str]]):
        """Initialize chat interface with message handler and memory store.
        
        Args:
            on_message: Callback function for handling new messages
        """
        self.on_message = on_message
        self.memory = MemoryStore(max_messages=1000)
        self._initialize_session_state()
        self._setup_page()

    def _initialize_session_state(self) -> None:
        """Initialize or validate session state variables."""
        if "conversation_id" not in st.session_state:
            st.session_state.conversation_id = str(uuid.uuid4())
        if "error" not in st.session_state:
            st.session_state.error = None
        if "search_query" not in st.session_state:
            st.session_state.search_query = ""
        if "show_timestamps" not in st.session_state:
            st.session_state.show_timestamps = True

    def _setup_page(self) -> None:
        """Configure the Streamlit page layout and sidebar."""
        st.title("Chat Interface")
        
        with st.sidebar:
            st.title("Chat Controls")
            
            # Display Options
            st.subheader("Display Options")
            st.session_state.show_timestamps = st.checkbox(
                "Show timestamps", 
                value=st.session_state.show_timestamps
            )
            
            # Search functionality
            st.subheader("Search Messages")
            search_query = st.text_input("🔍 Search", key="search_input")
            if search_query:
                search_results = self.memory.search_messages(search_query)
                if search_results:
                    st.subheader("Search Results")
                    for msg in search_results:
                        with st.expander(f"💬 {self._format_timestamp(msg['timestamp'])}"):
                            st.markdown(f"**{msg['role'].title()}**: {msg['content'][:100]}...")
                            st.caption(f"Message ID: {msg['id']}")
                else:
                    st.info("No matching messages found")
            
            # New conversation button
            if st.button("📝 New Conversation", type="primary"):
                self.memory.clear_memory()
                st.rerun()
            
            # Display message count and conversation ID
            st.divider()
            msg_count = self.memory.get_message_count()
            st.caption(f"Messages in conversation: {msg_count}")
            st.caption(f"Conversation ID: {self.memory.get_conversation_id()[:8]}...")
            
            # Export option
            if msg_count > 0 and st.button("📥 Export Chat"):
                self._export_chat()
            
            # Settings and controls
            with st.expander("⚙️ Settings"):
                if st.button("Clear Chat History"):
                    if self.memory.clear_memory():
                        st.success("Chat history cleared successfully")
                        st.rerun()
                    else:
                        st.error("Failed to clear chat history")

    def _format_timestamp(self, timestamp: float) -> str:
        """Format timestamp for display.
        
        Args:
            timestamp: Unix timestamp
            
        Returns:
            Formatted datetime string
        """
        dt = datetime.fromtimestamp(timestamp)
        return dt.strftime("%I:%M %p")  # Format: HH:MM AM/PM

    def _export_chat(self) -> None:
        """Export chat history as formatted text."""
        try:
            messages = self.memory.get_messages()
            if not messages:
                return
                
            export_text = "Chat History Export\n"
            export_text += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            
            for msg in messages:
                timestamp = datetime.fromtimestamp(msg['timestamp'])
                export_text += f"[{timestamp.strftime('%Y-%m-%d %H:%M:%S')}] "
                export_text += f"{msg['role'].upper()}: {msg['content']}\n"
            
            st.download_button(
                label="Download Chat History",
                data=export_text,
                file_name=f"chat_history_{st.session_state.conversation_id[:8]}.txt",
                mime="text/plain"
            )
            
        except Exception as e:
            logger.error(f"Failed to export chat: {e}")
            st.error("Failed to export chat history")

    def display_messages(self) -> None:
        """Display all messages in the chat interface."""
        messages = self.memory.get_messages()
        
        for msg in messages:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])
                if st.session_state.show_timestamps:
                    st.caption(f"Sent at {self._format_timestamp(msg['timestamp'])}")

    def handle_input(self) -> None:
        """Handle user input and generate responses."""
        if prompt := st.chat_input("Type your message..."):
            # Add user message
            if not self.memory.add_message("user", prompt):
                st.error("Failed to send message")
                return
            
            # Get bot response
            with st.spinner("Thinking..."):
                if response := self.on_message(prompt):
                    if not self.memory.add_message("assistant", response):
                        st.error("Failed to save assistant response")
                else:
                    st.error("Failed to get response")
                    
            st.rerun()

    def render(self) -> None:
        """Render the complete chat interface."""
        self.display_messages()
        self.handle_input()
