import os
from functions.config import *
import subprocess
from google.genai import types

def get_files_info(working_directory, directory="."):
    joined_path = os.path.join(working_directory, directory)
    absolute_path = os.path.abspath(joined_path)
    working_dir_abs_path = os.path.abspath(working_directory)

    if (absolute_path.startswith(working_dir_abs_path)) == False:
        return f'\tError: Cannot list "{directory}" as it is outside the permitted working directory'

    if (os.path.isdir(absolute_path)) == False:
        return f'\tError: "{directory}" is not a directory'

    list_of_dirs = os.listdir(absolute_path)
    combined_file_info =""
    for file in list_of_dirs:
        joined_location = os.path.join(absolute_path,file)
        try:
            size_of_file = os.path.getsize(joined_location)
            is_dir = os.path.isdir(joined_location)
            combined_file_info += f'-{file}: file_size={size_of_file}, is_dir = {is_dir}\n'
        
        
        except Exception as e:
            return f'\tError: getting {e}'

    return combined_file_info

def get_file_content(working_directory, file_path):
    joined_path = os.path.join(working_directory, file_path)
    absolute_path = os.path.abspath(joined_path)
    working_dir_abs_path = os.path.abspath(working_directory)

    if (absolute_path.startswith(working_dir_abs_path)) == False:
        return f'\tError: Cannot read "{file_path}" as it is outside the permitted working directory'
    if(os.path.isfile(absolute_path)) == False:
        return f'\tError: File not found or is not a regular file: "{file_path}"'
    
    file_content_string = ""
    try:
        with open(absolute_path, "r") as f:
                  file_content_string += f.read(MAX_CHARACTERS)
    except Exception as e:
                  return f'\tError: {e}'

    return f'\t {file_content_string}'

def write_file(working_directory, file_path, content):
    joined_path = os.path.join(working_directory, file_path)
    absolute_path = os.path.abspath(joined_path)
    working_dir_abs_path = os.path.abspath(working_directory)

    if (absolute_path.startswith(working_dir_abs_path)) == False:
        return f'\tError: Cannot read "{file_path}" as it is outside the permitted working directory'
    try:
        with open(absolute_path, "w") as f:
            f.write(content)

    except Exception as e:
        return f'f\tError: {e}'

    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

def run_python_file(working_directory, file_path, args=[]):
    joined_path = os.path.join(working_directory, file_path)
    absolute_path = os.path.abspath(joined_path)
    working_dir_abs_path = os.path.abspath(working_directory)
    
    if (absolute_path.startswith(working_dir_abs_path)) == False:
        return f'\tError: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if(os.path.isfile(absolute_path)) == False:
        return f'\tError: File "{file_path}" not found'

    if(absolute_path.endswith(".py") == False):
        return f'Error: "{file_path}" is not a Python file'

    try:
        if len(args) < 1:
            completed_process = subprocess.run(["python", absolute_path], capture_output= True, timeout=30)

        else:
            completed_process = subprocess.run(["python", absolute_path, args[0]],capture_output= True, timeout=30)
        #Check if exit code is anything other than 0 
        if completed_process.returncode != 0:
            return f'\tSTDOUT: {completed_process.stdout}\n\tSTDERR: {completed_process.stderr}\n\t Process exited with: {completed_process.returncode}'
        
        if completed_process.stdout == None:
            return f'No output produced'
        
        return f'\tSTDOUT: {completed_process.stdout}\n\tSTDERR: {completed_process.stderr}'

        

    except Exception as e:
        return f'Error: executing Python file: {e}'


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Read out the contents of the specified file, constrained to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The filepath to try to extract contents from, relative to the working directory.",
            ),
        },
    ),
)

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write to the specified filepath location, constrained to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The filepath specifiying the location for where to write to or to create a new file to write to , relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content that will be written into the location at the specified filepath."),
        },
    ),
)

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Execute a Python file in the working directory and return its output.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file, relative to working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="Command-line args passed to the Python file., IS NOT REQUIRED",
                items=types.Schema(type=types.Type.STRING), 
            ),
        },
        required=["file_path"],
    ),
)

