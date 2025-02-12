# MultiAgent AI Coding

MultiAgent AI Coding system that first asks clarifying questions about the user's request, generates a detailed implementation plan, then uses specialized AI agents (a code writing agent to implement the solution and a code review agent to validate and improve the code) powered by various LLM providers through Portkey.ai, with support for both terminal and web interfaces.

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd multiagent-ai-coding
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Linux/Mac
# or
.\venv\Scripts\activate  # On Windows
```

3. Install the required dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file and configure the following environment variables. You can use .envtemplate as a template:

API keys:
- `PORTKEY_API_BASE`: Base URL for Portkey API (default: "https://api.portkey.ai/v1")
- `PORTKEY_API_KEY`: Your Portkey API key
- `PORTKEY_VIRTUAL_KEY_ANTHROPIC`: Virtual key for Anthropic models
- `PORTKEY_VIRTUAL_KEY_OPENAI`: Virtual key for OpenAI models
- `PORTKEY_VIRTUAL_KEY_GOOGLE`: Virtual key for Google models
- `ZEP_API_KEY`: Your Zepp API key
- `OSMOSIS_API_KEY`: Your Osmosis API key


Coding Agent System Prompts:
- `CODE_WRITING_AGENT_SYSTEM_PROMPT`: System prompt for code writing agent. This should be customized based on your project's needs - for example, whether you want the agent to focus on implementing core functionality quickly or take a more thorough approach with extensive error handling.
- `CODE_REVIEW_AGENT_SYSTEM_PROMPT`: System prompt for code review agent. The strictness level can be adjusted depending on your goals - from basic functionality verification to comprehensive error detection and optimization suggestions.

Coding Agent Settings:
- `CODING_AGENT_MODEL`: Model to use for coding (default: "claude-3-5-sonnet-latest")
- `MAX_AGENT_STEPS`: Maximum number of steps for agents (default: 20)
- `PLANNING_INTERVAL`: Interval at which the agent will run a planning step (default: 3)
- `USE_O3_PLANNING`: Whether to use planning with O3 model (default: "true")
- `USE_CLARIFYING_QUESTIONS`: Whether to use clarifying questions (default: "true")
- `USE_WEB_SEARCH`: Whether to use web search (default: "false")
- `INCLUDE_CODEBASE_IN_SYSTEM_PROMPT`: Whether to include codebase in system prompt (default: "true")
- `MORE_AUTHORIZED_IMPORTS`: Additional authorized imports (default: "streamlit,smolagents")

Path Settings
- `AI_PLAYGROUND_PATH`: Path for AI playground (default: "ai_playground/")
- `TESTS_PATH`: Path for tests (default: "tests/tests_multiagent_coding/")

## Using MultiAgent Coding System

### Setting Up Your Codebase

To use the MultiAgent Coding System with your own codebase:

1. Create a directory for your project in the `ai_playground` folder:
```bash
mkdir ai_playground
```

2. Place your codebase files in this directory. The MultiAgent Coding System will use this as the working directory for code generation, review, and modifications.

3. When using any of the MultiAgent Coding interfaces, your project in `ai_playground` will be automatically recognized and the agents will work within this context.

## Available Interfaces

### 1. Terminal Interface (memory isn't implemented)

To run:
```bash
python terminal_multiagent_coding.py
```

### 2. Web Interface (has memory)
To run:
```bash
python app_multiagent_coding.py
```
