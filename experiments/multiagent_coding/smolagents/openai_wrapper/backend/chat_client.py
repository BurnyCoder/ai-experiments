from openai import OpenAI
from typing import List, Dict, Optional


class ChatClient:
    """A wrapper class for OpenAI chat completions."""

    def __init__(self, api_key: str):
        """Initialize the chat client with OpenAI API key."""
        self.client = OpenAI(api_key=api_key)

    def get_completion(
        self,
        messages: List[Dict[str, str]],
        model: str = "gpt-4",
        temperature: float = 0.7,
    ) -> Optional[str]:
        """
        Get a chat completion from the OpenAI API.

        Args:
            messages: List of message dictionaries with 'role' and 'content'
            model: The OpenAI model to use
            temperature: Sampling temperature (0.0 to 1.0)

        Returns:
            The assistant's response text or None if there's an error
        """
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error getting chat completion: {str(e)}")
            return None 