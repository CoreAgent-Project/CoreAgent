<p align="center">
  <picture>
    <img alt="CoreAgent" src="https://raw.githubusercontent.com/CoreAgent-Project/CoreAgent/main/assets/coreagent.png" width=30%>
  </picture>
</p>

<h3 align="center">
Simplest Agent Framework
</h3>

<p align="center">
| <a href="https://github.com/CoreAgent-Project/CoreAgent/blob/main/docs/Documentation.md"><b>Documentation</b></a> | <a href="https://discord.gg/Hytrg9UXgU"><b>Discord</b></a> |
</p>

----

CoreAgent is a lightweight and intuitive framework designed to make building intelligent agents straightforward. Focusing on simplicity, CoreAgent allows you to quickly integrate language models with custom tools to create powerful and versatile applications. 

## Key Features

* **Universal:** Both coding, chatting, one `Agent` class handles them all! 
* **Simplicity First:** Ease of use and minimal boilerplate.
* **Sharable Tool States**: Share the same tool instances states across multiple agents. 
* **Built-in Tools**: Lots of built-in tools to get you started fast! 

## Installation

To install CoreAgent, simply use pip:

```bash
pip install coreagent
````

## Getting Started

Try out simple `guard_and_theif.py` example: 
```shell
python ./examples/guard_and_theif.py \
  -u "https://api.openai.com/v1/" \
  -m "gpt-3.5-turbo" \
  -k "...API KEY..." \
  --verbose
```

Or, you may try to write a basic example demonstrating how to use CoreAgent:

```python
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
```

## Roadmap
- [x] Basic universal agent framework. 
- [x] Make `guided_grammar` optional, allow general LLM usage (DeepSeek API, GPT3.5/4/4o API, Qwen API, etc. )
- [ ] More intuitive simplified examples, alowing hands-on try-outs. 
- [ ] RAG-based memory module. 

## Contributing

Contributions to CoreAgent are welcome! If you have ideas for improvements, bug fixes, or new features, please feel free to open an issue or submit a pull request.

## License
Brought to you by Shanghai Glacies Technologies Co,. LTD. <br />
GNU Lesser General Public License v3.0
https://www.gnu.org/licenses/lgpl-3.0.en.html

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=CoreAgent-Project/CoreAgent&type=Date)](https://www.star-history.com/#CoreAgent-Project/CoreAgent&Date)
