import argparse
import os
import zipfile

parser = argparse.ArgumentParser()
parser.add_argument("zipfile", type=str)
args = parser.parse_args()

def cd(inputed_command):
    global current

    global currentObjectPath

    global path
    if (len(inputed_command)==2):
        newpath = currentObjectPath.joinpath(inputed_command[1])
        if(newpath.exists() and newpath.is_dir()):
            current = "/" + inputed_command[1]
            currentObjectPath = newpath
        else:
            print("It's not a dir or path doesn't exist")
    elif (len(inputed_command)==1):
        current = ""
        currentObjectPath = zipfile.Path(zipfile.ZipFile(path))

def pwd(inputed_command):
    global current
    if (len(inputed_command)==1):
        print(os.getcwd() + currentObjectPath.name)

def ls(inputed_command):
    global path
    if (len(inputed_command)==1):
        for i in currentObjectPath.iterdir():
            print(i.name)
    elif (len(inputed_command)==2):
        newpath = currentObjectPath.joinpath(inputed_command[1])
        if (newpath.is_dir()):
            for iter in newpath.iterdir():
                print(iter.name)
        else:
            print("It's not a directory")

def cat(inputed_command):
    global currentObjectPath
    if len(inputed_command)==2:
        newpath = currentObjectPath.joinpath(inputed_command[1])
        if (newpath.exists() and newpath.is_file()):
            print(newpath.read_text())
        else:
            print("The file doesn't exist or it's not a file at all!!!")


def main():
    global path
    global current
    global currentObjectPath


    object = zipfile.ZipFile(path)

    currentObjectPath = zipfile.Path(object)


    while True:
        print(path + current +"</>", end='')
        command = input().split()
        if command[0] == "ls":
            ls(command)
            continue
        elif command[0] == "cd":
            cd(command)
        elif command[0] == "pwd":
            pwd(command)
        elif command[0] == "cat":
            cat(command)



if __name__ == '__main__':
    current = ""
    path = args.zipfile
    currentObjectPath = zipfile.Path(zipfile.ZipFile(path))

    main()
