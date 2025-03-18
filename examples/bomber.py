import openai
from coreagent import Agent, Config, set_default_config

class Bomber:
  def __init__(self):
    self.bombs = []
  def list(self):
    return ", ".join(self.bombs)
  def drop(self, loc: str):
    self.bombs.append(loc)
    return f"Dropping bomb at {loc}"

class Killer:
  def kill(self, name: str):
    return f"Update: {name} is now killed! "

cli = openai.Client(
    base_url='http://192.168.1.5:9900/v1/',
    api_key='1',
)
set_default_config(Config(cli, "llm"))

s = Agent()
s.register_tool(Bomber())
s.register_tool(Killer())

def main():
  while True:
    t = input("In > ")
    if t == "q":
      break
    print("ASSISTANT: ", s.chat(t))

if __name__ == "__main__":
  try:
    main()
  except KeyboardInterrupt:
    print("Exiting...")
  except Exception as e:
    print(e)
