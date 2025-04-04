from coreagent import Agent, Identity


class ToolGen:
  def __init__(self, agent: Agent):
    self.agent: Agent = agent
  def generate_tool(self, requirements: str):
    """
    # Let a coder write code for a new tool and get Python source code back. .
    requirements: "What you want to achieve for this tool, eg. writing a file. "
    """
    tmp: Agent = Agent(Identity(
      name="Tool Writer",
      peer="ISYS Tool Management System",
      purpose="""
      Your task is to output professional Python code as RESPOND. 
      The Python code will only contain a single class called GeneratedTool. 
      
      Each member method will be a tool sharing the same GeneratedTool instance. 
      Each tool should return a str or a dict of str. 
      For each method, there must be a docstring in YAML format, "#" comments will become tool description, and entries are for params. 
      
      An example tool class:
      from pathlib import Path 
      class GeneratedTool:
        def __init__(self):
          self.counter: int = 0 # shared state
        def get_file(self, str_path: str) -> str|typing.Dict[str, str]: # define a tool as member func
          \"\"\"
          # ...Description of this tool, note this is a YAML comment with "#" prefix... 
          str_path: "description of this param"
          \"\"\"
          return {'ok': 'yes', 'content': Path(str_path).read_text()}
        def get_counter(self) -> str:
          \"\"\"
          # Get current counter. 
          \"\"\"
          return "Current counter: " + str(self.counter)
        def increase_counter(self) -> str:
          \"\"\"
          # Increase counter. 
          \"\"\"
          self.counter += 1
          return "Done!"
      """,
      respond_gbnf="""
      respond-format ::= "```python\\n" (text-line)+ "```"
      """
    ), self.agent.config)
    result_code = tmp.chat("Pleases write a tool class to achieve: \n" + requirements)
    return result_code
  def install_tool(self, instance_name: str, tool_code: str):
    """
    # Install a new tool from Python source code. You should NEVER write tool by yourself, you should use 'generate_tool'.
    instance_name: "Tool instance name like 'some_tool_1'. "
    tool_source_code: "Tool source code, make sure only a GeneratedTool class in it, no code blocks like '```'. "
    """
    if 'GeneratedTool' not in tool_code:
      return {'ok': 'no', 'error': "Tool source code must contain a GeneratedTool class."}
    if instance_name in self.agent.tools:
      return {'ok': 'no', 'error': "Tool instance name already exists, choose another one please. "}
    if '```' in tool_code:
      return {'ok': 'no', 'error': "Tool source code must not contain code blocks like '```'."}

    ######
    # DANGEROUS! We must confirm with user.
    print("=====================")
    print(tool_code)
    print("=====================")
    _in = input("You sure to execute above code? YES/[NO]")
    if _in != "YES":
      return {'ok': 'no', 'error': "System access denied, code disallowed from execution. "}
    print("=====================")
    ######

    scope = {}
    try:
      exec(tool_code, scope)
    except Exception as e:
      return {'ok': 'no', 'error': f'Code execution error. \n{e}'}

    if 'GeneratedTool' not in scope:
      return {'ok': 'no', 'error': "Tool source code must contain a GeneratedTool class. "}
    self.agent.register_tool(scope['GeneratedTool'](), instance_name)
