# AI Codebase Agent (Gemini Function-Calling)

An autonomous coding agent that can **inspect, modify, and run code inside a target working directory**. It uses Google’s Gemini function-calling to plan actions (list files, read files, write files, run Python) and iterates until your request is done or the step budget is hit.

---

## Features

- **Natural-language control**: “Add exponentiation to the calculator and run tests.”
- **Tool planning & execution**:
  - `get_files_info` — list files/directories
  - `get_file_content` — read file contents
  - `write_file` — create/overwrite files
  - `run_python_file` — execute a Python file
- **Guard-railed workspace**: all paths are **relative** to a designated working directory (defaults to `./calculator`).
- **Iterative loop**: up to 20 function-calling steps with model feedback.
- **Verbose mode**: see token usage and tool responses for debugging.

---

## Architecture



- **Model**: `gemini-2.0-flash-001`
- **Function tools**: declared with `types.Tool(function_declarations=[...])`
- **Dispatcher**: `call_function()` maps model calls to local tool functions and injects `working_directory`.

---

## Project Layout


├── agent.py # main script (Gemini loop + dispatcher)
├── functions/
│ ├── get_files_info.py # tool impl + schema (exported)
│ ├── get_file_content.py # tool impl + schema (exported)
│ ├── write_file.py # tool impl + schema (exported)
│ └── run_python_file.py # tool impl + schema (exported)
└── calculator/ # default working directory (sample app under edit)

> The agent currently injects `working_directory = "./calculator"` in `call_function()`.

---

## Requirements

- Python **3.10+**
- Google AI Studio API key (Gemini)
- Packages:
  - `python-dotenv`
  - `google-genai`

Create a `requirements.txt` (if not present):
python-dotenv
google-genai

## Quick Start

1. **Clone** this repo.
2. **Create `.env`** with:

GEMINI_API_KEY=your_api_key_here

3. **Install deps**:
```bash
pip install -r requirements.txt

Run:
python agent.py "Add multiply(a, b) to calculator/ops.py and run calculator/main.py"
```
Verbose (debug) mode
python agent.py "List project files" --verbose

Verbose prints your prompt, token usage, each tool call, and tool responses.

Usage Examples

“Find the bug causing division by zero in calculator/ and fix it.”

“Create calculator/advanced.py with power(a, b) and run calculator/main.py.”

“Read all files in calculator and summarize the module boundaries.”

Configuration

API key: loaded from .env → GEMINI_API_KEY.

Working directory: currently hard-coded to ./calculator in call_function().

To make this configurable, add WORKDIR in .env or support a --dir CLI flag and thread it to the tools.

Tool Contracts (expected functions)

Each tool lives in functions/ and must export both the implementation and the schema used in function_declarations.

get_files_info(working_directory, path=".")
Returns file/dir listing (depth is up to your implementation).

get_file_content(working_directory, path)
Returns file text.

write_file(working_directory, path, content)
Creates/overwrites file and returns a status payload.

run_python_file(working_directory, path, args=None, env=None)
Executes a Python file; returns {stdout, stderr, returncode}.

Register schemas in:
available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
        schema_run_python_file,
    ]
)

And map implementations in:

function_mapping = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "write_file": write_file,
    "run_python_file": run_python_file,
}

Security Model

All file ops are forced into the working directory via server-side injection.

The agent is instructed to only use relative paths.

You should still sanitize path in each tool to prevent .. traversal.

