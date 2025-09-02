from functions.get_files_info import *

def main():
    print("TRYING TO RUN FILE")
    print(run_python_file("calculator", "main.py"))

    print("TRYING TO RUN FILE")
    print(run_python_file("calculator", "main.py",["3 + 5"]))

    print("TRYING TO RUN FILE")
    print(run_python_file("calculator", "test.py"))

    print("TRYING TO RUN FILE")
    print(run_python_file("calculator", "../main.py"))

    print("TRYING TO RUN FILE")
    print(run_python_file("calculator", "nonexistent.py"))
    

if __name__== "__main__":
    main()

