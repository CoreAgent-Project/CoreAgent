## Built-In Tools

### FileTool
FileTool is a tool that can be used to read and write files.
```python
from coreagent import Agent
from coreagent.builtin import FileTool
s = Agent()
s.register_tool(FileTool('/tmp')) # specify a root dir
s.chat("write a HTML-based game at /") # / maps to /tmp in this case
```

### arxiv Tool
It allows your agent to search papers on arxiv.org. 
```python
from coreagent import Agent
from coreagent.builtin import ArxivTool
s = Agent()
s.register_tool(ArxivTool())
s.chat("find me papers about machine learning")
```

### ToolGen
This allows your agent to generate tools for itself.

Upon installation, you must type `YES` in terminal to allow code execution. 

Optional: Install seleniumbase via `pip install seleniumbase` to allow browser use. 
```python
from coreagent import Agent
from coreagent.builtin import ToolGen
s = Agent()
s.register_tool(ToolGen(s)) # pass in the agent instance
s.chat("make yourself a tool to search papers, documentation: https://info.arxiv.org/help/api/index.html")
```

### TODO: more to be added soon... 
