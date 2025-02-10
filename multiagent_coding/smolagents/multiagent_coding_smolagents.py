import os

from smolagents import (
    CodeAgent,
    ToolCallingAgent,
    tool,
    ManagedAgent,
    GradioUI
)
from smolagents.prompts import CODE_SYSTEM_PROMPT

# from langchain_openai import ChatOpenAI
from multiagent_coding.smolagents.smolagents_portkey import PortkeyModel

from dotenv import load_dotenv
# Load environment variables
load_dotenv()

# Base paths from environment variables with defaults
AI_PLAYGROUND_PATH = os.getenv('AI_PLAYGROUND_PATH', "ai_playground/")
TESTS_PATH = os.getenv('TESTS_PATH', "tests/tests_multiagent_coding/")

# Create directories if they don't exist
os.makedirs(AI_PLAYGROUND_PATH, exist_ok=True)
os.makedirs(TESTS_PATH, exist_ok=True)

# Model configuration from environment variables
openrouter_api_key = os.getenv('OPENROUTER_API_KEY')
model = os.getenv('CODING_AGENT_MODEL', "claude-3-5-sonnet-latest")
max_steps = int(os.getenv('MAX_AGENT_STEPS', '20'))
planning_interval = int(os.getenv('PLANNING_INTERVAL', '3'))

# Authorized imports from environment variable, falling back to default list
default_imports = ["streamlit", "portkey", "smolagents", "stat", "statistics", "random", "queue", "time", "datetime", "math", "re",
            'unicodedata', 'itertools', 'collections', 'json', 'csv', 'os', 'sys', 'pathlib', 'typing',
            'dataclasses', 'enum', 'abc', 'functools', 'operator', 'copy', 'pprint', 'logging',
            'argparse', 'configparser', 'yaml', 'requests', 'urllib', 'http', 'socket', 'email',
            'hashlib', 'base64', 'uuid', 'decimal', 'fractions', 'numbers', 'array', 'bisect',
            'heapq', 'weakref', 'types', 'calendar', 'zoneinfo', 'locale', 'gettext', 'threading',
            'multiprocessing', 'concurrent', 'asyncio', 'contextvars', 'signal', 'mmap', 'readline',
            'rlcompleter', 'struct', 'codecs', 'encodings', 'io', 'tempfile', 'shutil', 'glob',
            'fnmatch', 'linecache', 'pickle', 'shelve', 'marshal', 'dbm', 'sqlite3', 'zlib', 'gzip',
            'bz2', 'lzma', 'zipfile', 'tarfile', 'csv', 'configparser', 'netrc', 'xdrlib', 'plistlib',
            'hmac', 'secrets', 'string', 'difflib', 'textwrap', 'threading', 'subprocess', 'streamlit', 'inspect', 'hashlib', 'os', 'typing']

authorized_imports = default_imports + os.getenv('MORE_AUTHORIZED_IMPORTS', '').split(',')

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

@tool
def get_codebase() -> str:
    """
    Generates a prompt containing the entire codebase by recursively reading all files except those in .gitignore.
    Checks for .gitignore files in root and subfolders.
    
    Returns:
        str: A formatted string containing all code with file paths as headers
    """
    codebase_prompt = []
    
    # Store gitignore patterns from all .gitignore files
    gitignore_patterns = {}
    
    def load_gitignore_patterns(directory):
        """Load gitignore patterns from a directory's .gitignore file if it exists"""
        gitignore_path = os.path.join(directory, '.gitignore')
        if os.path.exists(gitignore_path):
            try:
                with open(gitignore_path, 'r') as f:
                    return [line.strip() for line in f if line.strip() and not line.startswith('#')]
            except Exception as e:
                print(f"Error reading {gitignore_path}: {str(e)}")
        return []

    def is_ignored(path):
        """Check if path matches any gitignore pattern from parent directories"""
        rel_path = os.path.relpath(path, AI_PLAYGROUND_PATH)
        current_dir = os.path.dirname(path)
        
        # Check patterns from current and all parent directories
        while current_dir >= AI_PLAYGROUND_PATH:
            if current_dir in gitignore_patterns:
                for pattern in gitignore_patterns[current_dir]:
                    if pattern.endswith('/'):
                        if rel_path.startswith(pattern):
                            return True
                    elif pattern.startswith('*'):
                        if rel_path.endswith(pattern[1:]):
                            return True
                    elif pattern in rel_path:
                        return True
            current_dir = os.path.dirname(current_dir)
        return False

    # First pass: collect all gitignore patterns
    for root, _, _ in os.walk(AI_PLAYGROUND_PATH):
        patterns = load_gitignore_patterns(root)
        if patterns:
            gitignore_patterns[root] = patterns

    # Second pass: read files
    for root, _, files in os.walk(AI_PLAYGROUND_PATH):
        for file in files:
            if file == '.gitignore':
                continue
            file_path = os.path.join(root, file)
            if not is_ignored(file_path):
                try:
                    with open(file_path, 'r') as f:
                        content = f.read()
                        relative_path = os.path.relpath(file_path, AI_PLAYGROUND_PATH)
                        # Detect file type for syntax highlighting
                        ext = os.path.splitext(file)[1][1:]
                        if ext:
                            codebase_prompt.append(f"\n### {relative_path}\n```{ext}\n{content}\n```\n")
                        else:
                            codebase_prompt.append(f"\n### {relative_path}\n```\n{content}\n```\n")
                except Exception as e:
                    print(f"Error reading {file_path}: {str(e)}")
                    
    return "\n".join(codebase_prompt)

