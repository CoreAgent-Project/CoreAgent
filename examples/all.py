from argparse import ArgumentParser

from coreagent import Agent, Config, set_default_config_from_args, get_default_config
from coreagent.builtin import FileTool, CodeBase, ToolGen, AskingShellExecutorTool, SeleniumBrowser, ArxivTool

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
agent.register_tool(ToolGen(agent))
agent.register_tool(AskingShellExecutorTool())
agent.register_tool(SeleniumBrowser(agent.config.llm, agent.config.model))

if args.coder:
  agent.register_tool(CodeBase(file_tool))

while True:
  t = input("In > ")
  if t == "q":
    break
  print("RESPONSE: \n" + agent.chat(t))
