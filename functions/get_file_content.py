import os
from config import MAX_CHARS


def get_file_content(working_directory, file_path):
    try:
        abs_work_path = os.path.abspath(working_directory)
        target = os.path.normpath(os.path.join(abs_work_path, file_path))

        # make sure no-one is playing silly buggers with the path
        valid_target_flag = os.path.commonpath([abs_work_path, target]) == abs_work_path

        if not valid_target_flag:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(target, "r") as f:
            content = f.read(MAX_CHARS)

            # Check for truncation by reading again
            if f.read(1):
                content += (
                    f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
                )

        return content
    except Exception as e:
        return f"Error: {e}"
