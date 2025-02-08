import os
from dotenv import load_dotenv
from portkey_ai import Portkey
from typing import List, Dict, Optional


class PortkeyClient:
    """A wrapper class for Portkey chat completions."""

    def __init__(self):
        """Initialize the Portkey client with API keys from environment."""
        load_dotenv()
        self.client = Portkey(
            api_key=os.getenv("PORTKEY_API_KEY"),
            virtual_key=os.getenv("PORTKEY_VIRTUAL_KEY_ANTHROPIC")
        )

    def get_completion(
        self,
        messages: List[Dict[str, str]],
        model: str = "claude-3-5-sonnet-latest",
        max_tokens: int = 8192,
    ) -> Optional[str]:
        """
        Get a chat completion from the Portkey API.

        Args:
            messages: List of message dictionaries with 'role' and 'content'
            model: The model to use
            max_tokens: Maximum tokens in response

        Returns:
            The assistant's response text or None if there's an error
        """
        try:
            response = self.client.chat.completions.create(
                messages=messages,
                model=model,
                max_tokens=max_tokens,
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error getting chat completion: {str(e)}")
            return None
