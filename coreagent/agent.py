import copy
import json
import typing

from attr import dataclass
from tqdm import tqdm
from typing import Type, Optional, Callable

import inspect

from .communication import aiml_example, protolang_specs, generate_aiml_syntax, encode_aiml

from .communication import parse_aiml
from .tool import ToolDesc, parseFuncDesc, parseFuncParameters
from .config import Config, get_default_config

default_system_prompt = """
You are [%%NAME%%]. 
You are interfacing with a turn-based scriptable system (ISYS), your peer [%%PEER%%] will interact with ISYS to engage with you.  
Diagram: `[%%PEER%%] <=> ISYS <=> [%%NAME%%] (You)`
----
%%PROTOCOL_DEFINITIONS%%
----
Example RESPOND output: 
```aiml
%$action=>_
RESPOND
%$_<
%$summary=>_
Some of my thoughts... (do not put draft packets here, it means never include "%$", they will cause parsing error! )
%$_< 
%$respond=>_
Hello there!
%$_< 
```
----
Example TOOLCALL output: 
```aiml
%$action=>_
TOOLCALL
%$_<
%$summary=>_
My plan: 
1. ...
2. ...
%$_<
%$param:some_func_param=>_
value
%$_<
```
----
Strictly follow below rules and never change: 
- ISYS is a turn-based system, you must send `respond` in order to receive next message from your peer [%%PEER%%].
- Follow these: repeat(get input => repeat(call tool => analyze result) => respond) 
- You only know knowledge within this chat context, forget prior information, stay on fact.
- Think in Chinese, think simply, and think should you call a function or not. 
- Think short, using 10-words, then propose a draft, then refine it.
- Never include any AIML/PROTOLANG text inside "summary. 
- ALl your thinking process will be removed/lost in next turn, so make sure to put important memories into `summary`. 
- Think when to use string block (eg. for multi-line strings). 
- Make sure not to over-call functions multiple times. 
- Always use tools to get latest information if you can, NEVER depend on previous context or states. 
- You can only either `RESPOND` or `CALLTOOL`. 
- Base solely on given or retrieved information, never assume anything, if not sure, double check (with tools or thinking). 
----
Conversation purpose: 
```
%%PURPOSE%%
```
----
You can and only can use following tools: 
```
%%TOOLS%%
```
----
Now always and only write directly as [%%NAME%%] according to given formatting. 
"""

# apply formatting
default_system_prompt = default_system_prompt.replace("%%PROTOCOL_DEFINITIONS%%", f"""
{aiml_example}
----
{protolang_specs}
""")

@dataclass
class Identity:
  name: str = 'Helper'
  peer: str = 'User'
  purpose: str = 'Assist User. '
  respond_gbnf: str = 'respond-format ::= [^(%$)]+'
  # LLM parameters
  temperature: Optional[float] = None
  frequency_penalty: float = 0.1
  generation_limit: int = 2000
  show_generation: bool = False

