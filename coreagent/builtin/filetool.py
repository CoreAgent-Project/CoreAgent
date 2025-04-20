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
  def tree(self, dir: str):
    """
    # Walk through all dir and sub-dir list all file structures.
    dir: Path to list all files at.
    """
    resolved = self._resolve(dir)
    if resolved is None:
      return "Root directory does not exist. "
    ret = {}
    for dirname, dirs, files in os.walk(str(resolved), topdown=True, followlinks=True):
      ret[Path(dirname).relative_to(self.root_path)] = '\n'.join(files) + "\n" + '\n'.join([d+' (dir)' for d in dirs])
    return ret
  def exists(self, file: str):
    """
    # Check a file/dir exists or not.
    file: The file to check for existence.
    """
    p = self._resolve(file)
    if p is None:
      return "Access denied! "
    return "file exists" if p.exists() else "file does not exist"
  def get_cwd(self):
    """
    # get current dir
    """
    return "/" + str(self.cwd.resolve().relative_to(self.root_path.resolve()))
  def cd(self, loc: str):
    """
    # Change working directory.
    """
    p = self._resolve(loc)
    if p is None:
      return "Access denied! "
    self.cwd = p
    return "Changed to: /" + str(self.cwd.resolve().relative_to(self.root_path.resolve()))
  def list(self):
    """
    # List all files.
    """
    if not self.cwd.exists():
      return "Current directory does not exist. "
    if not self.cwd.is_dir():
      return "Current directory is not a directory. "
    files = ["\"%s\" (%s)" % (x, 'file' if not os.path.isdir(os.path.join(str(self.cwd), x)) else 'dir') for x in os.listdir(str(self.cwd))]
    return {'files': "\n".join(files), 'count': str(len(files))}
  def mkdir(self, dir: str):
    """
    # Create a directory.
    dir: The directory name to create.
    """
    p = self._resolve(dir)
    if p is None:
      return "Access denied! "
    try:
      p.mkdir(0o0700, parents=True, exist_ok=True)
      return "Created: " + str(p.relative_to(self.root_path))
    except:
      return "Failed to create: " + str(p.relative_to(self.root_path))

  def write_file(self, file: str, content: str):
    """
    # Write a single file.
    # Warning: It will over-write existing file, so make sure write full content, do NOT omit anything.
    file: The single file name to write.
    content: Raw file content to write, everything in it will be written to the file.
    """
    p = self._resolve(file)
    if p is None:
      return "Access denied! "
    b = content.encode('utf-8')
    p.parent.mkdir(0o0700, parents=True, exist_ok=True)
    p.write_bytes(b)
    return "Wrote to: " + str(p.relative_to(self.root_path)) + "\n" + str(len(b)) + " bytes"
  def read_file(self, file: str) -> dict:
    """
    # Read a single file.
    file: The single file name to read.
    """
    p = self._resolve(file)
    str_path = "/" + str(p.resolve().relative_to(self.root_path.resolve()))
    if p is None:
      return {'state': 'error', 'reason': "Access denied! "}
    if p.is_dir():
      return {'state': 'error', 'reason': "Cannot read a directory! "}
    try:
      return {'state': 'ok', 'path': str_path, 'file_content': p.read_text(encoding='utf-8')}
    except:
      return {'state': 'error', 'path': str_path, 'reason': "Failed to read: /" + str(p.resolve().relative_to(self.root_path.resolve()))}
