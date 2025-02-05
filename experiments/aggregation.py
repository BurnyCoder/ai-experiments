from utils.openrouter import gpt4o, claude35sonnet, gemini2flash


def aggregate(prompt):
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
    
    # Get a synthesis using Claude 3.5 Sonnet
    synthesis = claude35sonnet(synthesis_prompt)
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


def test():
    test_prompt = "What are the three most important considerations when designing a new programming language?"
    results = aggregate(test_prompt)
    
    print("\nIndividual Responses:")
    for model, response in results["individual_responses"].items():
        print(f"\n{model.upper()}:")
        print(response)
        
    print("\nSynthesized Response:")
    print(results["synthesis"])
