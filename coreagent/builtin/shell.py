import subprocess

class AskingShellExecutorTool:
  """
  # Execute a shell command, note that you are never allowed to do deletions or removing files.
  command: "Command to execute. "
  """
  def exec_shell(self, command: str) -> str:
    # Define forbidden command starts (adjust as needed)
    # Checking the first word of the command after stripping whitespace
    forbidden_commands = ['rm', 'del', 'rd', 'rmdir']

    # Clean up command string and split to check the first part
    command_strip = command.strip()
    if not command_strip:
      print("Error: Empty command provided.")
      raise ValueError("Empty command provided.")

    command_parts = command_strip.split()
    executable = command_parts[0].lower()  # Check command case-insensitively

    # Check if the command starts with a forbidden word
    if executable in forbidden_commands:
      error_message = f"Error: Execution of potentially destructive command '{executable}' is forbidden."
      print(error_message)
      # Raise an exception to indicate failure due to policy
      raise PermissionError(error_message)

    # Ask for user confirmation
    print("-" * 40)
    print(f"Attempting to execute command:")
    print(f"  '{command_strip}'")
    print("-" * 40)

    try:
      # Use input() to get confirmation. Handle potential EOFError if input stream closes.
      confirm = input("Are you sure you want to execute this command? (yes/no): ").lower().strip()
    except EOFError:
      print("\nError: Input stream closed. Aborting execution.")
      raise RuntimeError("Could not get user confirmation due to closed input stream.")

    if confirm not in ['yes', 'y']:
      print("Execution cancelled by user.")
      # Return empty string or raise an exception if cancellation should be an error
      # Raising an exception might be clearer that the command did not run.
      raise InterruptedError("Command execution cancelled by user.")

    # Proceed with execution if confirmed and not forbidden
    print(f"\nUser confirmed. Executing command: {command_strip}")
    try:
      result = subprocess.run(
        command_strip,  # Use the stripped command
        shell=True,
        capture_output=True,
        text=True,
        check=True,
        encoding='utf-8',
        errors='replace'
      )
      print("Command executed successfully.")
      return result.stdout

    except subprocess.CalledProcessError as e:
      print(f"Error executing command: '{command_strip}'")
      print(f"Return code: {e.returncode}")
      print(f"Standard Error (stderr):\n{e.stderr}")
      raise e
    except FileNotFoundError:
      print(f"Error: The command or its first part ('{command_parts[0]}') was not found.")
      raise FileNotFoundError(f"Command not found: {command_parts[0]}")
    except Exception as e:
      print(f"An unexpected error occurred while executing '{command_strip}': {e}")
      raise e
