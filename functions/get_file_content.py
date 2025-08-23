import os
from config import MAX_CHARS


def get_file_content(working_directory, file_path):
    full_path = os.path.join(working_directory, file_path)
    abs_path = os.path.abspath(full_path)

    if not abs_path.startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.isfile(abs_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    try:
        with open(abs_path, "r") as f:
            content = f.read()
            if len(content) > MAX_CHARS:
                content = content[:MAX_CHARS] + " " + f' [...File "{file_path} truncated at {MAX_CHARS} characters"]'
            return content
    except Exception as e:
        return f'Error: {str(e)}'

