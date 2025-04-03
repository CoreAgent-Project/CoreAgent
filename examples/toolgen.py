import openai
from coreagent import Agent, Identity, set_default_config_from_args
from coreagent.builtin import ToolGen

# load deafult configurations from command-line arguments
set_default_config_from_args()



s = Agent()
s.register_tool(ToolGen(s))

while True:
  t = input("In > ")
  if t == "q":
    break
  print("RESPONSE: \n" + s.chat(t))
