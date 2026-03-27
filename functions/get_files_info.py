import os
from google.genai import types


def get_files_info(working_directory, directory="."):
    try:
        abs_work_path = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(abs_work_path, directory))

        # make sure no-one is playing silly buggers with the path
        valid_target_flag = (
            os.path.commonpath([abs_work_path, target_dir]) == abs_work_path
        )

        if not valid_target_flag:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'

        # list the directory contents
        try:
            entries = os.listdir(target_dir)
        except OSError as e:
            return f"Error: {e}"

        lines = []
        for name in entries:
            path = os.path.join(target_dir, name)
            try:
                size = os.path.getsize(path)
                is_dir = os.path.isdir(path)
            except OSError as e:
                return f"Error: {e}"

            lines.append(f"- {name}: file_size={size} bytes, is_dir={is_dir}")

        return "\n".join(lines)
    except Exception as e:
        return f"Error: {e}"


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)
