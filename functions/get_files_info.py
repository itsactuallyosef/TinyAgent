import os
from google.genai import types

# Function to get file information in a specified directory
# Example usage: get_files_info("/home/user/project", "src")
# Output: List of files and directories in "src" relative to "/home/user/project"

# It restricts access to the specified working directory and its subdirectories only by
# checking if the absolute path starts with the working directory's absolute path.

def get_files_info(working_directory, directory="."):
    full_path = os.path.join(working_directory, directory)
    
    # Normalized Path
    abs_path = os.path.abspath(full_path);

    if not abs_path.startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    if not os.path.isdir(abs_path):
        return f'Error: The path "{abs_path}" is not a valid directory'
    
    result = []
    
    try:
        # Loop over each entry in the directory,
        # and append the entry's info into 'result' 
        for entry in os.listdir(abs_path):
            entry_path = os.path.join(abs_path, entry)
            
            is_dir = os.path.isdir(entry_path)
            file_size = os.path.getsize(entry_path)

            result.append(f"- {entry}: file_size={file_size} bytes, is_dir={is_dir}")
            
    except Exception as e:
        return f"Error: '{str(e)}'"
    
    return "\n".join(result)


get_files_info_schema = types.FunctionDeclaration(
    name="get_files_info",
    description="List information about files in a specified directory along with their sizes within the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The target directory to list files from, relative to the working directory. Defaults to current directory."
            )
        } 
    )
)