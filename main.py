from google import genai
from google.genai import types

import os, sys
import argparse
from dotenv import load_dotenv

from functions.get_files_info import get_files_info_schema
from functions.get_file_content import get_file_content_schema
from functions.run_python import run_python_file_schema
from functions.write_file import write_file_schema
from functions.call_function import call_function


## Argument Parser
parser = argparse.ArgumentParser(description="AI Code Assistant")
parser.add_argument("prompt", type=str, help="The prompt to send to the AI model")
parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose output")

# types.Tool is a collection of functions the model can call
available_functions = types.Tool(
    function_declarations=[
        get_files_info_schema,
        get_file_content_schema,
        run_python_file_schema,
        write_file_schema
    ]
)

SYSTEM_PROMPT = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

def main():
    load_dotenv()

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    args = parser.parse_args()

    if args.verbose:
        print(f"User prompt: {args.prompt}\n")

    # Messages stored for tracking the conversation
    messages = [
        types.Content(role="user", parts=[types.Part(text=args.prompt)])
    ]

    generate_content(client, messages, True)


def generate_content(client: genai.Client, message, verbose: bool):
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=message,
        # lets you tweak how the model generates output—like controlling tone, length, randomness, safety, tool usage, and more
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            tools=[available_functions] # 'tools' are the functions the model can call
        )
    )

    # verbose output
    if verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
        print("---------------------------------------------------------------")
    
    # response.function_calls is a list of function calls the model wants to make
    # “If I had the ability to run functions, here’s what I would call in order.” is what the model is saying

    if not response.function_calls:
        print(response.text)
        return

    for function_call in response.function_calls:
        function_call_result = call_function(function_call, verbose)
        function_response = function_call_result.parts[0].function_response.response

        if not function_response:
            raise ValueError("Function response is empty")
        elif verbose:
            print(f"-> {function_response['result']}")

if __name__ == "__main__":
    main()
