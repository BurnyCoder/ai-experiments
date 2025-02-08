import os
from dotenv import load_dotenv
from portkey_ai import Portkey
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)

class PortkeyClient:
    """A wrapper class for Portkey chat completions with Claude model."""

    def __init__(self):
        """Initialize the Portkey client with API keys from environment."""
        load_dotenv()
        
        # Validate API keys
        self.api_key = os.getenv("PORTKEY_API_KEY")
        self.virtual_key = os.getenv("PORTKEY_VIRTUAL_KEY_ANTHROPIC")
        
        if not self.api_key or not self.virtual_key:
            raise ValueError("Missing required API keys")
            
        self.client = Portkey(
            api_key=self.api_key,
            virtual_key=self.virtual_key
        )
        
        # Default model configuration
        self.default_model = "claude-3-sonnet-20240229"
        self.default_system_prompt = "You are a helpful assistant."

    def _format_messages(self, messages: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """Format messages for Claude model.
        
        Args:
            messages: List of message dictionaries
            
        Returns:
            Formatted messages list
        """
        # Ensure we have at least a system message
        if not messages or messages[0].get('role') != 'system':
            messages.insert(0, {
                'role': 'system',
                'content': self.default_system_prompt
            })
            
        # Format messages for Claude
        formatted_messages = []
        for msg in messages:
            # Validate message format
            if not isinstance(msg, dict) or 'role' not in msg or 'content' not in msg:
                continue
            
            role = msg['role']
            content = msg['content']
            
            # Map roles to Claude format
            if role == 'user':
                formatted_messages.append({
                    'role': 'user',
                    'content': content
                })
            elif role == 'assistant':
                formatted_messages.append({
                    'role': 'assistant',
                    'content': content
                })
            elif role == 'system':
                formatted_messages.append({
                    'role': 'system',
                    'content': content
                })
                
        return formatted_messages

    def get_completion(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        max_tokens: int = 4096,
        temperature: float = 0.7
    ) -> Optional[str]:
        """
        Get a chat completion from the Portkey API.

        Args:
            messages: List of message dictionaries with 'role' and 'content'
            model: The model to use (defaults to claude-3-sonnet)
            max_tokens: Maximum tokens in response
            temperature: Response temperature (0-1)

        Returns:
            The assistant's response text or None if there's an error
        """
        try:
            # Format messages for Claude
            formatted_messages = self._format_messages(messages)
            
            if not formatted_messages:
                logger.error("No valid messages to send")
                return None
            
            # Make API request
            response = self.client.chat.completions.create(
                messages=formatted_messages,
                model=model or self.default_model,
                max_tokens=max_tokens,
                temperature=temperature
            )
            
            # Extract and return response content
            if response and response.choices and response.choices[0].message:
                return response.choices[0].message.content
            
            logger.error("Received invalid response format")
            return None
            
        except Exception as e:
            logger.error(f"Error getting chat completion: {str(e)}")
            return None

    def test_connection(self) -> bool:
        """Test the connection with a simple message.
        
        Returns:
            bool: True if connection is successful
        """
        try:
            test_messages = [{
                'role': 'system',
                'content': self.default_system_prompt
            }, {
                'role': 'user',
                'content': 'Hello'
            }]
            
            response = self.get_completion(test_messages)
            return response is not None
            
        except Exception as e:
            logger.error(f"Connection test failed: {e}")
            return False
