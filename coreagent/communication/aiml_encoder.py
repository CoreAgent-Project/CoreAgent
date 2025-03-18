def encode_aiml(data: dict):
  entries = []
  for key, value in data.items():
    if isinstance(value, str):
      entries.append(f"%${key}=>_\n{value}\n%$_<")
    else:
      raise Exception("values must be str")
  return "\n".join(entries) + "\n$$EOF$$"
