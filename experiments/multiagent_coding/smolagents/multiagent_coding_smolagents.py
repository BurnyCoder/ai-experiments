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

# Base path for AI playground
AI_PLAYGROUND_PATH = "experiments/multiagent_coding/smolagents/ai_playground/"
TESTS_PATH = "experiments/multiagent_coding/smolagents/tests/"

# Create directories if they don't exist
os.makedirs(AI_PLAYGROUND_PATH, exist_ok=True)
os.makedirs(TESTS_PATH, exist_ok=True)

load_dotenv()
openrouter_api_key = os.getenv('OPENROUTER_API_KEY')
model = "claude-3-5-sonnet-latest"
# model = "gemini-2.0-flash-thinking-exp-01-21"
# model = "gemini-2.0-pro-exp-02-05"
# model = "gemini-2.0-pro-exp"
# model = "gemini-2.0-pro-exp"
# model = "gemini-exp-1206"
# model = "gemini-2.0-flash"

authorized_imports = ["streamlit", "portkey", "smolagents", "stat", "statistics", "random", "queue", "time", "datetime", "math", "re",
            'unicodedata', 'itertools', 'collections', 'json', 'csv', 'os', 'sys', 'pathlib', 'typing',
            'dataclasses', 'enum', 'abc', 'functools', 'operator', 'copy', 'pprint', 'logging',
            'argparse', 'configparser', 'yaml', 'requests', 'urllib', 'http', 'socket', 'email',
            'hashlib', 'base64', 'uuid', 'decimal', 'fractions', 'numbers', 'array', 'bisect',
            'heapq', 'weakref', 'types', 'calendar', 'zoneinfo', 'locale', 'gettext', 'threading',
            'multiprocessing', 'concurrent', 'asyncio', 'contextvars', 'signal', 'mmap', 'readline',
            'rlcompleter', 'struct', 'codecs', 'encodings', 'io', 'tempfile', 'shutil', 'glob',
            'fnmatch', 'linecache', 'pickle', 'shelve', 'marshal', 'dbm', 'sqlite3', 'zlib', 'gzip',
            'bz2', 'lzma', 'zipfile', 'tarfile', 'csv', 'configparser', 'netrc', 'xdrlib', 'plistlib',
            'hmac', 'secrets', 'string', 'difflib', 'textwrap', 'threading', 'subprocess', 'streamlit']

@tool
def read_file(filepath: str) -> str:
    """
    Reads and returns the contents of a file.
    Args:
        filepath: Path to the file to read
    Returns:
        str: Contents of the file if successful, error message if failed
    """
    path = os.path.join(AI_PLAYGROUND_PATH, filepath)
    try:
        with open(path, 'r') as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {str(e)}"

@tool 
def read_directory(dirpath: str = "") -> str:
    """
    Lists contents of a directory.
    Args:
        dirpath: Path to the directory to read. If empty, returns contents of entire project directory.
    Returns:
        str: List of files and folders in the directory if successful, error message if failed
    """
    path = os.path.join(AI_PLAYGROUND_PATH, dirpath)
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
    path = os.path.join(AI_PLAYGROUND_PATH, filepath)
    try:
        # Create parent directories if they don't exist
        os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
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

You have access to the current project's files in development through the following tools:
- read_file: Read contents of a file
- read_directory: List contents of a directory
- write_file: Write content to a file

When you generate code, send it to the code review critic agent! After its reviewed, send the final code back to the user.
""" + """
When you receive a coding task, don't return the final code directly. Instead:

1. Write the initial code implementation
2. Call the code review agent to review it using the code_review_agent tool
3. Incorporate the feedback and improvements
4. Return the final improved code

You have access to the current project's files in development through the following tools:
- read_file: Read contents of a file
- read_directory: List contents of a directory
- write_file: Write content to a file

Remember to:
- Always use function calling rather than direct responses
- Let the code review agent validate and improve the code
- Only return the final code after review and improvements
- Always save the code to a file using the write_file tool
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
            additional_authorized_imports=authorized_imports,
            max_steps=20,
            #use_e2b_executor=True
        )
        
        self.managed_code_review_agent = ManagedAgent(
            agent=self.code_review_agent,
            name="code_review_agent",
            description="This is an agent that can review code and provide feedback.",
        )

        #self.code_writing_agent = ToolCallingAgent(
        self.code_writing_agent = CodeAgent(
            tools=[read_file, read_directory, write_file],
            model=self.model,
            managed_agents=[self.managed_code_review_agent],
            system_prompt=code_writing_agent_system_prompt,
            additional_authorized_imports=authorized_imports,
            max_steps=20,
            #use_e2b_executor=True
        )

    def save_logs(self, base_path, agent):
        """Save agent logs with incrementing number if file exists.
        
        Args:
            base_path (str): Base path to save logs to
            agent (Agent): Agent to get logs from
        
        Returns:
            str: Path where logs were saved
        """
        # Create base directory if it doesn't exist
        os.makedirs(base_path, exist_ok=True)
        
        log_file = os.path.join(base_path, "agent.logs")
        counter = 1
        while os.path.exists(log_file):
            log_file = os.path.join(base_path, f"agent_{counter}.logs")
            counter += 1
            
        try:
            with open(log_file, 'w') as f:
                f.write(str(agent.memory.steps))
            print(f"Logs saved to: {log_file}")
            return log_file
        except Exception as e:
            print(f"Error saving logs: {str(e)}")
            return None

    def run(self, prompt):
        result = self.code_writing_agent.run(prompt)
        self.save_logs(TESTS_PATH, self.code_writing_agent)
        return result

    def codebase_to_prompt(self):
        #https://github.com/mufeedvh/code2prompt
        return None