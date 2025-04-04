<p align="center">
  <picture>
    <img alt="CoreAgent" src="https://raw.githubusercontent.com/CoreAgent-Project/CoreAgent/main/assets/coreagent.png" width=30%>
  </picture>
</p>

<h3 align="center">
简单易用的智能体框架，支持有状态的工具调用
</h3>

<p align="center">
<a href="https://github.com/CoreAgent-Project/CoreAgent/blob/main/README.md">English Version</a>
</p>
<p align="center">
| <a href="https://github.com/CoreAgent-Project/CoreAgent/blob/main/docs/Documentation.md"><b>文档</b></a> | <a href="https://discord.gg/Hytrg9UXgU"><b>Discord</b></a> |
</p>

----

CoreAgent 是一个轻量级且直观的框架，旨在使构建智能体变得简单直接。CoreAgent 专注于简洁性，让您能够快速地将语言模型与自定义工具集成，从而创建强大且通用的应用程序。

## 状态化工具
隆重介绍 **Stateful Tools**, 使得同一个工具的状态在多个智能体间共享状态。
```python
from coreagent import Agent

class MyStatefulTool:
  def __init__(self):
    self.state = 0
  def add_state(self, n: int):
    self.state += n
  def get_state(self):
    return self.state

# single shared tool! 
shared_tool = MyStatefulTool()

agent_1 = Agent.with_tools(shared_tool)
agent_2 = Agent.with_tools(shared_tool)
agent_1.chat("增加10个状态值")
agent_2.chat("现在状态值是多少？")
```

## 安装

要安装 CoreAgent，只需使用 pip：

```bash
pip install coreagent
```

## 快速入门

试试简单的 `guard_and_theif.py` 样例: 
```shell
python ./examples/guard_and_theif.py \
  -u "https://api.openai.com/v1/" \
  -m "gpt-3.5-turbo" \
  -k "...API KEY..." \
  --verbose
```

使用 **DeepSeek** 官方接口: 
```shell
python examples/toolgen.py \
  -u "https://api.deepseek.com" \
  -k "sk-..." \
  -m deepseek-reasoner \
  --verbose
```

以下是一个基本示例，演示了如何使用 **CoreAgent**：

```python
from coreagent import Agent, set_default_config_from_args
import urllib.request
import json

# 读取公用参数 (--api-base-url/-u, --api-key/-k, --model/-m, --verbose/-v, --guided/-g)
set_default_config_from_args()

class IPTool:
  def get_my_ip(self) -> str:
    j = json.loads(urllib.request.urlopen("https://api.ipify.org/?format=json").read().decode())
    return j['ip']

s = Agent()
s.register_tool(IPTool())

s.chat("我的IP地址是多少？")
```

## Roadmap
- [x] 基础框架。 
- [x] 使 `guided_grammar` 成为可选依赖，支持常用LLM API (DeepSeek API, GPT3.5/4/4o API, Qwen API, etc. )
- [x] 更简单的样例代码。
- [ ] 基于RAG的记忆系统。
- [ ] 整合MCP客户端。

## 贡献

欢迎为 CoreAgent 做出贡献！如果您有改进、错误修复或新功能的想法，请随时提交 Issue 或 Pull Request。

## 许可证
上海格拉切斯工程科技有限公司 倾力呈现。<br />
GNU Lesser General Public License v3.0
https://www.gnu.org/licenses/lgpl-3.0.en.html

## 星星历史

[![Star History Chart](https://api.star-history.com/svg?repos=CoreAgent-Project/CoreAgent&type=Date)](https://www.star-history.com/#CoreAgent-Project/CoreAgent&Date)