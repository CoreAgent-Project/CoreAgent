from typing import Dict, List

def generate_aiml_syntax(respond_format_gbnf: str, tools: Dict[str, List[str]]) -> str:
    """
    Generates a GBNF grammar that supports RESPOND and TOOLCALL formats,
    ensuring all parameters for a tool are present and ordered.
    Supports dots in tool names by replacing them with underscores in rule names.
    Merges tool call name part and param blocks for stronger association.
    Ensures basic key-value block rules are defined early.

    Args:
        respond_format_gbnf: A string containing GBNF rules, including one named "respond-format".
        tools: A dictionary where keys are tool names and values are lists of parameter names.

    Returns:
        A string containing the complete GBNF grammar.
    """

    tool_call_blocks = []
    param_rules = ""

    for tool_name, params in tools.items():
        sanitized_tool_name = tool_name.replace(".", "_")
        param_block_content = []
        if params:
            for param in params:
                param_rules += f'toolcall-param-{sanitized_tool_name}-{param} ::= key-start-param-{sanitized_tool_name}-{param} value-content key-end\n'
                param_rules += f'key-start-param-{sanitized_tool_name}-{param} ::= "%$" "param:{param}" "=>_" newline\n'
                param_block_content.append(f'toolcall-param-{sanitized_tool_name}-{param}')
            param_string = ' '.join(param_block_content)
            tool_call_blocks.append(f'key-start-name "{tool_name}\\n" key-end {param_string}')
        else:
            tool_call_blocks.append(f'key-start-name "{tool_name}\\n" key-end')

    tool_call_block_rules = "|".join(f'toolcall-{tool.replace(".", "_")}-block' for tool in tools.keys()) if tools else "\"\""
    tool_specific_block_definitions = ""
    for tool_name in tools.keys():
        sanitized_tool_name = tool_name.replace(".", "_")
        tool_specific_block_definitions += f'toolcall-{sanitized_tool_name}-block ::= key-value-block-action-toolcall {tool_call_blocks[list(tools.keys()).index(tool_name)]}\n'

    gbnf_syntax = f"""
root ::= think-block (respond-block | toolcall-block) "$$EOF$$"
think-block ::= "%$summary=>_\\nNew info to remember (<=10 items): \\n" ((("- " text-line){{1,10}}) | ((("- " text-line){{1,11}}) "ok this is too many! \\n")) key-end
key-start-action ::= "%$" "action" "=>_" newline
key-start-respond ::= "%$" "respond" "=>_" newline
key-start-name ::= "%$" "name" "=>_" newline
key-end ::= "%$_<" newline
key-value-block-action-toolcall ::= key-start-action "TOOLCALL\\n" key-end
{respond_format_gbnf}
respond-block ::= key-value-block-action-respond key-value-block-respond
key-value-block-action-respond ::= key-start-action "RESPOND\\n" key-end
key-value-block-respond ::= key-start-respond respond-format key-end
toolcall-block ::= {tool_call_block_rules}
{tool_specific_block_definitions}
"""
    gbnf_syntax += param_rules
    gbnf_syntax += """param-key ::= [-a-zA-Z0-9_]+
value-content ::= text-line*
text-line ::= "%$_<"{0} [^\\n]* "%$_<"{0} newline
newline ::= "\\n"
key-value-block ::= key-start value-content key-end
key-start ::= "%$" key "=>_" newline
key ::= (namespace ":" sub-key) | simple-key
namespace ::= [-a-zA-Z0-9_]+
sub-key ::= [-a-zA-Z0-9_]+
simple-key ::= [-a-zA-Z0-9_]+
"""

    return gbnf_syntax

def get_test():
  respond_format_gbnf = """
  respond-format ::= [^(%$)]+
  """
  tools_test = {
      "get_weather": ["location", "format"],
      "Bomber.drop": ["loc"],
      "Bomber.list": [],
      "Killer.kill": ["name"],
  }

  generated_grammar_test = generate_aiml_syntax(respond_format_gbnf, tools_test)
  return generated_grammar_test
