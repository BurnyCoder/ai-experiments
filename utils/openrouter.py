import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

def get_openrouter_completion(prompt, model="openai/gpt-4o"):
    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
        },
        json={
            "model": model,
            "messages": [
                {
                    "role": "user",
                    "cont ent": prompt
                }
            ]
        }
    )
    result = response.json().get("choices", [{}])[0].get("message", {}).get("content", "") if response.json().get("choices") else response.json()
    print("Model: ", model, "Response: ", result)
    return result

def gpt4o(prompt):
    """Wrapper function for GPT-4o"""
    #return get_openrouter_completion(prompt, model="openai/gpt-4o-2024-11-20")
    return get_openrouter_completion(prompt, model="openai/gpt-4o")

def claude35sonnet(prompt):
    """Wrapper function for Claude 3.5 Sonnet"""
    return get_openrouter_completion(prompt, model="anthropic/claude-3.5-sonnet")

def gemini2flash(prompt):
    """Wrapper function for Gemini 2 Flash"""
    return get_openrouter_completion(prompt, model="google/gemini-2.0-flash")

def gemini2pro(prompt):
    """Wrapper function for Gemini 2 Pro"""
    return get_openrouter_completion(prompt, model="google/gemini-2.0-pro")

def test():
    # Test GPT-4o
    gpt4o_response = gpt4o("What is the meaning of life?")
    print("GPT-4o response:", gpt4o_response)
    
    # Test Claude 3.5 Sonnet
    claude_response = claude35sonnet("What is the meaning of life?")
    print("Claude 3.5 Sonnet response:", claude_response)
    
    # Test Gemini 2 Flash
    gemini_response = gemini2flash("What is the meaning of life?")
    print("Gemini 2 Flash response:", gemini_response)
