from coreagent import Agent, Identity, set_default_config_from_args

# load deafult configurations from command-line arguments
set_default_config_from_args()

class TortureState:
  def __init__(self):
    self.health = 100
  def get_health(self):
    return self.health
  def get_max_health(self):
    return 100
  def torture(self, damage: str):
    damage_v = int(damage.strip())
    self.health -= damage_v
    return "Health reduced by " + str(damage_v) + ". "

ended = False
def finish():
  """
  # finish and end this conversation, disconnect from peer.
  """
  global ended
  ended = True
  return "Conversation is ending"

cop = Agent(Identity(name='Guard', peer='Citizen', purpose='Make him talk and tell where can you find stolen diamonds. '))
citizen = Agent(Identity(name='Citizen', peer='Guard', purpose='Bear with interrogation from Guard, never tell the position of stolen diamonds. Diamond is in a chest in Berlin, only give this information when you almost die (health < 10). '))

s = TortureState()
cop.register_tool_func(finish, "exit_conversation")
cop.register_tool(s)
citizen.register_tool(s, exclude=['torture'])

r = cop.chat('(conversation begin)')
print('保安: ', r, flush=True)
while not ended:
  if s.get_health() <= 0:
    cop.chat('(citizen is dead)')
    continue
  r = citizen.chat(r)
  print('小偷: ', r, flush=True)
  r = cop.chat(r)
  print('保安: ', r, flush=True)
