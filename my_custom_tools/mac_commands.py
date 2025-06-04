import subprocess
import shlex
from langchain_core.tools import tool
from pydantic import BaseModel, Field

# Define the input schema for the tool
class ExecuteCommandArgs(BaseModel):
    command: str = Field(
        ...,
        description="The full shell command string to execute on the Mac M1 terminal. "
                    "Example: 'ls -la', 'echo hello world', 'python3 --version'."
    )

@tool(args_schema=ExecuteCommandArgs)
def execute_mac_command(command: str) -> str:
    """
    Executes a given shell command directly on the Mac M1 terminal and returns its output.
    
    WARNING: This tool allows arbitrary command execution. Use with extreme caution.
    Do not expose this function to untrusted users or environments.
    """
    try:
        # shlex.split robustly splits the command string into a list of arguments,
        # handling quotes and spaces correctly. This is safer than shell=True.
        command_parts = shlex.split(command)

        # Execute the command
        # capture_output=True captures stdout and stderr
        # text=True decodes output as text (UTF-8 by default)
        # check=False prevents CalledProcessError for non-zero exit codes; we handle it manually.
        # timeout is crucial to prevent commands from hanging indefinitely.
        result = subprocess.run(
            command_parts,
            capture_output=True,
            text=True,
            check=False,
            timeout=120 # Command will time out after 120 seconds (2 minutes)
        )

        output = ""
        if result.stdout:
            output += f"STDOUT:\n{result.stdout}\n"
        if result.stderr:
            output += f"STDERR:\n{result.stderr}\n"

        if result.returncode == 0:
            return f"Command executed successfully (Exit Code 0):\n{output}"
        else:
            return f"Command failed with Exit Code {result.returncode}:\n{output}"

    except FileNotFoundError:
        return f"Error: Command '{command_parts[0]}' not found. Please ensure it's in your PATH or provide the full path."
    except subprocess.TimeoutExpired:
        # If the command times out, it's possible some output was generated before timeout
        return (f"Error: Command '{command}' timed out after 120 seconds. "
                f"STDOUT before timeout:\n{result.stdout}\n"
                f"STDERR before timeout:\n{result.stderr}\n")
    except Exception as e:
        return f"An unexpected error occurred during command execution: {e}"

# If you have other tools, you can add them here.
# Open WebUI will discover all functions decorated with @tool in this file.