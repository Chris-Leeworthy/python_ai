import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types


def main():
    # Load ENV vars
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    if api_key is None:
        raise RuntimeError("No API Key found.")

    # Create the AI client object
    client = genai.Client(api_key=api_key)

    # get user input to feed to the AI
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")

    args = parser.parse_args()

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    # let's try it
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
    )

    # Outputs
    input_token_count = response.usage_metadata.prompt_token_count
    output_token_count = response.usage_metadata.candidates_token_count
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {input_token_count}")
        print(f"Response tokens: {output_token_count}")

    print(response.text)


if __name__ == "__main__":
    main()
