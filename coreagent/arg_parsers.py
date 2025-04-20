import typing
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
  arg_parser.add_argument("--temperature", "-t", default=None, type=float, help="Temperature for generation. ")

  arg_parser.add_argument("--custom-chat-template", "--tmpl", default=None, type=str, help="Custom chat template to use, only [qwq] now. ")

  # below are some hacky parameters
  arg_parser.add_argument("--deepseek", default=False, action="store_true", help="Automatically setup with DeepSeek Reasoner. ")
  arg_parser.add_argument("--deepseek-chat", default=False, action="store_true", help="Automatically setup with DeepSeek-Chat model (non-reasoning). ")
  arg_parser.add_argument("--bailian", default=False, action="store_true", help="Automatically setup with Aliyun's Bai Lian platform, this still requires \"--model\" parameter. ")

  if argument_parser_handler is not None:
    argument_parser_handler(arg_parser)

  args = arg_parser.parse_args(args)

  if args.deepseek or args.deepseek_chat:
    print("[DeepSeek] Automatic setup, ignoring \"--api-base-url\" and \"--model\". ")
    args.api_base_url = 'https://api.deepseek.com'
    args.model = 'deepseek-reasoner' if args.deepseek else 'deepseek-chat'
  elif args.bailian:
    print("[BaiLian] Automatic setup, ignoring \"--api-base-url\". ")
    args.api_base_url = 'https://dashscope.aliyuncs.com/compatible-mode/v1'

  cli = openai.Client(
      base_url=args.api_base_url,
      api_key=args.api_key,
  )

  kwargs = dict(
    llm=cli,
    model=args.model,
  )

  if args.api_base_url is None:
    args.api_base_url = None

  if args.temperature is not None:
    print("[Temperature] Setting temperature to %f. " % args.temperature)
    kwargs['temperature'] = float(args.temperature)

  if args.verbose:
    print("[Verbose] Showing generation process via a progress bar. ")
    kwargs['show_generation']=args.verbose

  if args.guided:
    print("[Guided] Using guided generation (xgrammar). ")
    kwargs['use_guided_generation']=args.guided,

  if args.custom_chat_template is not None:
    print("[Custom Chat Template] Using custom chat template. ")
    kwargs['chat_template_type'] = args.custom_chat_template

  set_default_config(Config(**kwargs))

  return args
