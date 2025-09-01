import os
from dotenv import load_dotenv
from google import genai
import sys
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)
from google.genai import types

def main():
    
   
    
    if len(sys.argv) < 2:
        print("No prompt was entered")
        return 1
    else:

        messages = [
                 types.Content(role="user", parts=[types.Part(text=sys.argv[1])]),
                 ]

        response = client.models.generate_content(
                model='gemini-2.0-flash-001', 
                contents=messages,
                )
        if len(sys.argv) == 3:
            if sys.argv[2] == "--verbose":
                print(f"User prompt: {sys.argv[1]}")
                print(f'Prompt Tokens: {response.usage_metadata.prompt_token_count}')
                print(f'Response Tokens: {response.usage_metadata.candidates_token_count}')
        
        print(response.text)    
        return 0

if __name__ == "__main__":
    main()
