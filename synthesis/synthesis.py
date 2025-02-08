from utils.openrouter import gpt4o, claude35sonnet, gemini2flash
import asyncio

class SynthesisModel:
    def __init__(self):
        """
        Initialize the synthesis model.
        """
        pass

    async def chat(self, messages, extra_synthesis_prompt="", verify=True):
        """
        OpenAI-style chat interface that processes a list of messages.
        
        Args:
            messages (list): List of message dictionaries with 'role' and 'content'
            extra_synthesis_prompt (str): Additional prompt to send to the synthesis model
            verify (bool): Whether to run verification step on the synthesis
        Returns:
            dict: Response in OpenAI format
        """
        # Extract the last user message as the prompt
        prompt = messages[-1]['content'] if messages else ""
        
        result = await self._synthesize(prompt, extra_synthesis_prompt, verify)
        
        return {
            'choices': [{
                'message': {
                    'role': 'assistant',
                    'content': result['synthesis']
                },
                'finish_reason': 'stop'
            }],
            'model': 'synthesis-model',
            'usage': {
                'prompt_tokens': None,
                'completion_tokens': None,
                'total_tokens': None
            },
            'raw_responses': result['individual_responses']
        }

    async def _synthesize(self, prompt, extra_synthesis_prompt, verify):
        """
        Internal method to call multiple LLM models and synthesize their responses.
        """
        # Get responses from all models concurrently
        responses = await asyncio.gather(
            self._get_response(gpt4o, prompt),
            self._get_response(claude35sonnet, prompt),
            self._get_response(gemini2flash, prompt)
        )
        
        gpt4_response, claude_response, gemini_response = responses
        
        # Create a synthesis prompt using the collected responses
        synthesis_prompt = f"""
        I have received multiple AI responses to the prompt: "{prompt}"
        
        GPT-4's response: {gpt4_response}
        Claude's response: {claude_response}
        Gemini's response: {gemini_response}
        
        Please synthesize these responses into a comprehensive answer that captures the key insights from all models.
        """
        
        if extra_synthesis_prompt:
            synthesis_prompt += f"\n\n{extra_synthesis_prompt}"
        
        # Get initial synthesis using Gemini 2 Flash
        synthesis_text = await self._get_response(gemini2flash, synthesis_prompt)
        
        if verify:
            # Verification prompt focused on completeness and accuracy
            verification_prompt = f"""
            You are a critical reviewer. Your task is to verify if the synthesis below properly combines insights from all model responses and follows the given instructions.

            Original prompt: "{prompt} {extra_synthesis_prompt}"

            Original responses:
            GPT-4: {gpt4_response}
            Claude: {claude_response}
            Gemini: {gemini_response}

            Current synthesis:
            {synthesis_text}

            Please analyze:
            1. Are all key insights from each model included?
            2. Is anything important missing or misrepresented?
            3. Does it fully address the original prompt and additional instructions?

            If any issues are found, provide a revised synthesis that addresses them.
            If no issues are found, respond with the original synthesis.
            Only respond with the synthesis text, no other text.
            """
            
            synthesis_text = await self._get_response(gemini2flash, verification_prompt)
            
        # Return all results
        return {
            "individual_responses": {
                "gpt4": gpt4_response,
                "claude": claude_response,
                "gemini": gemini_response
            },
            "synthesis": synthesis_text
        }

    async def _get_response(self, model_func, prompt):
        """
        Helper method to handle async model calls.
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, model_func, prompt)


