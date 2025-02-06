from utils.openrouter import gpt4o, claude35sonnet, gemini2flash

def synthesize(prompt, extra_synthesis_prompt="", verify=True):
    """
    Call multiple LLM models and synthesize their responses.
    
    Args:
        prompt (str): The input prompt to send to all models
        extra_synthesis_prompt (str): Additional prompt to send to the synthesis model
        verify (bool): Whether to run verification step on the synthesis
    Returns:
        dict: Aggregated results containing individual model responses and a synthesis
    """
    # Get responses from all models
    gpt4_response = gpt4o(prompt)
    claude_response = claude35sonnet(prompt)
    gemini_response = gemini2flash(prompt)
    
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
    synthesis_text = gemini2flash(synthesis_prompt)
    
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
        
        synthesis_text = gemini2flash(verification_prompt)
        
    # Return all results
    return {
        "individual_responses": {
            "gpt4": gpt4_response,
            "claude": claude_response,
            "gemini": gemini_response
        },
        "synthesis": synthesis_text
    }
