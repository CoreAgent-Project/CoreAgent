# CoreAgent: Simplest Agent Framework

CoreAgent is a lightweight and intuitive framework designed to make building intelligent agents straightforward. Focusing on simplicity, CoreAgent allows you to quickly integrate language models with custom tools to create powerful and versatile applications. 

Brought to you by Shanghai Glacies Technologies Co,. LTD. 

## Key Features

* **Simplicity First:** CoreAgent's key design emphasizes ease of use and minimal boilerplate.
* **Tool Registration:** Easily extend your agent's capabilities by registering custom tools.
* **Chat-Based Interaction:** Built around a conversational interface, making agent interaction natural and intuitive.
* **Extensible:** Designed to be easily adaptable and expandable to fit your specific needs.
* **Multi-Agent**: Share tool states across multiple agents.  
* **Coding**: Your agents can read/write to files easily. 

## Installation

To install CoreAgent, simply use pip:

```bash
pip install coreagent
````

## Getting Started

Here's a basic example demonstrating how to use CoreAgent:

```python
import os
from coreagent import Agent


class FileTool:
  def __init__(self):
    self.cwd = '.'

  def cwd(self):
    return self.cwd

  def cd(self, loc: str):
    """
    # Change working directory.
    """
    self.cwd = os.path.normpath(os.path.join(self.cwd, loc))
    return "Changed to: " + self.cwd

  def list(self):
    """
    # List all files.
    """
    return os.listdir(self.cwd)


s = Agent()
s.register_tool(FileTool())

s.chat('What files do i have? ')
```

In this example, we define a simple `FileTool` with functionalities to check the current working directory, change the directory, and list files. We then register this tool with a `ChatSession` instance. The `while` loop allows for interactive communication with the agent, where user input is passed to the `s.chat()` method.

## Registering Tools

CoreAgent makes it easy to integrate your own custom functionalities as tools. To register a tool, you simply need to:

1.  Define a Python class for your tool.
2.  Implement the methods you want to expose to the agent. Use docstrings to provide descriptions for your methods. These descriptions can be used by the agent to understand how to use the tool.
3.  Instantiate your tool class.
4.  Register the instance with the `ChatSession` using the `register_tool()` method.

Refer to the example above for a practical demonstration of tool registration.

## Contributing

Contributions to CoreAgent are welcome! If you have ideas for improvements, bug fixes, or new features, please feel free to open an issue or submit a pull request.

## License
GNU Lesser General Public License v3.0
https://www.gnu.org/licenses/lgpl-3.0.en.html
