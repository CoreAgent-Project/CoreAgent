import openai
from coreagent.communication import aiml_example

simplified_sql_grammar = r"""
root ::= (key-value-block)
key-value-block ::= key-start value-content key-end
key-start ::= "%$" key "=>_" newline
key-end ::= "%$_<" newline?
key ::= (namespace ":" sub-key) | simple-key
namespace ::= [-a-zA-Z0-9_]+
sub-key ::= [-a-zA-Z0-9_]+
simple-key ::= [-a-zA-Z0-9_]+
value-content ::= (text-line | key-value-block)*
text-line ::= [^\n]* newline
newline ::= "\n"
"""

cli = openai.Client(
  base_url='http://192.168.1.5:9900/v1/',
  api_key='1',
)

from coreagent.communication.gbnf_gen import get_test
total_content = ''
for z in cli.chat.completions.create(
    model="llm",
    messages=[
      {
        "role": "system",
        "content": f"You only write in following format. \n----\n{aiml_grammar}\n----{aiml_example}\n"
      },
      {
        "role": "user",
        "content": "say hello",
      }
    ],
    extra_body={"guided_grammar": get_test(), "guided_decoding_backend": 'xgrammar'},
    # extra_body={"guided_grammar": simplified_sql_grammar, "guided_decoding_backend": 'xgrammar:no-fallback'},
    stream=True,
):
  d = z.choices[0].delta
  if hasattr(d, 'reasoning_content') and len(d.reasoning_content) > 0:
    t = d.reasoning_content
  else:
    t = d.content
    total_content += d.content
  print(t, end='', flush=True)
print()
