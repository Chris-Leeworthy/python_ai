import os
import subprocess
from google.genai import types


def run_python_file(working_directory, file_path, args=None):
    try:
        abs_work_path = os.path.abspath(working_directory)
        target = os.path.normpath(os.path.join(abs_work_path, file_path))

        # make sure no-one is playing silly buggers with the path
        valid_target_flag = os.path.commonpath([abs_work_path, target]) == abs_work_path

        if not valid_target_flag:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        # make sure it's a python file
        if not target.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        # let's try to run the file
        command = ["python", target]
        if args:
            command.extend(args)

        completed = subprocess.run(
            command, cwd=abs_work_path, capture_output=True, text=True, timeout=30
        )

        parts = []
        if completed.returncode != 0:
            parts.append(f"Process exited with code {completed.returncode}")

        if not completed.stdout and not completed.stderr:
            parts.append("No output produced")
        else:
            if completed.stdout:
                parts.append("STDOUT:")
                parts.append(completed.stdout)
            if completed.stderr:
                parts.append("STDERR:")
                parts.append(completed.stderr)

        return "\n".join(parts).rstrip("\n")
    except Exception as e:
        return f"Error: executing Python file: {e}"


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description=(
        "Executes a Python file in the working directory with optional "
        "command line arguments and returns its output."
    ),
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description=(
                    "Path to the Python file to execute, relative to the working directory."
                ),
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description=(
                    "Optional list of command line arguments to pass to the Python script."
                ),
                items=types.Schema(
                    type=types.Type.STRING,
                    description="Single command line argument.",
                ),
            ),
        },
        required=["file_path"],
    ),
)
