import os
import asyncio
from experiments.synthesis.synthesis import SynthesisModel

async def test_logic(prompt, extra_synthesis_prompt=""):
    synthesis_model = SynthesisModel()
    results = await synthesis_model.chat([{"role": "user", "content": prompt}], extra_synthesis_prompt)
    
    # Create base test directory if it doesn't exist
    base_dir = 'experiments/synthesis/tests'
    os.makedirs(base_dir, exist_ok=True)
    
    # Find next available numbered directory
    i = 1
    while True:
        test_dir = f'{base_dir}/test_{i}'
        if not os.path.exists(test_dir):
            os.makedirs(test_dir)
            break
        i += 1
    
    # Save individual responses to separate files
    for model, response in results["raw_responses"].items():
        filename = f"{test_dir}/{model}_response.txt"
        with open(filename, 'w') as f:
            f.write(f"Response from {model.upper()} about {prompt}:\n\n")
            f.write(response)
        print(f"Saved {model}'s response to {filename}")
    
    # Save synthesis to separate file
    synthesis_file = f"{test_dir}/synthesis.txt"
    with open(synthesis_file, 'w') as f:
        f.write("Synthesized response about AI fields:\n\n")
        f.write(results["choices"][0]["message"]["content"])
    print(f"Saved synthesis to {synthesis_file}")

async def test():
    await test_logic("What are the main fields and subfields of artificial intelligence? List and briefly describe the key areas. Make sure to include all subfields.", extra_synthesis_prompt="When synthetizing, try to include all the subfields that all the models mentioned.")
    #await test_logic("Code a snake game in python")
