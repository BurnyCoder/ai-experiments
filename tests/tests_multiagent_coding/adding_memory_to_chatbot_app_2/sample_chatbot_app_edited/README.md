
# Chat Interface

A robust Streamlit-based chat interface with conversation memory, search capabilities, and clean separation between frontend and backend components.

## Features

- 💬 Clean, simple chat interface
- 🔍 Conversation search functionality
- 💾 Persistent conversation storage
- 🚀 Performance optimization with LRU caching
- 🧹 Automatic cleanup of old conversations
- 🎯 Clean separation of concerns
- 📝 Comprehensive error handling and logging

## Project Structure

## Setup

1. Install the required dependencies:

2. Create a `.env` file in the root directory with your API credentials:

## Running the Application

Start the Streamlit app:

The application will open in your default web browser.

## Features Guide

### Chat Interface
- Start new conversations with the "New Conversation" button
- Switch between previous conversations in the sidebar
- Delete individual conversations with the trash icon
- View message counts and timestamps for each conversation

### Search
- Use the search box in the sidebar to find specific conversations
- Search results show previews of matching messages
- Click "Load Conversation" to switch to a search result

### Settings
- Clean up old conversations automatically
- Clear the conversation cache
- Run manual cleanup operations

## Maintenance

### Cleaning Up Old Conversations

Use the cleanup utility to remove old or corrupted conversation files:

Options:
- `--storage-dir`: Directory containing conversation files
- `--max-age-days`: Maximum age of conversations to keep
- `--dry-run`: Preview what would be deleted without actually deleting

### Cache Management

The application uses LRU caching to improve performance. The cache:
- Stores up to 100 most recently accessed conversations
- Is automatically invalidated when conversations are deleted
- Can be manually cleared through the Settings panel

## Development

The codebase follows a clean architecture with:
- Separation between frontend and backend
- Comprehensive error handling
- Logging throughout the application
- Type hints for better code maintenance

### Key Components

1. ChatInterface (frontend/chat_interface.py)
   - Handles UI rendering and user interactions
   - Manages conversation display and navigation
   - Implements search interface

2. ConversationMemory (backend/memory.py)
   - Manages conversation persistence
   - Implements caching and search
   - Handles file operations

3. Chat Client (backend/portkey_chat_client.py)
   - Manages API communication
   - Handles message completions

## Note

Keep your API keys secure and never commit them to version control.
