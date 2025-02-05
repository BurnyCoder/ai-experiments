# AI Experiments

This repository contains various experiments and implementations related to AI agents, multi-agent systems, and language model interactions.

## Repository Structure

```
.
├── experiments/
│   ├── multiagent_coding/
│   │   ├── multiagent_coding_smolagents.py   # Implementation of small, focused coding agents
│   │   ├── fixed_prompt_pipeline.py          # Fixed prompt pipeline implementation
│   │   └── noncoding_examples_for_reference/ # Reference examples of non-coding tasks
│   └── aggregation.py                        # Aggregation experiment implementation
├── utils/
│   ├── openrouter.py                        # OpenRouter API integration utilities
│   └── openrotuermodels.txt                 # List of available OpenRouter models
├── run_multiagent_coding.py                 # Entry point for multi-agent coding experiments
├── run_aggregation.py                       # Entry point for aggregation experiments
├── run_openrouter.py                        # Entry point for OpenRouter-based experiments
└── prompts.md                               # Collection of prompts used in experiments
```

## Components

### Entry Points

- `run_multiagent_coding.py`: Main script to run multi-agent coding experiments
- `run_aggregation.py`: Script to execute aggregation experiments
- `run_openrouter.py`: Script to run OpenRouter-based experiments

### Experiments

#### Multi-agent Coding
Located in `experiments/multiagent_coding/`:
- `multiagent_coding_smolagents.py`: Implements small, focused agents for coding tasks
- `fixed_prompt_pipeline.py`: Contains a fixed prompt pipeline implementation
- Reference examples for non-coding scenarios are stored in `noncoding_examples_for_reference/`

#### Aggregation
- `experiments/aggregation.py`: Implementation of aggregation experiments

### Utilities

Located in `utils/`:
- `openrouter.py`: Provides utilities for interacting with the OpenRouter API
- `openrotuermodels.txt`: Contains a list of available models through OpenRouter

### Configuration

- `.env`: Environment variables and configuration settings
- `prompts.md`: Collection of prompts used across different experiments

## Dependencies

The project requires the following Python libraries:

### Core Dependencies
- `python-dotenv` - Environment variable management
- `requests` - HTTP requests for API interactions
- `smolagents` - Agent framework for multi-agent systems

### Language Model Integrations
- `langchain-anthropic` - Anthropic Claude integration
- `langchain-openai` - OpenAI integration
- `langchain-google-genai` - Google Generative AI integration
- `langchain-core` - Core LangChain functionality
- `langgraph` - Graph-based agent orchestration

### Document Processing & Search
- `langchain-community` - Community tools and utilities
- `langchain-experimental` - Experimental LangChain features
- `faiss-cpu` - Vector similarity search

### Telemetry & Monitoring
- `openinference` - Instrumentation for agent monitoring
- `opentelemetry-sdk` - Telemetry data collection
- `opentelemetry-exporter-otlp` - Telemetry data export

### Installation

Install all required dependencies using pip:

```bash
pip install -r requirements.txt
```

## Setup

1. Clone the repository
2. Create and configure your `.env` file with necessary API keys and settings
3. Install required dependencies

## Usage

Each experiment can be run using its corresponding entry point script:

```bash
# Run multi-agent coding experiments
python run_multiagent_coding.py

# Run aggregation experiments
python run_aggregation.py

# Run OpenRouter experiments
python run_openrouter.py
```

## Contributing

Feel free to submit issues and enhancement requests.

## License

[License information to be added]
