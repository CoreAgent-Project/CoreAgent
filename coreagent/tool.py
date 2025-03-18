import typing
from typing import Optional, Callable

import pydantic
from attr import dataclass
from pydantic import Field, BaseModel


class ToolCall(pydantic.BaseModel):
  name: str = Field(description='Name of the function to call. ')
  param: Optional[dict] = Field({}, description="Parameters of the function. ")

@dataclass
class ToolDesc:
  name: str
  desc: str
  parameters: str
  param_names: typing.List[str]
  def __str__(self):
    desc = self.desc.replace("\n", "")
    params = "\n".join([("- " + x) for x in self.parameters.split("\n")])
    return f"""
    **{self.name}**
    Tool [{self.name}] Description: {desc})
    Tool [{self.name}] parameters: 
    {params}
    """

import yaml
import inspect
def parseFuncDesc(c: Callable[..., str]):
  d = [x.strip()[1:].strip() for x in (c.__doc__ or '').split("\n") if len(x.strip()) > 0 and x.strip().startswith('#')]
  return '\n'.join(d)

def parseFuncParameters(c: Callable[..., str]):
  meta = yaml.safe_load(c.__doc__ or '') or {}
  sig: inspect.Signature = inspect.signature(c)
  params = sig.parameters
  str = []
  names = []
  for k in params:
    t = params[k].annotation
    if t == inspect.Parameter.empty:
      raise Exception("No type annotation for " + k + ". ")
    str.append(f"{k}: {t.__name__}")
    names.append(k)
  return "\n".join(str) if len(str) > 0 else "(none)", names

def parseFuncAsModel(c: Callable[..., str]):
  meta = yaml.safe_load(c.__doc__ or '') or {}
  sig: inspect.Signature = inspect.signature(c)
  params = sig.parameters
  for k in params:
    t = params[k].annotation
    if t == inspect.Parameter.empty:
      raise Exception("No type annotation for " + k + ". ")
  m = pydantic.create_model('func_' + c.__name__, **{k: (t, pydantic.Field(description=meta[k] if k in meta else None)) for k in params})
  return m

if __name__ == '__main__':
  def m(name: str, score: int, dead: bool) -> str:
    """
    # Get the student's score.
    name: Student's name.
    score: The numerical score.
    """
    return "s"
  print(parseFuncDesc(m))
  print(parseFuncAsModel(m).model_json_schema())
