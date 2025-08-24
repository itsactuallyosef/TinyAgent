import os, subprocess, sys
from google.genai import types

def run_python_file(working_directory: str, file_path: str, args=[]):
    full_path = os.path.join(working_directory, file_path)
    abs_path = os.path.abspath(full_path)

    if not abs_path.startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.exists(abs_path):
        return f'Error: File "{file_path}" not found.'
    
    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    try:
        completed = subprocess.run(
            [sys.executable, abs_path, *args],
            cwd=working_directory,
            capture_output=True,
            timeout=30, 
            text=True
        )

        stdout = completed.stdout.strip()
        stderr = completed.stderr.strip()
        
        parts = []
        if stdout:
            parts.append(f"STDOUT: \n{stdout}")
        if stderr:
            parts.append(f"STDERR: \n{stderr}")
        if completed.returncode != 0:
            parts.append(f"Process exited with code {completed.returncode}")

        if not parts:
            return "No output produced."
        
        return "\n".join(parts)
    except subprocess.TimeoutExpired:
        return "Error: Process timed out after 30 seconds"
    except Exception as e:
        return f"Error: {str(e)}"

run_python_file_schema = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file located within the working directory and captures its output. It can also pass optional arguments to the script.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The relative path to the Python file from the working_directory."
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING
                ),
                description="Optional list of string arguments to pass to the Python script."
            )
        },
        required=["file_path"]
    )
)