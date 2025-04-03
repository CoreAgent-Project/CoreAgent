## Defining And Registering A Tool

CoreAgent makes it easy to integrate your own custom functionalities as tools. To register a tool, you simply need to:

1.  Define a Python class for your tool.
2.  Implement the methods you want to expose to the agent. Use docstrings to provide descriptions for your methods. These descriptions can be used by the agent to understand how to use the tool.
3.  Instantiate your tool class.
4.  Register the instance with the `ChatSession` using the `register_tool()` method.

Refer to the example above for a practical demonstration of tool registration.

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
