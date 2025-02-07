from experiments.multiagent_coding.smolagents.multiagent_coding_smolagents import MultiAgentCoding

coding = MultiAgentCoding()
#result = coding.run("Write a Python function to calculate factorial recursively.")
result = coding.run("Add the simplest possible memory to the chatbot app. No databases, no saving to files. Just a simple in-memory dictionary to store the conversation history.")
print(result)
