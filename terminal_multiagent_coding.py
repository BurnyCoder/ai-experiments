import sys
import logging
from multiagent_coding.smolagents.multiagent_coding_smolagents import MultiAgentCoding

def main():
    """
    Simple terminal interface for interacting with the MultiAgentCoding system.
    Allows users to input coding requests and displays the generated code responses.
    """
    # Set up logging
    logging.basicConfig(
        level=logging.WARNING,  # Changed from INFO to WARNING to disable most logs
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger(__name__)
    logger.disabled = True  # Disable this logger

    logger.info("Initializing MultiAgentCoding system")
    coding = MultiAgentCoding()
    
    logger.info("Starting terminal interface")
    print("Welcome to the MultiAgent Coding!")
    print("Enter your coding requests, or type 'exit' to quit.")
    print("-" * 50)

    while True:
        try:
            # Get user input
            user_input = input("\nEnter your coding request: ").strip()
            
            # Check for exit command
            if user_input.lower() in ['exit', 'quit']:
                logger.info("User requested exit")
                print("\nThank you for using MultiAgent Coding. Goodbye!")
                sys.exit(0)
                
            # Skip empty inputs    
            if not user_input:
                logger.debug("Empty input received, continuing")
                continue
                
            logger.info("Processing user request: %s", user_input)
            print("\nThinking... Please wait...\n")
            
            # Process the request
            logger.debug("Calling run_terminal with user input")
            result = coding.run_terminal(user_input)
            
            # Display the result
            logger.info("Request processed successfully")
            print("-" * 50)
            print("Final AI response to user:")
            print("-" * 50)
            print(result)
            print("-" * 50)
            
        except KeyboardInterrupt:
            logger.warning("Operation cancelled by keyboard interrupt")
            print("\n\nOperation cancelled by user.")
            sys.exit(0)
            
        except Exception as e:
            logger.error("Error occurred while processing request", exc_info=True)
            print(f"\nAn error occurred: {str(e)}")
            print("Please try again.")

if __name__ == "__main__":
    main()
