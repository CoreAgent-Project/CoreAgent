import openai
from coreagent.communication import aiml_example, parse_aiml
from coreagent.communication import protolang_specs

system_prompt = f"""
You're communicating with USER via ISYS system using AIML. 
Diagram: [USER] <=> [ISYS] <=> [YOU]
You only output in PROTOLANG which is in AIML syntax. 
----
{aiml_example}
----
{protolang_specs}
----
Available tools: 
```
**WRITE_FILE**
Tool [WRITE_FILE] Description: Write a file. 
Tool [WRITE_FILE] Parameters: 
- file: str, the file name to write. 
- content_text: str, the content to write. 
```
----

You must strictly follow these rules and never change: 
- Always and only write in PROTOLANG format. 
- Do not hallucinate, only use provided tools. 
- To get latest information, always use corresponding tool (if provided), don't depend on previous context. 
"""

cli = openai.Client(
    base_url='http://192.168.1.5:9900/v1/',
    api_key='1',
)

# from coreagent.communication.ebnf_gen import create_ebnf_for_functions
# ebnf = create_ebnf_for_functions({'WRITE_FILE': ['file', 'content_text']})
# print(ebnf)

total_content = ''
for z in cli.chat.completions.create(
  messages=[
    dict(role='system', content=system_prompt),
    dict(role='user', content='use tool WRITE_FILE, param file set to me.txt, write a poem in it. '),
  ],
  model='llm', stream=True):
  d = z.choices[0].delta
  if hasattr(d, 'reasoning_content') and len(d.reasoning_content) > 0:
    t = d.reasoning_content
  else:
    t = d.content
    total_content += d.content
  print(t, end='', flush=True)
print()
print("============")
print(parse_aiml(total_content))
