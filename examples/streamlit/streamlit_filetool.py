from argparse import ArgumentParser

from coreagent import Agent, Config, set_default_config_from_args, get_default_config
from coreagent.builtin import FileTool, CodeBase, MySQLTool

import streamlit as st

# We have extra arguments.
def register_extra_args(ap: ArgumentParser):
  ap.add_argument('--root-dir', '-d', default='.', type=str)
  ap.add_argument('--allow-write', '-w', default=False, action='store_true')
  ap.add_argument('--coder', default=False, action='store_true', help='Enable coding abilities. ')

args = set_default_config_from_args(argument_parser_handler=register_extra_args)

# update some required params since we might generate a lot!
default_config: Config = get_default_config()
default_config.generation_limit=10000

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

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
  st.chat_message(msg['role']).markdown(msg['content'])

def tool_callback(tool_name: str):
  _m = st.chat_message('tool')
  text = "```\nCalling tool: %s\n```" % tool_name
  _m.markdown(text)
  st.session_state.messages.append({"role": "tool", "content": text})

def summary_callback(summary: str):
  _m = st.chat_message('summary')
  text = "```\nSummary: %s\n```" % summary
  _m.markdown(text)
  st.session_state.messages.append({"role": "summary", "content": text})

if message := st.chat_input("Chat Input"):
  m = st.chat_message("user")
  m.markdown(message)
  st.session_state.messages.append({"role": "user", "content": message})
  response_text = agent.chat(message, tool_callback=tool_callback, summary_callback=summary_callback)
  m = st.chat_message("assistant")
  m.write(response_text)
  st.session_state.messages.append({"role": "assistant", "content": response_text})

