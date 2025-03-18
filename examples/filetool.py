import openai
from coreagent import Agent, Config, set_default_config, Identity
from coreagent.tools import FileTool

cli = openai.Client(
    base_url='http://192.168.1.5:9900/v1/',
    api_key='1',
)
set_default_config(Config(cli, "llm"))

import argparse
ap = argparse.ArgumentParser()
ap.add_argument('--root-dir', '-d', default='.', type=str)
ap.add_argument('--allow-write', '-w', default=False, type=bool)
args = ap.parse_args()

s = Agent(Identity(show_generation=True, generation_limit=50000, temperature=0.3))
s.register_tool(FileTool(args.root_dir), exclude=['write_file'] if not args.allow_write else None)

while True:
  t = input("In > ")
  if t == "q":
    break
  print("RESPONSE: \n" + s.chat(t))
