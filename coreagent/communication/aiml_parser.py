import re # Import the regular expression module

def parse_aiml(aiml_str: str) -> dict:
  """
  Parses AIML-like syntax string, potentially wrapped in Markdown code blocks,
  and returns a dictionary.

  Handles input formats like:
  1. Raw AIML string:
     %$key=value
     %$block=>_
     content
     %$_<

  2. AIML wrapped in a code block (with optional surrounding whitespace/newlines):
     ```aiml
     %$key=value
     %$block=>_
     content
     %$_<
     ```

  Args:
      aiml_str: The AIML-like syntax string to parse, possibly wrapped.

  Returns:
      A dictionary representing the parsed AIML structure.
      Key-value pairs are stored as direct entries in the dictionary.
      String blocks are also stored as entries with their keys and content.

  Raises:
      ValueError: If the syntax within the AIML content is invalid
                  (e.g., malformed key-value, unclosed block).
  """
  if aiml_str is None:
    return {}

  pattern = r"^\s*```(aiml)?\s*(.*?)\s*```\s*$"
  match = re.search(pattern, aiml_str, re.DOTALL)

  if match:
    # If a code block is found, use the captured content
    aiml_content_to_parse = match.group(2)
  else:
    # Otherwise, assume the entire input string is the AIML content
    aiml_content_to_parse = aiml_str.strip() # Strip outer whitespace just in case

  # If after extraction or stripping, the content is empty, return empty dict
  if not aiml_content_to_parse:
    return {}
  result = {}
  lines = aiml_str.splitlines()
  i = 0
  while i < len(lines):
    line = lines[i]
    # Strip leading/trailing whitespace from the line itself for processing
    stripped_line = line.strip()

    if not stripped_line:  # Skip empty or whitespace-only lines
      i += 1
      continue
    if line.strip() == "$$EOF$$":
      break

    if line.startswith("%$"):
      line_content = line[2:]  # Remove "%$" prefix
      if "=>_" in line_content:
        # String Block
        parts = line_content.split("=>_", 1)
        if len(parts) != 2:
          raise ValueError(f"Invalid string block syntax at line {i + 1}: {line}")
        string_block_key = parts[0].strip()

        if not _is_valid_key(string_block_key):
          raise ValueError(f"Invalid string block key at line {i + 1}: {string_block_key}")

        string_block_content_lines = []
        i += 1
        while i < len(lines):
          block_line = lines[i]
          if block_line.strip() == "%$_<":  # Corrected condition: Check for exact match "%$_<"
            string_block_content = "\n".join(string_block_content_lines)
            result[string_block_key] = string_block_content
            i += 1
            break  # String block ended
          else:
            string_block_content_lines.append(block_line)
            i += 1
        else:  # Reached end of lines without closing "_<"
          raise ValueError(
            f"Unclosed string block starting at line {i - len(string_block_content_lines)} with key: {string_block_key}")


      elif "=" in line_content:
        # Key-Value Pair
        parts = line_content.split("=", 1)
        if len(parts) != 2:
          raise ValueError(f"Invalid key-value pair syntax at line {i + 1} (relative to extracted content): {line}")
        key = parts[0].strip()
        value = parts[1].strip()

        if not _is_valid_key(key):
          raise ValueError(f"Invalid key at line {i + 1} (relative to extracted content): {key}")

        result[key] = value
        i += 1
      else:
        raise ValueError(f"Invalid syntax at line {i + 1} (relative to extracted content): Expected '=' or '=>_' after '%$'. Line: {line}")
    else:
      i += 1

  return result


def _is_valid_key(key: str) -> bool:
  """Checks if a key is valid according to the grammar, now allowing underscores."""
  if not key:
    return False
  for char in key:
    if not (char.isalnum() or char == ":" or char == "_" or char == "."):
      return False
  return True
