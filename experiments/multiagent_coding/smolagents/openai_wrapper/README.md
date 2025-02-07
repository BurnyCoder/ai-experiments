# Simple GPT-4 Chat Interface

A minimalist Streamlit-based chat interface for OpenAI's GPT-4 model, with a clean separation between frontend and backend components.

## Project Structure

```
.
├── backend/
│   └── chat_client.py    # OpenAI API wrapper
├── frontend/
│   └── chat_interface.py # Streamlit UI components
├── app.py               # Main application
├── requirements.txt     # Dependencies
└── README.md           # This file
```

## Setup

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file in the root directory with your OpenAI API key:
```bash
OPENAI_API_KEY=your_api_key_here
```

## Running the Application

Start the Streamlit app by running:
```bash
streamlit run app.py
```

The application will open in your default web browser. You can then start chatting with GPT-4 through the simple interface.

## Features

- Clean separation of concerns between frontend and backend
- Modular and maintainable code structure
- Clean, simple chat interface
- Message history persistence during session
- Real-time responses from GPT-4
- Loading spinner while waiting for responses
- Error handling for failed API calls

## Note

Make sure to keep your API key secure and never commit it to version control.