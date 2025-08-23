from google import genai
from google.genai import types

import os, sys
from dotenv import load_dotenv

# API Client
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

def main():
    load_dotenv()

    verbose = "--verbose" in sys.argv
    args = []
    for arg in sys.argv[1:]:
        if not arg.startswith("--"):
            args.append(arg)
    
    if not args:
        print("AI Code Assistant")
        print('\nUsage: python main.py "your prompt here" [--verbose]')
        print('Example: python main.py "How do I build a calculator app?"')
        sys.exit(1)

    prompt = " ".join(args)
    
    if verbose:
        print(f"User prompt: {prompt}\n")

    # Messages stored for tracking the conversation
    messages = [
        types.Content(role="user", parts=[types.Part(text=prompt)])
    ]

    generate_content(client, messages, True)


def generate_content(client: genai.Client, message, verbose: bool):
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=message
    )

    # verbose output
    if verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    
    print("Response:")
    print(response.text)

if __name__ == "__main__":
    main()
