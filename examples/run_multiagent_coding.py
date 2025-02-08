from multiagent_coding.smolagents.multiagent_coding_smolagents import MultiAgentCoding

coding = MultiAgentCoding()
result = coding.run("Write a Python function to calculate factorial recursively.")
#result = coding.run("Add the simplest possible memory to the chatbot app. No databases, no saving to files. Just a simple in-memory dictionary to store the conversation history.")
# result = coding.run("""
# Fix this error:
# AttributeError: 'ChatMemory' object has no attribute '_cleanup_old_conversations'
# Traceback:
# File "/home/burny/.local/lib/python3.11/site-packages/streamlit/runtime/scriptrunner/script_runner.py", line 535, in _run_script
#     exec(code, module.__dict__)
# File "/home/burny/Desktop/josef/ai-experiments/experiments/multiagent_coding/smolagents/ai_playground/chatbot_app/app.py", line 28, in <module>
#     st.session_state.conversation_id = st.session_state.chat_memory.create_conversation()
#                                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# File "/home/burny/Desktop/josef/ai-experiments/experiments/multiagent_coding/smolagents/ai_playground/chatbot_app/backend/chat_memory.py", line 57, in create_conversation
#     self._cleanup_old_conversations()
#     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# """)
# result = coding.run("""
# Fix this error:
# INFO:backend.chat_memory:Initialized new ChatMemory instance
# INFO:__main__:Initialized new chat memory in session state
# INFO:__main__:Created new conversation: ad838f67-4a09-4413-b020-8455815cf8f4
# 2025-02-07 16:24:30.494 Uncaught app exception
# Traceback (most recent call last):
#   File "/home/burny/.local/lib/python3.11/site-packages/streamlit/runtime/scriptrunner/script_runner.py", line 535, in _run_script
#     exec(code, module.__dict__)
#   File "/home/burny/Desktop/josef/ai-experiments/experiments/multiagent_coding/smolagents/ai_playground/chatbot_app/app.py", line 84, in <module>
#     stats = st.session_state.chat_memory.get_conversation_stats(st.session_state.conversation_id)
#             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# AttributeError: 'ChatMemory' object has no attribute 'get_conversation_stats'
# """)

# result = coding.run("""
# Run the chatbot app accordign to readme.md. Tell me back how exactly do i access it on what url after you launch it.
# """)

# result = coding.run("""
# Run the chatbot app with "python -m streamlit run chatbot_app/app.py". Tell me back how exactly do i access it on what url after you launch it. Do not give me guide on how to run it, run it yoruself and tell me where to access it.
# """)


print(result)
