import os
from dataclasses import dataclass
from portkey_ai import Portkey
from typing import Dict, List, Optional

from smolagents.models import Model, ChatMessage, Tool, parse_tool_args_if_needed


class PortkeyModel(Model):
    """This model connects to Portkey.ai as a gateway to multiple LLM providers.

    Parameters:
        model_id (`str`):
            The model identifier to use (e.g. "claude-3-5-sonnet-latest", "gpt-4o", "gemini-2.0-pro-exp-02-05").
        api_key (`str`, *optional*):
            The Portkey API key. If not provided, will try to read from PORTKEY_API_KEY env var.
        virtual_key (`str`, *optional*): 
            The Portkey virtual key for the specific provider. If not provided, will try to read from env var.
        **kwargs:
            Additional keyword arguments to pass to the Portkey API.
    """

    def __init__(
        self,
        model_id: str,
        api_key: Optional[str] = None,
        virtual_key: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.model_id = model_id

        if api_key is None:
            api_key = os.getenv("PORTKEY_API_KEY")
        if virtual_key is None:
            # Try to get virtual key from env based on model
            if "claude" in model_id.lower():
                virtual_key = os.getenv("PORTKEY_VIRTUAL_KEY_ANTHROPIC")
            elif "gpt" in model_id.lower():
                virtual_key = os.getenv("PORTKEY_VIRTUAL_KEY_OPENAI") 
            elif "gemini" in model_id.lower():
                virtual_key = os.getenv("PORTKEY_VIRTUAL_KEY_GOOGLE")

        self.client = Portkey(
            api_key=api_key,
            virtual_key=virtual_key
        )

    def __call__(
        self,
        messages: List[Dict[str, str]],
        stop_sequences: Optional[List[str]] = None,
        grammar: Optional[str] = None,
        tools_to_call_from: Optional[List[Tool]] = None,
        **kwargs,
    ) -> ChatMessage:
        completion_kwargs = self._prepare_completion_kwargs(
            messages=messages,
            stop_sequences=stop_sequences,
            grammar=grammar,
            tools_to_call_from=tools_to_call_from,
            model=self.model_id,
            **kwargs,
        )

        response = self.client.chat.completions.create(**completion_kwargs)

        self.last_input_token_count = response.usage.prompt_tokens if response.usage.prompt_tokens is not None else 0
        self.last_output_token_count = response.usage.completion_tokens if response.usage.completion_tokens is not None else 0

        message = ChatMessage.from_dict(
            response.choices[0].message.model_dump(include={"role", "content", "tool_calls"})
        )
        message.raw = response

        if tools_to_call_from is not None:
            return parse_tool_args_if_needed(message)
        return message
