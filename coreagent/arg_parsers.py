from argparse import ArgumentParser
from typing import Sequence, Optional
from collections.abc import Callable

import openai

from coreagent import set_default_config, Config

def set_default_config_from_args(args: Sequence[str] | None = None, argument_parser_handler: Optional[Callable[[ArgumentParser], None]] = None):
  """
  Set default configuration from command-line arguments.
  :param args: Where to parse from? Set to None to use command-line arguments.
  :param argument_parser_handler: In case you want to get extra params.
  :return: Parsed parameters.
  """
  arg_parser = ArgumentParser()
  arg_parser.add_argument("--guided", "-g", action="store_true", default=False, help="Use xgrammar guided generation. ")
  arg_parser.add_argument("--api-base-url", "-u", default='http://192.168.1.5:9900/v1/', help="OpenAI-Compatible API base url. ")
  arg_parser.add_argument("--api-key", "-k", default="1", help="API key ")
  arg_parser.add_argument("--model", "-m", default="llm", help="Model to use. ")
  arg_parser.add_argument("--verbose", "-v", action="store_true", default=False, help="Show generation process via a progress bar. ")

  if argument_parser_handler is not None:
    argument_parser_handler(arg_parser)

  args = arg_parser.parse_args(args)

  if args.api_base_url is None:
    args.api_base_url = None

  if args.verbose:
    print("[Verbose] Showing generation process via a progress bar. ")

  if args.guided:
    print("[Guided] Using guided generation (xgrammar). ")

  cli = openai.Client(
      base_url=args.api_base_url,
      api_key=args.api_key,
  )
  set_default_config(Config(cli, args.model, use_guided_generation=args.guided, show_generation=args.verbose))

  return args
