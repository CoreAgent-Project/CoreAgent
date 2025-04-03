from coreagent import Agent, set_default_config_from_args, get_default_config

# load deafult configurations from command-line arguments
set_default_config_from_args()

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

if get_default_config().use_guided_generation:
  print("Using xgrammar guided generation. ")

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
