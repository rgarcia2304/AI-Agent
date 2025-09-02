import os
from dotenv import load_dotenv
from google import genai
import sys
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)
from google.genai import types
from functions.get_files_info import schema_get_files_info

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

-List files and directories

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.


"""

def main():
    
    if len(sys.argv) < 2:
        print("No prompt was entered")
        return 1
    else:
        
        available_functions = types.Tool(
                function_declarations=[
                        schema_get_files_info,
                    ])

        messages = [
                 types.Content(role="user", parts=[types.Part(text=sys.argv[1])]),
                 ]

        response = client.models.generate_content(
                model='gemini-2.0-flash-001', 
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions], system_instruction=system_prompt),
                )
        if len(sys.argv) == 3:
            if sys.argv[2] == "--verbose":
                print(f"User prompt: {sys.argv[1]}")
                print(f'Prompt Tokens: {response.usage_metadata.prompt_token_count}')
                print(f'Response Tokens: {response.usage_metadata.candidates_token_count}')
                

        if len(response.function_calls) > 0:
            for i in range(len(response.function_calls)):
                print(f"Calling function: {response.function_calls[i].name}({response.function_calls[i].args})")
        else:
            print(response.text)    
        return 0

if __name__ == "__main__":
    main()
