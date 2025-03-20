# CoreAgent: Simplest Agent Framework

CoreAgent is a lightweight and intuitive framework designed to make building intelligent agents straightforward. Focusing on simplicity, CoreAgent allows you to quickly integrate language models with custom tools to create powerful and versatile applications. 

Brought to you by Shanghai Glacies Technologies Co,. LTD. 

## Key Features

* **Simplicity First:** Ease of use and minimal boilerplate.
* **Multi-Agent**: Share the same tool instances states across multiple agents.
* **Built-in Tools**: Lots of built-in tools to get you started fast! 

## Installation

To install CoreAgent, simply use pip:

```bash
pip install coreagent
````

## Getting Started

Here's a basic example demonstrating how to use CoreAgent:

```python
from coreagent import Agent
import urllib.request
import json

class IPTool:
  def get_my_ip(self) -> str:
    j = json.loads(urllib.request.urlopen("https://api.ipify.org/?format=json").read().decode())
    return j['ip']

s = Agent()
s.register_tool(IPTool())

s.chat("What's my IP address? ")
```

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
