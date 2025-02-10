import streamlit as st
from datetime import datetime
from backend.memory import Memory

class ChatInterface:
    def __init__(self, on_message):
        self.on_message = on_message
        self.memory = Memory(max_messages=50)
        self._setup_page()

    def _setup_page(self):
        st.title("Chat Interface")
        
    def display_messages(self):
        """Display all messages in the chat history."""
        messages = self.memory.get_messages_with_timestamps()
        for message in messages:
            with st.chat_message(message["role"]):
                st.markdown(f"{message['content']} *(sent at {message['time']})*")

    def handle_input(self):
        """Handle user input and display responses."""
        if prompt := st.chat_input("What's on your mind?"):
            # Add and display user message
            user_message = self.memory.add_message("user", prompt)
            with st.chat_message("user"):
                st.markdown(f"{prompt} *(sent at {datetime.fromisoformat(user_message['timestamp']).strftime('%H:%M:%S')})*")

            # Get and display assistant response
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    if response := self.on_message(prompt):
                        assistant_message = self.memory.add_message("assistant", response)
                        st.markdown(f"{response} *(sent at {datetime.fromisoformat(assistant_message['timestamp']).strftime('%H:%M:%S')})*")
                    else:
                        st.error("Failed to get response from the assistant.")
                        
    def render(self):
        """Render the complete chat interface."""
        self.display_messages()
        self.handle_input()
