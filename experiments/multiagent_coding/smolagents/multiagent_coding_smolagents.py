from dotenv import load_dotenv
import os

from smolagents import (
    CodeAgent,
    ToolCallingAgent,
    tool,
    ManagedAgent
)
from smolagents import LiteLLMModel, OpenAIServerModel
from smolagents.prompts import CODE_SYSTEM_PROMPT

# from langchain_openai import ChatOpenAI
from portkey_ai import createHeaders, PORTKEY_GATEWAY_URL
from utils.portkey import gemini2flashthinking
from experiments.multiagent_coding.smolagents.smolagents_portkey import PortkeyModel

load_dotenv()
openrouter_api_key = os.getenv('OPENROUTER_API_KEY')
#model = "claude-3-5-sonnet-latest"
# model = "gemini-2.0-flash-thinking-exp-01-21"
# model = "gemini-2.0-pro-exp-02-05"
# model = "gemini-2.0-pro-exp"
# model = "gemini-2.0-pro-exp"
#model = "gemini-exp-1206"
model = "gemini-2.0-flash"

@tool
def read_file(filepath: str) -> str:
    """
    Reads and returns the contents of a file.
    Args:
        filepath: Path to the file to read
    Returns:
        str: Contents of the file if successful, error message if failed
    """
    path = "experiments/multiagent_coding/smolagents/ai_playground/"+filepath
    try:
        with open(path, 'r') as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {str(e)}"

@tool 
def read_directory(dirpath: str) -> str:
    """
    Lists contents of a directory.
    Args:
        dirpath: Path to the directory to read
    Returns:
        str: List of files and folders in the directory if successful, error message if failed
    """
    path = "experiments/multiagent_coding/smolagents/ai_playground/"+dirpath
    try:
        contents = os.listdir(path)
        return "\n".join(contents)
    except Exception as e:
        return f"Error reading directory: {str(e)}"

@tool
def write_file(filepath: str, content: str) -> str:
    """
    Writes content to a file.
    Args:
        filepath: Path where to write the file
        content: Content to write to the file
    Returns:
        str: Success message if written, error message if failed
    """
    path = "experiments/multiagent_coding/smolagents/ai_playground/"+filepath
    try:
        with open(path, 'w') as f:
            f.write(content)
        return f"Successfully wrote to {path}"
    except Exception as e:
        return f"Error writing file: {str(e)}"


class MultiAgentCoding:
    def __init__(self):        
        self.model = PortkeyModel(model)
               
        code_writing_agent_system_prompt = CODE_SYSTEM_PROMPT + """
You are an expert Python programmer. Your task is to write clean, efficient, and well-documented code based on the given requirements.
Follow these guidelines:
- Write code that follows PEP 8 style guidelines
- Include clear docstrings and comments
- Use descriptive variable names
- Write modular and reusable code
- Handle edge cases and errors appropriately
- Focus on readability and maintainability

When you generate code, send it to the code review critic agent! After its reviewed, send the final code back to the user.
""" + """
When you receive a coding task, don't return the final code directly. Instead:

1. Write the initial code implementation
2. Call the code review agent to review it using the code_review_agent tool
3. Incorporate the feedback and improvements
4. Return the final improved code

Remember to:
- Always use function calling rather than direct responses
- Let the code review agent validate and improve the code
- Only return the final code after review and improvements
"""

        code_review_agent_system_prompt = CODE_SYSTEM_PROMPT + """
You are an expert code reviewer. Your task is to review and fix the code provided by the user.
Focus on:
- Code correctness and functionality
- Style and PEP 8 compliance
- Documentation and comments
- Error handling
- Performance and efficiency
- Code organization and structure
- Potential bugs or issues
- Suggestions for improvement

When you are done fixing the code, send the final code back to the user.
"""

        #self.code_review_agent = ToolCallingAgent(
        self.code_review_agent = CodeAgent(
            tools=[read_file, read_directory, write_file],
            model=self.model,
            system_prompt=code_review_agent_system_prompt,
            #use_e2b_executor=True
        )
        
        self.managed_code_review_agent = ManagedAgent(
            agent=self.code_review_agent,
            name="code_review_agent",
            description="This is an agent that can review code and provide feedback.",
        )

        self.code_writing_agent = ToolCallingAgent(
        #self.code_writing_agent = CodeAgent(
            tools=[read_file, read_directory, write_file],
            model=self.model,
            managed_agents=[self.managed_code_review_agent],
            system_prompt=code_writing_agent_system_prompt,
            #use_e2b_executor=True
        )

    def run(self, prompt):
        return self.code_writing_agent.run(prompt)

    def test(self):
        return self.code_writing_agent.run("Write a Python function to calculate factorial recursively.")
    
    def codebase_to_prompt(self):
        #https://github.com/mufeedvh/code2prompt
        return None