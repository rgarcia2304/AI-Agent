import os

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
            return f'\tError: getting {file} info'

    return combined_file_info

