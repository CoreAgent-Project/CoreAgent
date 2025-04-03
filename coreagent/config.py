from typing import Optional

import openai
from attr import dataclass

@dataclass
class Config:
  """
  # Configuration file for an Agent, can be shared across Agent instances.
  """
  # ---- essential settings ----
  llm: openai.Client                                    # MUST SET!
  model: str                                            # MUST SET!
  # ---- optional settings ----
  temperature: Optional[float] = None
  frequency_penalty: float = None # generally don't set this, may cause problems.
  generation_limit: int = 5000
  # ---- optional settings ----
  use_guided_generation: bool = False                    # Disable if you're using non vLLM deployments
  guided_decoding_backend: str = 'xgrammar:no-fallback' # Tested with vLLM with Engine v0.
  use_stop_token: bool = False                          # Tested not working with vLLM <= 0.8.0, since stop tokens are also considered during reasoning, see vLLM Issue #14170.
  chat_template_type: Optional[str] = None              # modified chat templates, only for vLLM, one of ["qwq" or None]
  # ---- display only ----
  show_generation: bool = False  # Don't use it for now, a bug in vLLM (tested as of <= v0.8.0) caused random junks to be streamed, check out vLLM Issue #15188.
  progressbar_length: int = 50   # Not used for now

# Default configuration (used internally, do NOT modify directly! )
default_config: Optional[Config] = None

# Get the default configuration
def get_default_config() -> Config:
  global default_config
  if default_config is None:
    raise Exception("default config is not set.")
  return default_config

# Set the default configuration
def set_default_config(config: Config):
  global default_config
  default_config = config
