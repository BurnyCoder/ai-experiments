# Chat Interface

A minimalist Streamlit-based chat interface with a clean separation between frontend and backend components, powered by Portkey AI.

## Project Structure

```
.
├── backend/
│   ├── portkey_chat_client.py  # Portkey API wrapper
│   └── openai_chat_client.py   # OpenAI API wrapper (alternative)
├── frontend/
│   └── chat_interface.py       # Streamlit UI components
├── app.py                      # Main application
├── requirements.txt            # Dependencies
└── README.md                   # This file
```

## Setup

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file in the root directory with your Portkey API credentials:
```bash
PORTKEY_API_KEY=your_portkey_api_key_here
PORTKEY_VIRTUAL_KEY_ANTHROPIC=your_portkey_virtual_key_here
```

## Running the Application

Start the Streamlit app by running:
```bash
python -m streamlit run app.py
```

The application will open in your default web browser. You can then start chatting through the simple interface.

## Features

- Clean separation of concerns between frontend and backend
- Clean, simple chat interface
- Real-time responses from Claude 3.5 Sonnet via Portkey

## Note

Make sure to keep your API keys secure and never commit them to version control.