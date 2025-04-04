import gradio as gr
from coreagent import Agent, Identity, set_default_config_from_args
from coreagent.builtin import ToolGen
import openai

# Load default configurations from command-line arguments
set_default_config_from_args()

# Initialize the agent
s = Agent()

# Register the ToolGen tool
s.register_tool(ToolGen(s))

def chat_with_agent(message, history):
    """
    This function takes a user message and the chat history,
    sends the message to the agent, and returns the agent's response.
    """
    response = s.chat(message)
    return response

if __name__ == "__main__":
    # Create the Gradio interface
    iface = gr.ChatInterface(
        fn=chat_with_agent,
        type="messages",
        title="CoreAgent with Tool Generation",
        description="Chat with an agent that can generate and use tools on the fly.",
        examples=["Generate a tool that adds two numbers.", "What is the result of 5 + 3 using the tool?"],
        theme="soft",
    )

    # Launch the Gradio app
    iface.launch()
