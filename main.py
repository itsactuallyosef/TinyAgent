from google import genai
from google.genai import types

import os, sys
import argparse
from dotenv import load_dotenv

from typing import List, Union

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

When a user asks a question or makes a request, make a function call plan.
Don't ask for more information.
Use the functions to get information about the files, read file contents, run Python files, and write files as needed to fulfill the user's request.
You can perform the following operations:

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

    generate_content(client, messages, args.verbose)
    print("\n--- Conversation History ---")
    for user_msg in messages:
        print(user_msg.role + ": " + "".join([part.text for part in user_msg.parts if part.text]))
        

def generate_content(client: genai.Client, message: Union[List, str], verbose: bool):
    MAX_ITERATIONS = 20

    for i in range(MAX_ITERATIONS):
        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash-001",
                contents=message,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT,
                    tools=[available_functions]
                )
            )

            # verbose output
            if verbose:
                print(f"\nIteration {i+1}/{MAX_ITERATIONS}")
                print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
                print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
                print("---------------------------------------------------------------")

            # Add candidates' content back to conversation
            for _, candidate in enumerate(response.candidates):
                message.append(candidate.content)

            # If final text is available → done
            if not response.function_calls:
                print(response.text)
                break

            # Otherwise, handle function calls
            for function_call in response.function_calls:
                function_call_result = call_function(function_call, verbose)
                function_response = function_call_result.parts[0].function_response.response

                if not function_response:
                    raise ValueError("Function response is empty")

                result_text = (
                    function_response["result"]
                    if isinstance(function_response, dict) and "result" in function_response
                    else str(function_response)
                )       

                if verbose:
                    print(f"-> {result_text}")

                user_msg = types.Content(
                    role="user",
                    parts=[types.Part(text=result_text)]
                )
                message.append(user_msg)

        except Exception as e:
            print(f"Error during iteration {i+1}: {e}")
            break
    else:
        # Only runs if loop finished all 20 iterations without break
        print("Reached maximum iterations without final response.")

if __name__ == "__main__":
    main()
