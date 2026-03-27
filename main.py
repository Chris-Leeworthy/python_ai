import os
import sys
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions, call_function


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
    # Conversation history; start with the user's prompt
    messages: list[types.Content] = [
        types.Content(role="user", parts=[types.Part(text=args.user_prompt)])
    ]
    # Limit the number of tool/response iterations
    for _ in range(20):
        # Call the model with the current conversation history
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions],
                system_instruction=system_prompt,
            ),
        )
        if not response.usage_metadata:
            raise RuntimeError("Gemini API response appears to be malformed")
        if args.verbose:
            print("Prompt tokens:", response.usage_metadata.prompt_token_count)
            print("Response tokens:", response.usage_metadata.candidates_token_count)
        # Add the model's candidate content to the conversation history
        if response.candidates:
            for candidate in response.candidates:
                if candidate.content is not None:
                    messages.append(candidate.content)
        else:
            # No candidates at all is an error for our purposes
            print("Error: Model returned no candidates")
            sys.exit(1)
        # If there are no tool calls, we have a final answer: print and stop
        if not response.function_calls:
            print("Response:")
            print(response.text)
            return
        # There ARE tool calls, so run them and collect results for this iteration
        function_results: list[types.Part] = []
        for function_call in response.function_calls:
            function_call_result = call_function(function_call, verbose=args.verbose)
            # The Content object must have at least one part
            if not function_call_result.parts:
                raise RuntimeError(
                    "Error: call_function returned Content with empty parts"
                )
            first_part = function_call_result.parts[0]
            func_resp = first_part.function_response
            if func_resp is None:
                raise RuntimeError("Error: first Content part has no function_response")
            if func_resp.response is None:
                raise RuntimeError("Error: function_response.response is None")
            # Save this part so the model can see the tool result next turn
            function_results.append(first_part)
            if args.verbose:
                print(f"-> {func_resp.response}")
        # Append all tool results as a single user message so the model can see them
        if function_results:
            messages.append(types.Content(role="user", parts=function_results))
    # If we get here, we hit the iteration limit without a final response
    print("Error: Reached maximum number of iterations without a final response")
    sys.exit(1)


if __name__ == "__main__":
    main()
