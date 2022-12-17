# Importing libraries and our own modules
import json
import os.path
import Memory as memoryManager

import json
import os.path

class Folder:
    def __init__(self, name, location, parent):
        self.type = "folder"
        self.children = []
        self.name = name
        self.location = location
        self.parent = parent
        if self.parent != None:
            self.parent.children.append(self)


class File:
    def __init__(self, name, content, parent):
        self.type = "file"
        self.name = name
        self.content = content
        self.size = len(content) # Every character of string is considered 1 byte
        self.parent = parent
        self.parent.children.append(self)

    def write_to_file(self, content, writeAtPosition = 0):
        if writeAtPosition == 0:
            self.content = self.content + content
            self.size = len(self.content)
        else:
            self.content = self.content[:writeAtPosition] + \
                content + self.content[writeAtPosition:]
            self.size = len(self.content)

        print('Write successful')

    def read_from_file(self, start=0, size=0):
        if start == 0 and size == 0:
            return self.content
        else:
            return self.content[start:start+size]

    def move_within_file(self, start, size, target):
        newContent = self.content[start:start+size]
        self.content = self.content[:start] + self.content[start+size:]
        self.content = self.content[:target] + \
            newContent + self.content[target:]
        print('File content successfully moved.')

    def truncate(self, maxSize):
        self.content = self.content[:maxSize]
        self.size = maxSize
        print("File size reduced to {} bytes".format(maxSize))


root = Folder('root', 'root', None)
currentDir = root

def cd(name):
    global currentDir

    if name == '..':
        if (currentDir.parent == None):
            return
        currentDir = currentDir.parent
        return

    iterate = currentDir.children
    # print(iterate)

    for child in iterate:
        if child.name == name:
            if child.type == "folder":
                currentDir = child
                return
    print('No such directory')


def ls():
    global currentDir
    for child in currentDir.children:
        print(child.name)


def mkdir(name):
    global currentDir
    Folder(name, name, currentDir)  
    print('Folder creation successful.')


def create(fileName, fileContent=""):
    global currentDir
    File(fileName, fileContent, currentDir)
    print('File creation successful.')


def move(name, destination):
    global currentDir
    for childToMove in currentDir.children:
        if childToMove.name == name:
            for endPoint in currentDir.children:
                if endPoint.name == destination:
                    if endPoint.type == "folder":
                        print(childToMove.name)
                        endPoint.children.append(childToMove)
                        childToMove.parent = destination
                        currentDir.children.remove(childToMove)
                        print('{} moved to {} folder.'.format(name, destination))
                        return
    print('No such directory')
    return


def delete(fileName):
    global currentDir
    iterate = currentDir.children
    # print(len(iterate))

    for child in iterate:
        if child.name == fileName:
            if child.type == "file":
                currentDir.children.remove(child)
                print("File successfully deleted.")
                return

    print('No such file')
    return


def open_file(fileName):
    global currentDir
    iterate = currentDir.children

    for child in iterate:
        if child.name == fileName:
            if child.type == "file":
                return child

    print('No such file')
    return


def storeRecursively(veryRoot, fileSystem):
    for child in veryRoot.children:
        if child.type == "folder":
            fileSystem[child.name] = {}
            storeRecursively(child, fileSystem[child.name])
        else:
            fileSystem[child.name] = {

                'name': child.name,
                'content': child.content,
                'type': child.type}


def saveToJson():
    # recursively save the tree in a dictionary
    global root
    fileSystem = {}

    storeRecursively(root, fileSystem)

    # print(fileSystem)
    with open("sample.dat", "w") as outfile:
        json.dump(fileSystem, outfile)


def convertJsonToTree(jsonFile, parent):

    global root

    if (root.children == []):
        print("empty")
        parent = root

    for key in jsonFile:
        if type(jsonFile[key]) == dict:

            if jsonFile[key].get('type') == None:
                # i cannot use parent here as recursively it has to be used again with original value
                tempParent = Folder(key, key, parent)

            else:
                File(key, jsonFile[key].get('content'),parent)
                tempParent = parent

            convertJsonToTree(jsonFile[key], tempParent)


