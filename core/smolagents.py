import os
import logging
import json
from datetime import datetime

from smolagents import (
    CodeAgent,
    ToolCallingAgent,
    tool,
    ManagedAgent,
    GradioUI,
    DuckDuckGoSearchTool
)
from smolagents.prompts import CODE_SYSTEM_PROMPT
from smolagents.memory import TaskStep, ActionStep

# from langchain_openai import ChatOpenAI
from core.smolagents_portkey_support import PortkeyModel
from core.portkey_api import o3minihigh, claude35sonnet

from core.osmosis_api import OsmosisAPI
store_knowledge = OsmosisAPI().store_knowledge
delete_by_intent = OsmosisAPI().delete_by_intent

from dotenv import load_dotenv
# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(
    level=logging.WARNING,  # Changed from INFO to WARNING to disable most logs
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
logger.disabled = True  # Disable this logger

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
use_planning = os.getenv('USE_O3_PLANNING', 'true').lower() == 'true'
use_clarifying_questions = os.getenv('USE_CLARIFYING_QUESTIONS', 'true').lower() == 'true'
use_web_search = os.getenv('USE_WEB_SEARCH', 'false').lower() == 'true'

planning_model = o3minihigh 
clarifying_model = o3minihigh 

planning_agent_system_prompt = os.getenv('PLANNING_AGENT_SYSTEM_PROMPT', """
Given a coding task, generate a clear, step-by-step plan that outlines:
1. What needs to be implemented
2. The sequence of steps to implement it

Format the response as a markdown list with clear sections.

Remember to:
- Be specific and actionable
- Break down complex tasks into manageable pieces

You're not making production level code, you're just making minimal changes to get the code to work.
""")

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
            'bz2', 'lzma', 'zipfile', 'tarfile', 'netrc', 'xdrlib', 'plistlib', 'hmac', 'secrets',
            'string', 'difflib', 'textwrap', 'subprocess', 'inspect', 'msvcrt', 'turtle', 'tty',
            'termios', 'fcntl', 'select', 'ssl', 'pygame', 'curses']

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
    logger.debug(f"Reading file: {filepath}")
    path = os.path.join(AI_PLAYGROUND_PATH, filepath)
    try:
        with open(path, 'r') as f:
            content = f.read()
            logger.debug(f"Successfully read file: {filepath}")
            return content
    except Exception as e:
        logger.error(f"Error reading file {filepath}: {str(e)}")
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
    logger.debug(f"Reading directory: {dirpath}")
    path = os.path.join(AI_PLAYGROUND_PATH, dirpath)
    try:
        contents = os.listdir(path)
        logger.debug(f"Successfully read directory: {dirpath}")
        return "\n".join(contents)
    except Exception as e:
        logger.error(f"Error reading directory {dirpath}: {str(e)}")
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
    logger.debug(f"Writing to file: {filepath}")
    path = os.path.join(AI_PLAYGROUND_PATH, filepath)
    try:
        # Create parent directories if they don't exist
        os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
        with open(path, 'w') as f:
            f.write(content)
        logger.debug(f"Successfully wrote to file: {filepath}")
        return f"Successfully wrote to {path}"
    except Exception as e:
        logger.error(f"Error writing to file {filepath}: {str(e)}")
        return f"Error writing file: {str(e)}"

@tool
def get_codebase() -> str:
    """
    Generates a prompt containing the entire codebase by recursively reading all code files (.py, .js, .css, .html, .ts, etc.)
    except those in .gitignore. Checks for .gitignore files in root and subfolders.
    
    Returns:
        str: A formatted string containing all code with file paths as headers
    """
    logger.debug("Getting codebase")
    codebase_prompt = []
    
    # Code file extensions to include
    CODE_EXTENSIONS = {'.py', '.js', '.jsx', '.ts', '.tsx', '.css', '.scss', '.html', '.vue', '.go', '.java', '.cpp', '.c', '.h', '.rs', '.sql', '.md', '.txt', '.json', '.yaml', '.yml', '.toml', '.ini', '.conf', '.cfg', '.properties', '.env', '.lock', '.lockb', '.lock.json', '.lock.yaml', '.lock.yml', '.lock.toml', '.lock.ini', '.lock.conf', '.lock.cfg', '.lock.properties', '.lock.env'}
    
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
                logger.error(f"Error reading {gitignore_path}: {str(e)}")
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
    logger.debug("Collecting gitignore patterns")
    for root, _, _ in os.walk(AI_PLAYGROUND_PATH):
        patterns = load_gitignore_patterns(root)
        if patterns:
            gitignore_patterns[root] = patterns

    # Second pass: read files
    logger.debug("Reading files for codebase")
    for root, _, files in os.walk(AI_PLAYGROUND_PATH):
        for file in files:
            file_path = os.path.join(root, file)
            file_ext = os.path.splitext(file)[1]
            
            if file_ext not in CODE_EXTENSIONS:
                continue
                
            if not is_ignored(file_path):
                try:
                    with open(file_path, 'r') as f:
                        content = f.read()
                        relative_path = os.path.relpath(file_path, AI_PLAYGROUND_PATH)
                        # Detect file type for syntax highlighting
                        ext = file_ext[1:]  # Remove the dot
                        codebase_prompt.append(f"\n### {relative_path}\n```{ext}\n{content}\n```\n")
                except Exception as e:
                    logger.error(f"Error reading {file_path}: {str(e)}")
                    
    logger.debug("Successfully generated codebase")
    return "\n".join(codebase_prompt)

