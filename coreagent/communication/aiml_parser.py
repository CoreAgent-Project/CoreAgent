def parse_aiml(aiml_str: str) -> dict:
  """
  Parses AIML-like syntax string and returns a dictionary.

  Args:
      aiml_str: The AIML-like syntax string to parse.

  Returns:
      A dictionary representing the parsed AIML structure.
      Key-value pairs are stored as direct entries in the dictionary.
      String blocks are also stored as entries with their keys and content.
  """
  if aiml_str is None or aiml_str == '':
    return {}
  result = {}
  lines = aiml_str.splitlines()
  i = 0
  while i < len(lines):
    line = lines[i]
    if not line:  # Skip empty lines
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
            if i < len(lines) and lines[i].strip() and not lines[i].strip().startswith(
                "%$"):  # consume optional lineTerminator after _<
              i += 1  # skip if there is a line after _< and it is not a new block
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
          raise ValueError(f"Invalid key-value pair syntax at line {i + 1}: {line}")
        key = parts[0].strip()
        value = parts[1].strip()

        if not _is_valid_key(key):
          raise ValueError(f"Invalid key at line {i + 1}: {key}")

        result[key] = value
        i += 1
      else:
        raise ValueError(f"Invalid syntax at line {i + 1}: {line}. Expected '=' or '=>_' after '%$'")
    else:
      # Ignore lines not starting with %$ (for now, could be error depending on desired strictness)
      i += 1

  return result


def _is_valid_key(key: str) -> bool:
  """Checks if a key is valid according to the grammar, now allowing underscores."""
  if not key:
    return False
  for char in key:
    if not (char.isalnum() or char == ":" or char == "_"):
      return False
  return True
