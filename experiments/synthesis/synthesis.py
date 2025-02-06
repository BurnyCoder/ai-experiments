from utils.openrouter import gpt4o, claude35sonnet, gemini2flash


def synthesize(prompt):
    """
    Call multiple LLM models and synthesize their responses.
    
    Args:
        prompt (str): The input prompt to send to all models
        
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
    
    # Get a synthesis using Gemini 2 Flash
    synthesis = gemini2flash(synthesis_prompt)
    synthesis_text = synthesis
    
    # Return all results
    return {
        "individual_responses": {
            "gpt4": gpt4_response,
            "claude": claude_response,
            "gemini": gemini_response
        },
        "synthesis": synthesis_text
    }
