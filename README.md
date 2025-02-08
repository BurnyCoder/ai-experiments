# AI Experiments Repository

This repository contains a collection of AI-powered tools and interfaces for different use cases. The main components include a MultiAgent Coding System, Multi-LLM Synthesis System, and various interfaces to interact with them.

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd ai-experiments
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

4. Create a `.env` file in the root directory with your API keys:
```bash
PORTKEY_API_KEY=your_portkey_api_key
PORTKEY_VIRTUAL_KEY_ANTHROPIC=your_portkey_virtual_key_for_anthropic
PORTKEY_VIRTUAL_KEY_OPENAI=your_portkey_virtual_key_for_openai
PORTKEY_VIRTUAL_KEY_GOOGLE=your_portkey_virtual_key_for_google
```

## Available Interfaces

### 1. Terminal Synthesis System (memory wasnt implemented yet)
A command-line interface for interacting with multiple LLMs and synthesizing their responses.

To run:
```bash
python terminal_synthesis.py
```

Features:
- Interactive prompt-based interface
- Displays individual responses from each model
- Shows synthesized final response
- Easy exit with 'exit' or 'quit' commands

### 2. MultiAgent Coding Web Interface (has memory)
A Gradio-based web interface for generating and reviewing code using a coder agent and a code reviewer agent.
To run:
```bash
python app_multiagent_coding.py
```

Features:
- User-friendly web interface
- Real-time code generation
- Code review and improvements
- Visual feedback and interactions

### 3. Terminal MultiAgent Coding (memory wasnt implemented yet)
A command-line interface for the MultiAgent Coding system.

To run:
```bash
python terminal_multiagent_coding.py
```

## Environment Variables

The following environment variables can be configured in your `.env` file. You can use .envtemplate as a template:

API keys:
- `PORTKEY_API_BASE`: Base URL for Portkey API (default: "https://api.portkey.ai/v1")
- `PORTKEY_API_KEY`: Your Portkey API key
- `PORTKEY_VIRTUAL_KEY_ANTHROPIC`: Virtual key for Anthropic models
- `PORTKEY_VIRTUAL_KEY_OPENAI`: Virtual key for OpenAI models
- `PORTKEY_VIRTUAL_KEY_GOOGLE`: Virtual key for Google models

Coding Agent Settings:
- `CODING_AGENT_MODEL`: Model to use for coding (default: "claude-3-5-sonnet-latest")
- `MAX_AGENT_STEPS`: Maximum number of steps for agents (default: 20)
- `AI_PLAYGROUND_PATH`: Path for AI playground (default: "ai_playground/")
- `TESTS_PATH`: Path for tests (default: "tests/tests_multiagent_coding/")
- `INCLUDE_CODEBASE_IN_SYSTEM_PROMPT`: Whether to include codebase in system prompt (default: "true")
- `MORE_AUTHORIZED_IMPORTS`: Additional authorized imports (default: "streamlit,smolagents")

Coding Agent System Prompts:
- `CODE_WRITING_AGENT_SYSTEM_PROMPT`: System prompt for code writing agent
- `CODE_REVIEW_AGENT_SYSTEM_PROMPT`: System prompt for code review agent
