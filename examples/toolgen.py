import openai
from coreagent import Agent, Config, set_default_config, Identity
from coreagent.tools import ToolGen

cli = openai.Client(
    base_url='http://192.168.1.5:9900/v1/',
    api_key='1',
)
set_default_config(Config(cli, "llm"))

s = Agent(Identity(show_generation=False, generation_limit=5000, temperature=0.0))
s.register_tool(ToolGen(s))

while True:
  t = input("In > ")
  if t == "q":
    break
  print("RESPONSE: \n" + s.chat(t))
