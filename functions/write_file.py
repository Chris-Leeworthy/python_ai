import os
from config import MAX_CHARS
from google.genai import types


def write_file(working_directory, file_path, content):

    try:
        abs_work_path = os.path.abspath(working_directory)
        target = os.path.normpath(os.path.join(abs_work_path, file_path))

        # make sure no-one is playing silly buggers with the path
        valid_target_flag = os.path.commonpath([abs_work_path, target]) == abs_work_path

        if not valid_target_flag:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        if os.path.isdir(target):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        # Get the directory name
        dir_name = os.path.dirname(target)

        if dir_name:
            os.makedirs(dir_name, exist_ok=True)

        with open(target, "w") as f:
            written = f.write(content)

            print(f"{written} characters written")

        return target
    except Exception as e:
        return f"Error: {e}"


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description=(
        "Writes the given content to a file relative to the working directory, "
        "creating parent directories as needed and overwriting any existing file."
    ),
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description=(
                    "Path to the file to write, relative to the working directory."
                ),
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Text content to write to the file.",
            ),
        },
        required=["file_path", "content"],
    ),
)
