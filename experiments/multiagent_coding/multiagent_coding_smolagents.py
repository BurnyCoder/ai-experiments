from dotenv import load_dotenv
import os

from smolagents import (
    CodeAgent,
    ToolCallingAgent,
    tool
)
from smolagents import LiteLLMModel
from smolagents.prompts import CODE_SYSTEM_PROMPT

load_dotenv()
openrouter_api_key = os.getenv('OPENROUTER_API_KEY')

@tool
def read_file(filepath: str) -> str:
    """
    Reads and returns the contents of a file.
    Args:
        filepath: Path to the file to read
    Returns:
        str: Contents of the file if successful, error message if failed
    """
    try:
        with open(filepath, 'r') as f:
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
    try:
        contents = os.listdir(dirpath)
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
    try:
        with open(filepath, 'w') as f:
            f.write(content)
        return f"Successfully wrote to {filepath}"
    except Exception as e:
        return f"Error writing file: {str(e)}"


class MultiAgentCoding:
    def __init__(self):
        self.model = LiteLLMModel("openrouter/anthropic/claude-3-5-sonnet")
        
        modified_system_prompt = CODE_SYSTEM_PROMPT + "\nAlways send your generated code to the critic! Send all the relevant bits from the codebase!" # Change the system prompt here

        self.code_review_agent = CodeAgent(
            tools=[read_file, read_directory, write_file],
            model=self.model,
            name="code_review_agent", 
            description="This is an agent that can review code and provide feedback.",
            use_e2b_executor=True
        )

        self.code_writing_agent = CodeAgent(
            tools=[read_file, read_directory, write_file],
            model=self.model,
            managed_agents=[self.code_review_agent],
            use_e2b_executor=True
            #system_prompt=modified_system_prompt
        )

    def run(self, prompt):
        return self.code_writing_agent.run(prompt)

    def test(self):
        return self.code_writing_agent.run("Write a Python function to calculate factorial recursively.")
    
    def codebase_to_prompt(self):
        #https://github.com/mufeedvh/code2prompt
        return None