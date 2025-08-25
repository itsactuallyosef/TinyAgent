from google.genai import types
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.run_python import run_python_file
from functions.write_file import write_file

name_to_function = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "run_python_file": run_python_file,
    "write_file": write_file
}

WORKING_DIRECTORY = "./calculator"

def call_function(function_call_part: types.FunctionCall, verbose: bool =False):
    function_name = function_call_part.name.lower()
    function_args = function_call_part.args

    if verbose:
        print(f"Calling function: {function_name}({function_args})")
    else:
        print(f" - Calling function: {function_name}")

    func = name_to_function.get(function_name)

    if not func:
        response = {"error": f"Unknown function: {function_name}"}
    else:
        function_result = func(WORKING_DIRECTORY, **function_args)
        response = {"result": function_result}

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response=response,
            )
        ],
    )



    