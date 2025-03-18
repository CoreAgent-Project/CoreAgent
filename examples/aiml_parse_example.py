from coreagent.communication import parse_aiml

# Example usage:
text1 = """
%$action=RESPOND
%$respond=some text
"""

parsed1 = parse_aiml(text1)
print("Parsed Example 1:", parsed1)

text2 = """
%$action=TOOL
%$name=text
%$params=>_
some parameter,
another parameter, and some text
or any random text
%$_<
"""

parsed2 = parse_aiml(text2)
print("Parsed Example 2:", parsed2)

text3 = """
%$key:with:colon=value1
%$another_key=another value
%$long_text=>_
This is a long
text block
with multiple lines.
%$_<
%$last_key=final value
%$ns:key = value with prefix spaces. 
"""

parsed3 = parse_aiml(text3)
print("Parsed Example 3:", parsed3)
