import os
from dotenv import load_dotenv
from google import genai


def main():
    # Load ENV vars
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    if api_key is None:
        raise RuntimeError("No API Key found.")

    # Create the AI client object
    client = genai.Client(api_key=api_key)

    # let's try it
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents="Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum.",
    )

    # Outputs
    input_token_count = response.usage_metadata.prompt_token_count
    output_token_count = response.usage_metadata.candidates_token_count
    print(f"Prompt tokens: {input_token_count}")
    print(f"Response tokens: {output_token_count}")
    print(response.text)


if __name__ == "__main__":
    main()
