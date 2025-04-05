import os.path
from typing import Optional
import codecs

from .filetool import FileTool
from .. import Agent, Config, Identity

class CodeBase:
  def __init__(self, file_tool: Optional[FileTool] = None, override_agent_config: Optional[Config] = None):
    self.codebase = {}
    self.file_tool = file_tool
    self.override_agent_config = override_agent_config
  def list(self):
    """
    # List all known files and their code explanations.
    """
    return {'files': [*self.codebase.keys()]}
  def get_explanation(self, file_name: str):
    """
    # Get the code explanation for a given file.
    file_name: Get existing already-analyzed code file or return None.
    """
    if not file_name in self.codebase:
      return None
    return self.codebase[file_name]
  def analyze_and_add(self, file_name: str):
    """
    # Analyze a file and add its code explanation to the codebase.
    file_name: The file to analyze.
    """
    file_name = os.path.normpath(file_name)
    if file_name in self.codebase:
      return self.codebase[file_name]

    if self.file_tool is None:
      with codecs.open(file_name, 'r', 'utf-8') as f:
        lines = f.readlines()
    else:
      f = self.file_tool._resolve(file_name)
      if f is None:
        return {'ok': False, 'error': 'Access denied! '}
      lines = f.read_text(encoding='utf-8').split('\n')

    lines = ["#L%04d>%s" % (i, line) for i, line in enumerate(lines)]

    agent = Agent(config=self.override_agent_config, identity=Identity(
      name="Code Analyzer",
      peer="CodeBase Manager",
      purpose="Analyze given code and give short report of what this file does. "
    ))
    resp = agent.chat("\n".join(lines))

    data = {
      'file': file_name,
      'explanation': resp,
    }
    self.codebase[file_name] = data
    return data
