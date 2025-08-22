import os, sys
from google import genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

def main():

    prompt = " ".join(sys.argv[1:])

    if (prompt.strip() == ""): 
        print("Error: Please provide a prompt")
        sys.exit(1)
    
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=prompt
    )

    print("Prompt tokens:", response.usage_metadata.prompt_token_count)
    print("Response tokens:", response.usage_metadata.candidates_token_count)
    print("Response:")
    print(response.text)

if __name__ == "__main__":
    main()
