import streamlit as st
from typing import Callable, Optional


class ChatInterface:
    """A Streamlit-based chat interface."""

    def __init__(self, on_message: Callable[[str], Optional[str]]):
        """
        Initialize the chat interface.

        Args:
            on_message: Callback function that handles new messages
        """
        self.on_message = on_message
        self._initialize_session_state()
        self._setup_page()

    def _initialize_session_state(self):
        """Initialize the session state for storing messages."""
        if "messages" not in st.session_state:
            st.session_state.messages = []

    def _setup_page(self):
        """Configure the page settings and title."""
        st.title("Chat Interface")

    def display_messages(self):
        """Display all messages in the chat history."""
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    def handle_input(self):
        """Handle user input and display responses."""
        if prompt := st.chat_input("What's on your mind?", key="main_chat_input"):
            # Display user message
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            # Get and display assistant response
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    if response := self.on_message(prompt):
                        st.session_state.messages.append(
                            {"role": "assistant", "content": response}
                        )
                        st.markdown(response)
                    else:
                        st.error("Failed to get response from the assistant.")

    def render(self):
        """Render the complete chat interface."""
        self.display_messages()
        self.handle_input() 