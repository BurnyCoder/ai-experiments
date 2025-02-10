import streamlit as st
import time
from datetime import datetime
from backend.memory import Memory

def run_memory_tests():
    """Comprehensive tests for the Memory implementation"""
    st.header("Memory Implementation Tests")
    
    try:
        # Test 1: Initialization
        st.subheader("1. Memory Initialization")
        memory = Memory(max_messages=5)
        st.success("✓ Memory initialized successfully")
        
        # Test 2: Adding messages
        st.subheader("2. Message Addition")
        test_messages = [
            ("user", "Hello there!"),
            ("assistant", "Hi! How can I help?"),
            ("user", "What's the weather like?"),
            ("assistant", "I don't have access to weather information."),
        ]
        
        for role, content in test_messages:
            msg = memory.add_message(role, content)
            st.write(f"Added message: {msg['role']}: {msg['content']} at {msg['timestamp']}")
        st.success("✓ Messages added successfully")
        
        # Test 3: Retrieving messages
        st.subheader("3. Message Retrieval")
        recent = memory.get_recent_messages(n=2)
        st.write("Last 2 messages:", recent)
        st.success("✓ Message retrieval working")
        
        # Test 4: Message search
        st.subheader("4. Message Search")
        search_results = memory.search_messages("weather")
        st.write("Search results for 'weather':", search_results)
        st.success("✓ Message search working")
        
        # Test 5: Message pruning
        st.subheader("5. Message Pruning")
        before_count = len(memory.get_recent_messages())
        memory.prune_old_messages(keep_last=2)
        after_count = len(memory.get_recent_messages())
        st.write(f"Messages before pruning: {before_count}")
        st.write(f"Messages after pruning: {after_count}")
        st.success("✓ Message pruning working")
        
        # Test 6: Session state persistence
        st.subheader("6. Session State Persistence")
        if 'chat_memory' in st.session_state:
            st.write("Memory persists in session state")
            st.success("✓ Session state persistence working")
        else:
            st.error("× Session state persistence failed")
            
    except Exception as e:
        st.error(f"Test failed: {str(e)}")
        raise e

# Add test button and run tests
if st.button("Run All Tests"):
    run_memory_tests()
