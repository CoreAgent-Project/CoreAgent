import openai
from coreagent import Agent, set_default_config_from_args

# load deafult configurations from command-line arguments
set_default_config_from_args()

class VFSTool:
  def __init__(self):
    self.files = {}
  def ls(self):
    return {'files': self.files}
  def write(self, file: str, content: str):
    self.files[file] = content
  def read(self, file: str):
    return self.files[file]

s = Agent()
s.register_tool(VFSTool(), 'fs')

while True:
  t = input("In > ")
  if t == "q":
    break
  print("AGENT: ", s.chat(t))
