from multiagent_coding.smolagents.multiagent_coding_smolagents import MultiAgentCoding

def main():
    """
    Launch the MultiAgent Coding system with Gradio UI interface.
    """
    coding = MultiAgentCoding()
    coding.launch_with_ui()

if __name__ == "__main__":
    main()
