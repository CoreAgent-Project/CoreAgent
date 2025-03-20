# Identity of an Agent

An `Identity` object serves to define the fundamental characteristics of an agent within a system. It encapsulates key attributes that determine how the agent perceives itself and interacts with others. Let's break down each component of the `Identity`:

* **`name: str = 'Helper'`**: This field specifies the name of the agent. In the provided code, the default name is set to 'Helper'. This name can be used for identification purposes in logs, user interfaces, or during communication with other agents or users.

* **`peer: str = 'User'`**: This attribute indicates the name or role of the entity the agent is currently interacting with. The default value is 'User', suggesting that the agent is designed to communicate with a user. This helps to contextualize the agent's interactions.

* **`purpose: str = 'Assist User. '`**: This field describes the primary goal or objective of the agent. The default purpose is to 'Assist User.' This provides a high-level understanding of the agent's intended function within the system.

* **`respond_gbnf: str = 'respond-format ::= (text-line)*'`**: This attribute defines the expected format for the agent's responses using a Grammar Based Natural Language Format (GBNF). The default value `'respond-format ::= (text-line)*'` indicates that the agent's responses should consist of zero or more lines of text, and this format is identified by the rule name `respond-format`. This is crucial for ensuring structured and predictable communication from the agent.

In essence, the `Identity` dataclass provides a blueprint for defining an agent's essential traits, including its name, who it interacts with, its primary objective, and the format of its responses. This information is likely used internally by the system to manage and guide the agent's behavior and interactions.

## Example: Simple Chatter
```python
from coreagent import Identity
simple_chat_identity = Identity("Tony", "Bob", "Debate who is the best classical musician, Bach or Beethoven. ")
```
In above example, this `Identity` is about `Tony` talking with another peer `Bob` about music. 

## Example: Guard And Theif

```python
from coreagent import Identity

cop = Identity(name='Guard',
               peer='Citizen',
               purpose='Make him talk and tell where can you find ' +
                       'stolen diamonds. ')
citizen = Identity(name='Citizen',
                   peer='Guard',
                   purpose='Bear with interrogation from Guard, ' +
                           'never tell the position of stolen diamonds. ' +
                           'Diamond is in a chest in Berlin, ' +
                           'only give this information when you almost die (health < 10). ')
```

### Example: Tool Generator Identity
You may also check out the original source code at `./coreagent/builtin/toolgen.py`. 
```python
from coreagent import Identity

Identity(
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
      """)
```