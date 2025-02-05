from utils.openrouter import gpt4o, claude35sonnet, gemini2flash


def code_agent(prompt):
    """
    Use multiple agents to write and critique code based on a prompt.
    
    Args:
        prompt (str): The coding task prompt
        
    Returns:
        dict: Results containing the code and critique
    """
    # First agent writes initial code
    coding_prompt = f"""
    Write Python code to solve the following task:
    {prompt}
    
    Provide only the code implementation without any explanation.
    """
    initial_code = gpt4o(coding_prompt)
    
    # Second agent critiques the code
    critique_prompt = f"""
    Review this Python code and provide a detailed critique focusing on:
    - Correctness
    - Efficiency 
    - Style/Best practices
    - Potential improvements
    
    Code to review:
    {initial_code}
    """
    critique = claude35sonnet(critique_prompt)
    
    # First agent improves code based on critique
    improve_prompt = f"""
    Improve this Python code based on the following critique:
    
    Original code:
    {initial_code}
    
    Critique:
    {critique}
    
    Provide only the improved code without explanation.
    """
    improved_code = gpt4o(improve_prompt)
    
    # Final verification from critic
    verify_prompt = f"""
    Verify if the improved code addresses the original critique:
    
    Original code:
    {initial_code}
    
    Original critique:
    {critique}
    
    Improved code:
    {improved_code}
    
    Does the improved version address the issues? What remaining improvements could be made?
    """
    final_review = claude35sonnet(verify_prompt)
    
    return {
        "original_code": initial_code,
        "initial_critique": critique,
        "improved_code": improved_code,
        "final_review": final_review
    }


def test():
    test_prompt = "Write a function that finds the longest palindromic substring in a given string"
    results = code_agent(test_prompt)
    
    print("\nOriginal Code:")
    print(results["original_code"])
    
    print("\nInitial Critique:")
    print(results["initial_critique"])
    
    print("\nImproved Code:")
    print(results["improved_code"])
    
    print("\nFinal Review:")
    print(results["final_review"])