@tool
def generate_plan(prompt: str) -> str:
    """
    Generates a plan for the given coding task using o3-mini-high model.
    
    Args:
        prompt: The user's coding task request
        
    Returns:
        str: A detailed plan outlining the steps to complete the task
    """
    logger.debug("Generating plan")
    planning_prompt = f"""
{planning_agent_system_prompt}

Given this coding task:
{prompt}

Codebase:
{get_codebase()}
"""

    plan = planning_model(planning_prompt)
    logger.debug("Successfully generated plan")
    return planning_prompt, plan

@tool
def ask_clarifying_questions(prompt: str) -> list:
    """
    Generates clarifying questions for the given coding task using o3-mini-high model.
    
    Args:
        prompt: The user's coding task request
        
    Returns:
        list: A list of clarifying questions
    """
    logger.debug("Generating clarifying questions")
    clarifying_prompt = f"""
Given this coding task, what clarifying questions would you ask to better understand the requirements?
Please respond with a JSON array containing 3 key questions that would help clarify any ambiguities.
Format the response as: ["question 1", "question 2", "question 3"]

Task:
{prompt}

Codebase:
{get_codebase()}
"""

    questions_json = clarifying_model(clarifying_prompt)
    import json
    questions = json.loads(questions_json)
    logger.debug("Successfully generated clarifying questions")
    return clarifying_prompt, questions

