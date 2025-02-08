import sys
from synthesis.synthesis import SynthesisModel
import asyncio

def main():
    """
    Simple terminal interface for interacting with the Synthesis system.
    Allows users to input prompts and displays synthesized responses from multiple LLMs.
    """
    synthesis = SynthesisModel()
    
    print("Welcome to the Multi-LLM Synthesis System!")
    print("Enter your prompts, or type 'exit' to quit.")
    print("-" * 50)

    async def process_input(user_input):
        messages = [{"role": "user", "content": user_input}]
        result = await synthesis.chat(messages)
        return result

    while True:
        try:
            # Get user input
            user_input = input("\nEnter your prompt: ").strip()
            
            # Check for exit command
            if user_input.lower() in ['exit', 'quit']:
                print("\nThank you for using the Synthesis System. Goodbye!")
                sys.exit(0)
                
            # Skip empty inputs    
            if not user_input:
                continue
                
            print("\nSynthesizing responses... Please wait...\n")
            
            # Process the request
            result = asyncio.run(process_input(user_input))
            
            # Display individual model responses
            print("\nIndividual Model Responses:")
            for model, response in result['raw_responses'].items():
                print("-" * 50)
                print(f"{model.upper()}:")
                print(response)

            # Display the synthesized result
            print("-" * 50)
            print("Synthesized Response:")
            print("-" * 50)
            print(result['choices'][0]['message']['content'])
            print("-" * 50)
            
           
        except KeyboardInterrupt:
            print("\n\nOperation cancelled by user.")
            sys.exit(0)
            
        except Exception as e:
            print(f"\nAn error occurred: {str(e)}")
            print("Please try again.")

if __name__ == "__main__":
    main()
