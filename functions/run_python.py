import os, subprocess, sys

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