class MultiAgentCoding:
    def __init__(self):        
        self.model = PortkeyModel(model)
        
        # Load prompts from environment variables with defaults
        include_codebase = os.getenv('INCLUDE_CODEBASE_IN_SYSTEM_PROMPT', 'true').lower() == 'true'
        codebase_str = get_codebase() if include_codebase else ""
        
        code_writing_agent_system_prompt = os.getenv('CODE_WRITING_AGENT_SYSTEM_PROMPT', """
You are an expert Python programmer. 

When you receive a coding task, don't return the final code directly. Instead:

1. Write the initial code implementation
2. Call the code review agent to fix it using the code_review_agent tool
3. Return the final improved code to the user

Remember to:
- Always use function calling rather than direct responses
- Let the code review agent validate and improve the code
- Only return the final code after review and improvements
- Always save the code to a file using the write_file tool

When you generate code, send it to the code review critic agent! After its reviewed, send the final code back to the user.

You have access to the current project's files in development through the following tools:
- read_file: Read contents of a file
- read_directory: List contents of a directory
- write_file: Write content to a file

Do not do more than 5 iterations. Just quickly finish it.

Codebase:
""")
        
        # print("Code Writing Agent System Prompt:")
        # print(code_writing_agent_system_prompt)
        
        code_writing_agent_system_prompt = CODE_SYSTEM_PROMPT + code_writing_agent_system_prompt + codebase_str

        code_review_agent_system_prompt = os.getenv('CODE_REVIEW_AGENT_SYSTEM_PROMPT', """
You are an expert code reviewer. Your task is to review and fix the code provided to you. Make sure the code compiles functions correctly. When you are done fixing the code, send the final code back. Don't try to do too many changes, just make sure the code compiles and functions correctly. 

Don't be too harsh, you're not making production level code, just minimal changes to get the code to work.
""") 
        
        # print("Code Review Agent System Prompt:")
        # print(code_review_agent_system_prompt)

        code_review_agent_system_prompt = CODE_SYSTEM_PROMPT + code_review_agent_system_prompt # + codebase_str
       
        #self.code_review_agent = ToolCallingAgent(
        self.code_review_agent = CodeAgent(
            tools=[read_file, read_directory, write_file], # get_codebase
            model=self.model,
            system_prompt=code_review_agent_system_prompt,
            additional_authorized_imports=authorized_imports,
            max_steps=max_steps,
            planning_interval=planning_interval
        )
        
        self.managed_code_review_agent = ManagedAgent(
            agent=self.code_review_agent,
            name="code_review_agent",
            description="This is an agent that can review code and provide feedback."
        )

        #self.code_writing_agent = ToolCallingAgent(
        self.code_writing_agent = CodeAgent(
            tools=[read_file, read_directory, write_file], # get_codebase
            model=self.model,
            managed_agents=[self.managed_code_review_agent],
            system_prompt=code_writing_agent_system_prompt,
            additional_authorized_imports=authorized_imports,
            max_steps=max_steps,
            planning_interval=planning_interval
        )

        # Initialize Gradio UI
        self.ui = GradioUI(self.code_writing_agent)

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

    def launch_with_ui(self):
        """Launch the Gradio UI interface"""
        self.ui.launch()