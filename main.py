import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import argparse
from prompt import system_prompt
from call_function import available_functions, call_function


def generate_content(client, messages):
    response = client.models.generate_content(
        model='gemini-3.5-flash', 
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],system_instruction=system_prompt),
    )

    return response

def main():
    load_dotenv()
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    user_prompt = args.user_prompt
    verbose = args.verbose
    messages: list[types.Content] = [
        types.Content(role="user", parts=[types.Part(text=args.user_prompt)])
    ]
    for _ in range(20):
        response = generate_content(client=client, messages=messages)
        if response.usage_metadata is not None:
            if verbose:
                print(f"User prompt: {user_prompt}")
                print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
                print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
            if response.candidates:
                for candidate in response.candidates:
                    messages.append(candidate.content)
            if response.function_calls:
                function_results = []
                for function_call in response.function_calls:
                    function_call_result = call_function(function_call, verbose=verbose)
                    if function_call_result.parts is None:
                        raise Exception("Empty .parts list")
                    elif function_call_result.parts[0].function_response is None:
                        raise Exception("Empty .parts[0].function_response")
                    elif function_call_result.parts[0].function_response.response is None:
                        raise Exception("Empty .parts[0].function_response.response")
                    else:
                        function_results.append(function_call_result.parts[0])
                        if verbose:
                            print(f"-> {function_call_result.parts[0].function_response.response}")
                messages.append(types.Content(role="user", parts=function_results))
            else:
                print(response.text)
                return 0
                    
        else:
            raise RuntimeError("Didnt get a response")
    
    print("Reached maximum amount of iterations.")
    return 1
    


if __name__ == "__main__":
    main()
