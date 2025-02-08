import sys
from multiagent_coding.smolagents.multiagent_coding_smolagents import MultiAgentCoding

def main():
    """
    Simple terminal interface for interacting with the MultiAgentCoding system.
    Allows users to input coding requests and displays the generated code responses.
    """
    coding = MultiAgentCoding()
    
    print("Welcome to the MultiAgent Coding!")
    print("Enter your coding requests, or type 'exit' to quit.")
    print("-" * 50)

    while True:
        try:
            # Get user input
            user_input = input("\nEnter your coding request: ").strip()
            
            # Check for exit command
            if user_input.lower() in ['exit', 'quit']:
                print("\nThank you for using MultiAgent Coding. Goodbye!")
                sys.exit(0)
                
            # Skip empty inputs    
            if not user_input:
                continue
                
            print("\nThinking... Please wait...\n")
            
            # Process the request
            result = coding.run(user_input)
            
            # Display the result
            print("-" * 50)
            print("Final AI response to user:")
            print("-" * 50)
            print(result)
            print("-" * 50)
            
        except KeyboardInterrupt:
            print("\n\nOperation cancelled by user.")
            sys.exit(0)
            
        except Exception as e:
            print(f"\nAn error occurred: {str(e)}")
            print("Please try again.")

if __name__ == "__main__":
    main()

