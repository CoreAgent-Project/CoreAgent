import openai
from coreagent import Agent, Config, set_default_config

class VFSTool:
  def __init__(self):
    self.files = {}
  def ls(self):
    return {'files': self.files}
  def write(self, file: str, content: str):
    self.files[file] = content
  def read(self, file: str):
    return self.files[file]

cli = openai.Client(
    base_url='http://192.168.1.5:9900/v1/',
    api_key='1',
)
set_default_config(Config(cli, "llm"))

s = Agent()
s.register_tool(VFSTool(), 'fs')

while True:
  t = input("In > ")
  if t == "q":
    break
  print("AGENT: ", s.chat(t))
