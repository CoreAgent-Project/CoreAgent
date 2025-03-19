from pexpect.replwrap import python

## Define a tool for CoreAgent

### Simplest example: 
```python
class HelloTool:
  def get_hello_text(self, name: str):
    return f"Hello World, {name}! "
```

### Registering to the Agent: 
```python
from coreagent import Agent

class HelloTool:
  def get_hello_text(self, name: str):
    return f"Hello World, {name}! "

agent = Agent()
agent.register_tool(HelloTool()) # one-line
# maybe more tools?...
```

### With descriptions:
```python
class HelloTool:
  def get_hello_text(self, name: str) -> str:
    """
    # Get a hello text for a given name. 
    name: "The name you want to say hello to. "
    """
    return f"Hello World, {name}! "
```

### Returning a dictionary:

```python
import typing
from time import time

class HelloTool:
  def get_hello_text(self, name: str) -> typing.Dict[str, str]:
    """
    # Get a hello text for a given name. 
    name: "The name you want to say hello to. "
    """
    return {
      "name": name,
      "welcome_text": "Hello! ",
      "timestamp": int(time.time() / 1000),
      "text": f"Hello World, {name}! ",
    }
```