class Agent:
    def __init__(self, identity: Identity = None, config: Config = None):
        if config is None:
          config = get_default_config()
        if identity is None:
          identity = Identity()
        self.identity: Identity = identity
        self.config: Config = config
        self.tool_desc: typing.Dict[str, ToolDesc] = {}
        self.tools: typing.Dict[str, Type[Callable[..., str]]] = {}
        self.system_msg = default_system_prompt
        self.msg_history = [
          {'role': 'system', 'content': self.system_msg},
        ]
    def register_tool(self, tool: any, name_prefix: str = None, exclude: typing.Optional[typing.List[str]] = None):
      if name_prefix is None:
        name_prefix = type(tool).__name__
      mem = inspect.getmembers(tool, predicate=inspect.ismethod)
      for v in mem:
        if not v[0].startswith('_') and (exclude is None or v[0] not in exclude):
          self.register_tool_func(v[1], name_prefix + '.' + v[0])
    def register_tool_func(self, f: Callable[..., str], name: Optional[str] = None):
      if name is None:
        name = f.__name__
      if name in self.tools:
        raise Exception(f'tool {name} already registered')
      self.tools[name] = f
      param_desc, param_list = parseFuncParameters(f)
      self.tool_desc[name] = ToolDesc(name=name, desc=parseFuncDesc(f), parameters=param_desc, param_names = param_list)

    # ---- core chatting functions ----
    def chat(self, message: Optional[str] = None, add = True, return_delta: bool = False, continue_last: bool = False):
      history = copy.copy(self.msg_history)
      history[0]['content'] = (self.system_msg
                               .replace("%%NAME%%", self.identity.name)
                               .replace("%%PEER%%", self.identity.peer)
                               .replace("%%PURPOSE%%", self.identity.purpose)
                               .replace("%%TOOLS%%", "----\n".join([self.tool_desc[x].__str__() for x in self.tool_desc])))
      delta_history = [{'role': 'user', 'content': encode_aiml({'sender': 'user', 'text': message})}]
      delta_history = self._run(history, delta_history)
      if add:
        for d in delta_history:
          self.msg_history.append(d)
      if return_delta:
        return delta_history
      return parse_aiml(delta_history[-1]['content'])['respond']
    # ---- internal calls ----
    def _run(self, history, delta_histories) -> typing.List[dict]:
      cloned_history = [*history, *delta_histories]
      # print(cloned_history[0]['content'])
      resp: str = self._call_llm(cloned_history)
      # print(resp)
      aiml: dict = parse_aiml(resp)
      if aiml == {}:
        aiml = {'action': 'RESPOND', 'respond': ''} # default to respond nothing
      action = aiml['action']
      if action == 'RESPOND':
        delta_histories.append({'role': 'assistant', 'content': resp})
        return delta_histories
      if action == 'TOOLCALL':
        # cloned_aiml_without_params = dict([(k, v if not k.startswith('param:') and len(v) > 10 else '(...deducted from memory...)') for k, v in aiml.items()])
        # delta_histories.append({'role': 'assistant', 'content': encode_aiml(cloned_aiml_without_params)})
        delta_histories.append({'role': 'assistant', 'content': resp})
        tool_name = aiml['name']
        if tool_name in self.tools:
          tool = self.tools[tool_name]
          params = dict([(k[6:], aiml[k]) for k in aiml.keys() if k.startswith('param:')])
          print(f'{self.identity.name} call tool {tool_name}')
          # print(param)
          # import sys;sys.exit(0)
          if params == {}:
            tool_resp = tool()
          else:
            tool_resp = tool(**params)
          delta_histories.append({'role': 'user', 'content': encode_aiml({'sender': 'Tool', 'text': str(tool_resp)})})
        else:
          raise Exception(f'tool {aiml["name"]} not registered')
      else:
        delta_histories.append({'role': 'user', 'content': encode_aiml({'sender': 'Nobody', 'text': "(waiting for respond)"})})
      return self._run(history, delta_histories)
    def _call_llm(self, history) -> str:
      # print(json.dumps(history, indent=2))
      grammar_text = generate_aiml_syntax(self.identity.respond_gbnf, dict(
            [(x, self.tool_desc[x].param_names) for x in self.tool_desc]
          ))
      if not self.identity.show_generation:
        r = self.config.llm.chat.completions.create(
          model=self.config.model,
          messages=history,
          temperature=self.identity.temperature,
          extra_body=dict(
            guided_grammar=grammar_text,
            guided_decoding_backend='xgrammar:no-fallback',
          ),
          frequency_penalty=self.identity.frequency_penalty,
          max_completion_tokens=self.identity.generation_limit,
          stop="$$EOF$$",
        )
        if r.choices[0].finish_reason != "stop":
          print(r.choices[0].message.content)
          print(f'WARNING: finish_reason={r.choices[0].finish_reason}')
          raise Exception("too long")
        return r.choices[0].message.content or ''
      ##########
      r = self.config.llm.chat.completions.create(
        model=self.config.model,
        messages=history,
        stream=True,
        temperature=0.0,
        extra_body=dict(
          guided_grammar=grammar_text,
          guided_decoding_backend='xgrammar:no-fallback',
        ),
        frequency_penalty=self.identity.frequency_penalty,
        max_completion_tokens=self.identity.generation_limit,
        stop="$$EOF$$",
      )
      total = ''
      reasoning = ''
      resp = ''
      # prog = tqdm(r, unit='')
      finish_reason = None

      entered_content = False
      for chunk in r:
        # print(chunk.choices[0], flush=True)
        if hasattr(chunk.choices[0].delta, "reasoning_content"):
          total += chunk.choices[0].delta.reasoning_content
          reasoning += chunk.choices[0].delta.reasoning_content
          print(chunk.choices[0].delta.reasoning_content, end='', flush=True)
        elif hasattr(chunk.choices[0].delta, "content") and len(chunk.choices[0].delta.content) > 0:
          if not entered_content:
            entered_content=True
            print("\n========\nOUTPUT: \n")
          total += chunk.choices[0].delta.content
          resp += chunk.choices[0].delta.content
          print(chunk.choices[0].delta.content, end='', flush=True)
        if len(total) > self.config.progressbar_length:
          total = total[-self.config.progressbar_length:]
        # prog.set_postfix_str(total.replace("\n", ""), refresh=False)
        finish_reason = chunk.choices[0].finish_reason
      if finish_reason == 'length':
        raise Exception('generation too long')
      return resp.lstrip("think>")
