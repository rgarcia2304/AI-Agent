import os
from dotenv import load_dotenv
from google import genai
import sys
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)
from google.genai import types
from functions.get_files_info import *
import json

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

-List files and directories
-Return contents of a specific file
-Write to file or create a file
-Run python files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.


"""


def call_function(function_call_part, verbose=False):
    
    #print(f"[DEBUG] raw args: {function_call_part.args}")

    kwargs = dict(function_call_part.args)
    kwargs["working_directory"] = "./calculator"
    
    if (verbose):
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f"Calling function: {function_call_part.name}")

    function_mapping = {"get_files_info":get_files_info, "get_file_content":get_file_content, "write_file":write_file, "run_python_file":run_python_file}
    func = function_mapping.get(function_call_part.name)
    
    if func is None:
        return types.Content(
    role="tool",
    parts=[
        types.Part.from_function_response(
            name=function_name,
            response={"error": f"Unknown function: {function_name}"},
        )
    ],
)

    else:
        result = func(**kwargs)
        return types.Content(
    role="tool",
    parts=[
        types.Part.from_function_response(
            name=function_call_part.name,
            response={"result": result},
        )
    ],
)
 
    
def main():
    
    if len(sys.argv) < 2:
        print("No prompt was entered")
        return 1
    else:
        
        verbose_flag = False

        available_functions = types.Tool(
                function_declarations=[
                        schema_get_files_info,
                        schema_get_file_content,
                        schema_write_file,
                        schema_run_python_file,
                    ])
        
        messages = [
                 types.Content(role="user", parts=[types.Part(text=sys.argv[1])]),
                 ]

        
        for i in range(20):
            
            try:

                response = client.models.generate_content(
                    model='gemini-2.0-flash-001', 
                    contents=messages,
                    config=types.GenerateContentConfig(
                        tools=[available_functions], system_instruction=system_prompt,
                    ))
               
                 #add content to the conversation
                for responses in response.candidates:
                    #print(responses)
                    messages.append(responses.content)

                #print(len(sys.argv))
                if len(sys.argv) == 3:
                    if sys.argv[2] == "--verbose":
                        verbose_flag = True
                        print(f"User prompt: {sys.argv[1]}")
                        print(f'Prompt Tokens: {response.usage_metadata.prompt_token_count}')
                        print(f'Response Tokens: {response.usage_metadata.candidates_token_count}')
        

                if response.function_calls is not None:
                    for i in range(len(response.function_calls)):
                        fc_result = call_function(response.function_calls[i], verbose_flag)
                        fc_response = fc_result.parts[0].function_response.response
                        if (fc_response is not None) and verbose_flag == True:
                            print(f'-> {fc_response}')
                                
                        messages.append(fc_result)
                else:
                     if response.text is not None:
                        print(response.text)
                        break

            except Exception as e:
                return f'Error: {e}'
        
        
        return 0

if __name__ == "__main__":
    main()
