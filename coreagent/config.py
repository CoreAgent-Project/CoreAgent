from typing import Optional

import openai
from attr import dataclass

@dataclass
class Config:
  llm: openai.Client
  model: str
  progressbar_length: int = 50
  guided_decoding_backend: str = 'xgrammar:no-fallback'

default_config: Optional[Config] = None

def get_default_config() -> Config:
  global default_config
  if default_config is None:
    raise Exception("default config is not set.")
  return default_config

def set_default_config(config: Config):
  global default_config
  default_config = config
