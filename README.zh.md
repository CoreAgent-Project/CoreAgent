<p align="center">
  <picture>
    <img alt="CoreAgent" src="https://raw.githubusercontent.com/CoreAgent-Project/CoreAgent/main/assets/coreagent.png" width=30%>
  </picture>
</p>

<h3 align="center">
简单易用的智能体框架
</h3>

<p align="center">
| <a href="https://github.com/CoreAgent-Project/CoreAgent/blob/main/docs/Documentation.md"><b>文档</b></a> | <a href="https://discord.gg/Hytrg9UXgU"><b>Discord</b></a> |
</p>

----

CoreAgent 是一个轻量级且直观的框架，旨在使构建智能体变得简单直接。CoreAgent 专注于简洁性，让您能够快速地将语言模型与自定义工具集成，从而创建强大且通用的应用程序。

## 主要特性

* **Simplicity First**: 易于使用，最少样板代码。
* **Multi-Agent**: 多个智能体之间共享相同的工具实例状态。
* **Built-in Tools**: 大量内置工具，助您快速入门！

## 安装

要安装 CoreAgent，只需使用 pip：

```bash
pip install coreagent
```

## 快速入门

以下是一个基本示例，演示了如何使用 CoreAgent：

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

s.chat("我的IP地址是多少？")
```

## 注册工具

CoreAgent 可以轻松地将您自己的自定义功能集成为工具。要注册工具，您只需：

1.  为您的工具定义一个 Python 类。
2.  实现您想要暴露给 Agent 的方法。使用文档字符串为您的方法提供描述。这些描述可供 Agent 理解如何使用该工具。
3.  实例化您的工具类。
4.  使用 `register_tool()` 方法将实例注册到 `ChatSession`。

请参阅上面的示例，以获取工具注册的实际演示。

## Roadmap
- [x] 基础框架。 
- [x] 移除 `guided_grammar` 强制需求，支持常用LLM API (DeepSeek API, GPT3.5/4/4o API, Qwen API, etc. )
- [ ] 更简单的样例代码。
- [ ] 基于RAG的记忆系统。

## 贡献

欢迎为 CoreAgent 做出贡献！如果您有改进、错误修复或新功能的想法，请随时提交 Issue 或 Pull Request。

## 许可证
上海格拉切斯工程科技有限公司 倾力呈现。<br />
GNU Lesser General Public License v3.0
https://www.gnu.org/licenses/lgpl-3.0.en.html

## 星星历史

[![Star History Chart](https://api.star-history.com/svg?repos=CoreAgent-Project/CoreAgent&type=Date)](https://www.star-history.com/#CoreAgent-Project/CoreAgent&Date)