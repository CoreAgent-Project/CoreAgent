# CoreAgent：无比简单的 Agent 框架

CoreAgent 是一个轻量级且直观的框架，旨在使构建智能 Agent 变得简单直接。CoreAgent 专注于简洁性，让您能够快速地将语言模型与自定义工具集成，从而创建强大且通用的应用程序。

上海格拉切斯工程科技有限公司 倾力呈现。

## 主要特性

* **简洁至上：** CoreAgent 的关键设计强调易用性和最少的样板代码。
* **工具注册：** 通过注册自定义工具轻松扩展您的 Agent 的功能。
* **基于聊天的交互：** 基于对话式界面构建，使 Agent 交互自然直观。
* **可扩展：** 设计易于适配和扩展，以满足您的特定需求。
* **多Agent写作**: 多个Agent可以共享工具状态，共同协作。 
* **代码编写**: 轻松读写文件。 

## 安装

要安装 CoreAgent，只需使用 pip：

```bash
pip install coreagent
```

## 快速入门

以下是一个基本示例，演示了如何使用 CoreAgent：

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
    # 更改工作目录。
    """
    self.cwd = os.path.normpath(os.path.join(self.cwd, loc))
    return "Changed to: " + self.cwd

  def list(self):
    """
    # 列出所有文件。
    """
    return os.listdir(self.cwd)


s = Agent()
s.register_tool(FileTool())

s.chat('What files do i have? ')
```

在此示例中，我们定义了一个简单的 `FileTool`，它具有检查当前工作目录、更改目录和列出文件的功能。然后，我们将此工具注册到 `ChatSession` 实例中。`while` 循环允许与 Agent 进行交互式通信，用户的输入将传递给 `s.chat()` 方法。

## 注册工具

CoreAgent 可以轻松地将您自己的自定义功能集成为工具。要注册工具，您只需：

1.  为您的工具定义一个 Python 类。
2.  实现您想要暴露给 Agent 的方法。使用文档字符串为您的方法提供描述。这些描述可供 Agent 理解如何使用该工具。
3.  实例化您的工具类。
4.  使用 `register_tool()` 方法将实例注册到 `ChatSession`。

请参阅上面的示例，以获取工具注册的实际演示。

## 贡献

欢迎为 CoreAgent 做出贡献！如果您有改进、错误修复或新功能的想法，请随时提交 Issue 或 Pull Request。

## 许可证
GNU Lesser General Public License v3.0
https://www.gnu.org/licenses/lgpl-3.0.en.html
