from functions.get_files_info import *

def main():
    print("ATTEMPTING TO WRITE")
    print(write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum"))
    
    print("ATTEMPTING TO WRITE")
    print(write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"))

    print("ATTEMPTING TO WRITE")
    print(write_file("calculator", "/tmp/temp.txt", "this should not be allowed"))



if __name__== "__main__":
    main()

