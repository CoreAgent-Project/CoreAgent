from argparse import ArgumentParser

import openai
from coreagent import Agent, Config, set_default_config_from_args, get_default_config
from coreagent.builtin import FileTool

# We have extra arguments.
def register_extra_args(ap: ArgumentParser):
  ap.add_argument('--root-dir', '-d', default='.', type=str)
  ap.add_argument('--allow-write', '-w', default=False, type=bool)

# load deafult configurations from command-line arguments
args = set_default_config_from_args(argument_parser_handler=register_extra_args)

# update some required params since we might generate a lot!
default_config: Config = get_default_config()
default_config.generation_limit=5000

s = Agent()
s.register_tool(FileTool(args.root_dir), exclude=['write_file', 'mkdir'] if not args.allow_write else None)

while True:
  t = input("In > ")
  if t == "q":
    break
  print("RESPONSE: \n" + s.chat(t))
