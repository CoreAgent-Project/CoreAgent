from argparse import ArgumentParser

import gradio as gr
from coreagent import Agent, Config, set_default_config_from_args, get_default_config
from coreagent.builtin import FileTool, CodeBase, MySQLTool


# We have extra arguments.
def register_extra_args(ap: ArgumentParser):
  ap.add_argument('--root-dir', '-d', default='.', type=str)
  ap.add_argument('--allow-write', '-w', default=False, action='store_true')
  ap.add_argument('--coder', default=False, action='store_true', help='Enable coding abilities. ')

args = set_default_config_from_args(argument_parser_handler=register_extra_args)

# update some required params since we might generate a lot!
default_config: Config = get_default_config()
default_config.generation_limit=50000

file_tool = FileTool(args.root_dir)

agent = Agent()
agent.register_tool(file_tool, exclude=['write_file', 'mkdir'] if not args.allow_write else None)
if args.coder:
  agent.register_tool(CodeBase(file_tool))

def chat_with_agent(message, history):
    """
    This function takes a user message and the chat history,
    sends the message to the agent, and returns the agent's response.
    """
    global agent
    if agent is None:
        return "Please configure and initialize the agent first."
    response = agent.chat(message)
    return response

if __name__ == "__main__":
    with gr.Blocks() as iface:
        chat_iface = gr.ChatInterface(
            fn=chat_with_agent,
            title="Chat with CoreAgent",
            description="Chat with an agent that can interact with files and (optionally) code.",
            examples=["List files in the root directory.", "Create a file named 'test.txt' with content 'Hello World' (if write access is allowed).", "Write a python function that adds two numbers (if coder is enabled)."],
            theme="soft",
        )
    iface.launch()
