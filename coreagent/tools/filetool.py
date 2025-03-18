from pathlib import Path
import os

class FileTool:
  def __init__(self, root_path: str = '.'):
    self.root_path: Path = Path(root_path)
    self.cwd: Path = self.root_path
  def _resolve(self, loc: str) -> Path|None:
    subPath: Path = Path(loc)
    if subPath.is_absolute():
      subPath = self.root_path / subPath.relative_to(subPath.root)
      if not self.root_path in subPath.parents and not self.root_path.samefile(subPath):
        return None
      return subPath
    else:
      p = self.cwd / subPath
      if not self.cwd in p.parents and not self.cwd.samefile(p):
        return None
      return p
  def get_cwd(self):
    """
    # get current dir
    """
    return str(self.cwd.relative_to(self.root_path))
  def cd(self, loc: str):
    """
    # Change working directory.
    """
    p = self._resolve(loc)
    if p is None:
      return "Access denied! "
    self.cwd = p
    return "Changed to: " + str(self.cwd.relative_to(self.root_path))
  def list(self):
    """
    # List all files.
    """
    if not self.cwd.exists():
      return "Current directory does not exist. "
    if not self.cwd.is_dir():
      return "Current directory is not a directory. "
    return "\n".join(os.listdir(str(self.cwd)))
  def write_file(self, file: str, content: str):
    """
    # Write file.
    """
    p = self._resolve(file)
    if p is None:
      return "Access denied! "
    b = content.encode('utf-8')
    p.parent.mkdir(0o0700, parents=True, exist_ok=True)
    p.write_bytes(b)
    return "Wrote to: " + str(p.relative_to(self.root_path)) + "\n" + str(len(b)) + " bytes"
  def read_file(self, file: str) -> str:
    """
    # Read file.
    """
    p = self._resolve(file)
    if p is None:
      return "Access denied! "
    return p.read_text(encoding='utf-8')