class MultiAgentCoding:
    def __init__(self):
        logger.info("Initializing MultiAgentCoding")
        self.model = PortkeyModel(model)
        
        # Load prompts from environment variables with defaults
        include_codebase = os.getenv('INCLUDE_CODEBASE_IN_SYSTEM_PROMPT', 'true').lower() == 'true'
        codebase_str = get_codebase() if include_codebase else ""
        
        code_writing_agent_system_prompt = os.getenv('CODE_WRITING_AGENT_SYSTEM_PROMPT', """
You are an expert Python programmer. 

When you receive a coding task:

1. First ask clarifying questions using the ask_clarifying_questions tool
2. Get and review the generated plan from the planning tool
3. Create your implementation plan based on the generated plan
4. Write the initial code implementation
5. Call the code review agent to fix it using the code_review_agent tool
6. Return the final improved code to the user

ALWAYS ask clarifying questions before starting.
ALWAYS use the planning tool to get a plan for the coding task before writing any code.
ALWAYS use the code review agent to review the code after it's written.

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
- generate_plan: Generate a detailed plan for the coding task
- ask_clarifying_questions: Ask clarifying questions about the task

Do not do more than 5 iterations. Just quickly finish it.

Codebase:
""")
        
        code_writing_agent_system_prompt = CODE_SYSTEM_PROMPT + code_writing_agent_system_prompt + codebase_str

        code_review_agent_system_prompt = os.getenv('CODE_REVIEW_AGENT_SYSTEM_PROMPT', """
You are an expert code reviewer. Your task is to review and fix the code provided to you. Make sure the code compiles functions correctly. When you are done fixing the code, send the final code back. Don't try to do too many changes, just make sure the code compiles and functions correctly. 

Don't be too harsh, you're not making production level code, just minimal changes to get the code to work.
""") 
        
        code_review_agent_system_prompt = CODE_SYSTEM_PROMPT + code_review_agent_system_prompt # + codebase_str
               
        # Build tools list based on USE_PLANNING and USE_CLARIFYING_QUESTIONS env vars
        tools = [read_file, read_directory, write_file]
        if use_web_search:
            tools.append(DuckDuckGoSearchTool())
        # if use_clarifying_questions:
        #     tools.append(ask_clarifying_questions)
        # if use_planning:
        #     tools.append(generate_plan)

        logger.info("Initializing code review agent")
        self.code_review_agent = CodeAgent(
            tools=tools,
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

        logger.info("Initializing code writing agent")
        self.code_writing_agent = CodeAgent(
            tools=tools,
            model=self.model,
            managed_agents=[self.managed_code_review_agent],
            system_prompt=code_writing_agent_system_prompt,
            additional_authorized_imports=authorized_imports,
            max_steps=max_steps,
            planning_interval=planning_interval
        )

        self.ui = GradioUI(self.code_writing_agent)
        
        # Initialize instance variables
        self.questions = None
        self.plan = None
        self.prompt = None
        self.result = None

    def save_logs(self, base_path, agent):
        """Save agent logs with incrementing number if file exists.
        
        Args:
            base_path (str): Base path to save logs to
            agent (Agent): Agent to get logs from
        
        Returns:
            str: Path where logs were saved
        """
        logger.debug(f"Saving logs to {base_path}")
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
            logger.info(f"Logs saved to: {log_file}")
            return log_file
        except Exception as e:
            logger.error(f"Error saving logs: {str(e)}")
            return None

    def _store_agent_knowledge(self):
        """Store agent interactions and knowledge for future reference"""
        turns = []
        turn_counter = 0
        
        # Add clarifying questions turn if questions were asked
        if self.questions:
            turn_counter += 1
            turns.append({
                "turn": turn_counter,
                "inputs": self.clarifying_prompt,
                "decision": json.dumps(self.questions),
                "memory": "Generated clarifying questions",
                "result": self.questions
            })

        # Add planning turn if plan was generated
        if self.plan:
            turn_counter += 1
            turns.append({
                "turn": turn_counter,
                "inputs": self.planning_prompt,
                "decision": "Generate implementation plan",
                "memory": "Generated implementation plan",
                "result": self.plan
            })

        # Add implementation turns
        turn_counter += 1
        turns.append({
            "turn": turn_counter,
            "inputs": self.prompt,
            "decision": "Generate code implementation",
            "memory": "Generated code implementation",
            "result": self.result
        })

        # Convert agent memory steps to turns
        if hasattr(self.code_writing_agent, 'memory') and self.code_writing_agent.memory:
            for step in self.code_writing_agent.memory.steps:
                turn_counter += 1
                
                if isinstance(step, TaskStep):
                    turns.append({
                        "turn": turn_counter,
                        "inputs": step.task,
                        "decision": "Task definition",
                        "memory": "Defined task",
                        "result": None
                    })
                
                elif isinstance(step, ActionStep):
                    # Extract input messages
                    inputs = []
                    for msg in step.model_input_messages:
                        for content in msg['content']:
                            if content['type'] == 'text':
                                inputs.append(content['text'])
                    
                    # Extract tool calls
                    tool_info = []
                    if step.tool_calls:
                        for call in step.tool_calls:
                            tool_info.append({
                                "name": call.name,
                                "arguments": call.arguments,
                                "id": call.id
                            })
                    
                    turns.append({
                        "turn": turn_counter,
                        "inputs": "\n".join(inputs),
                        "decision": json.dumps(tool_info) if tool_info else step.model_output,
                        "memory": f"Step {step.step_number} execution",
                        "result": step.action_output
                    })

        # Save turns to file for debugging
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        turns_file = os.path.join(TESTS_PATH, f"turns_{timestamp}.txt")
        with open(turns_file, 'w') as f:
            f.write(str(turns))
        
        # Store the knowledge
        store_knowledge(
            query=self.prompt,
            turns=turns,
            success=True,
            agent_type="code_writing"
        )

    def run_terminal(self, prompt):
        logger.info("Running terminal with prompt")
        self.planning_prompt = prompt
        self.questions = None
        self.plan = None
        self.prompt = prompt
        
        # First ask clarifying questions
        if use_clarifying_questions:
            print("Figuring out clarifying questions...\n")
            self.clarifying_prompt, self.questions = ask_clarifying_questions(prompt)
            
            print(f"Clarifying Questions:")
            for i, question in enumerate(self.questions, 1):
                print(f"\n{i}. {question}")
                answer = input(f"\nYour answer to question {i}: \n").strip()
                self.prompt += f"\nQ: {question}\nA: {answer}"
                self.planning_prompt += f"\nClarifying Question: {question}\nAnswer from the user: {answer}"
        
        # Generate and execute plan
        if use_planning:
            print("\nGenerating plan...\n")
            self.planning_prompt, self.plan = generate_plan(self.planning_prompt)
            print(f"\nPlan: {self.plan}")
            self.result = self.code_writing_agent.run(self.plan)
        else:
            logger.info("Running code writing agent without plan")
            self.result = self.code_writing_agent.run(self.prompt)

        # Store knowledge and save logs
        self._store_agent_knowledge()
        logger.info("Saving logs")
        log_file = self.save_logs(TESTS_PATH, self.code_writing_agent)
        
        return self.result

    def launch_with_ui(self):
        """Launch the Gradio UI interface"""
        logger.info("Launching Gradio UI")
        self.ui.launch()