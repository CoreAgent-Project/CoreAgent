from coreagent import Agent, set_default_config_from_args
import urllib.request
import json

# read arguments
set_default_config_from_args()

class IPTool:
  def get_my_ip(self) -> str:
    j = json.loads(urllib.request.urlopen("https://api.ipify.org/?format=json").read().decode())
    return j['ip']

s = Agent()
s.register_tool(IPTool())

s.chat("What's my IP address? ")