def print_directory_structure(directory):
    print(directory.name.upper())
    for child in directory.children:
        if child.type == "file":
            print(" |")
            print("  --> " + child.name, child.size, "bytes")
        else:
            print(" |")
            print("  --> " + child.name)

    print("******************************")

    for child in directory.children:
        if child.type == "folder":
            print_directory_structure(child)
        else:
            return

def manual():
    print("\tOperation Manual")
    print("1. Make a directory - mkdir <folder>")
    print("2. Change the directory - cd <folder>")
    print("3. Create a file - touch <file> <<optional:file content>>")
    print("4. Delete a file - del <file>")
    print("5. Move a file - mov <source folder/file> <destination folder>")
    print("6. Open a file - open <file>")
    print("7. Close a file - close <file>")
    print("8. Write to a file - wr <<optional: write-at position>")
    print("9. Read from a file - rd <<optional: starting index>> <<optional: content size>>")
    print("10. Move within a file - movwithin <starting index> <content size> <target index>")
    print("11. Truncate a file - trunc <size>")
    print("12. List all files & folders in current directory - ls")
    print("13. Display memory map - map")
    print("14. Display directory map - fmap")
    print("15. Exit the system - exit")


child = ""
completeString = ""

# Check if fp exists or is empty
if os.path.isfile('sample.dat'):
    fp = open("sample.dat", "r")
    if os.stat('sample.dat').st_size != 0:
        parent = None
        jsonFile = json.load(open('sample.dat'))
        convertJsonToTree(jsonFile, parent)

print("\t|| FILE MANAGEMENT SYSTEM ||\n")
print("Enter <man> command  to open the operations manual\n")

while (True):
    command = [command for command in input("\n{}> ".format(currentDir.name)).split()]

    match command[0]:
        case 'man':
            manual()
        case 'mkdir':
            if (len(command) == 2):
                mkdir(command[1])
            else:
                print('Invalid Format. Enter "man" for operations manual')
        case 'cd':
            if (len(command) == 2):
                cd(command[1])
            else:
                print('Invalid Format. Enter "man" for operations manual')
        case 'touch':
            if (len(command) == 2):
                create(command[1])
            elif (len(command) >= 3):
                for string in command:
                    if (command.index(string) >= 2):
                        if (command.index(string) < len(command)):
                            if (completeString == ""):
                                completeString = string
                            else:
                                completeString = completeString + " " + string
                        else:
                            break
                # print(completeString)
                create(command[1], completeString)
            else:
                print('Invalid Format. Enter "man" for operations manual')
        case 'del':
            if (len(command) == 2):
                delete(command[1])
            else:
                print('Invalid Format. Enter "man" for operations manual')
        case 'mov':
            if (len(command) == 3):
                move(command[1], command[2])
            else:
                print('Invalid Format. Enter "man" for operations manual')
        case 'open':
            child = open_file(command[1])
            if (child != ""):
                print('Opened {}'.format(child.name))
            else:
                print('File opening failed.')
        case 'close':
            if(child != ""):
                print('{} has been closed'.format(child.name))
                child = ""
            else:
                print('File already closed.')
        case 'wr':
            if (child != "" and len(command) == 1):
                file_text = input("Enter text: ")
                child.write_to_file(file_text)
            elif (child != "" and len(command) == 2):
                file_text = input("Enter text: ")
                child.write_to_file(file_text, int(command[1]))
            else:
                print("No file was opened")
        case 'rd':
            if (child != "" and len(command) == 1):
                file_content = child.read_from_file()
                print(file_content)
            elif (child != "" and len(command) == 3):
                file_content = child.read_from_file(int(command[1]), int(command[2]))
                print(file_content)
            elif (child == ""):
                print("No file was opened")
            else:
                print('Invalid Format. Enter "man" for operations manual')
        case 'movwithin':
            if (child != "" and len(command) == 4):
                child.move_within_file(int(command[1]), int(command[2]), int(command[3]))
            else:
                print("No file was opened")
        case 'trunc':
            if (child != "" and len(command) == 2):
                child.truncate(int(command[1]))
            else:
                print("No file was opened")
        case 'ls':
            ls()
        case 'map':
            print('TO BE IMPLEMENTED. WAITTTT')
        case 'fmap':
            newCurrentDir = root
            print_directory_structure(newCurrentDir)
        case 'exit':
            saveToJson()
            print("Shutting down system & saving... Goodbye!")
            break
        case _:
            print("Command not recognized")
