# Importing libraries and our own modules
import json
import os.path
import pickle
import Memory as memoryManager
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

        block_returned = M1.write_to_block(self.name, self.content)
        print(f'Write successful\n{block_returned}')

    def read_from_file(self, start=0, size=0):
        if start == 0 and size == 0:
            return self.content
        else:
            return self.content[start:start+size]

    def move_within_file(self, start, target, size):
        newContent = self.content[start:start+size]
        self.content = self.content[:start] + self.content[start+size:]
        self.content = self.content[:target] + \
            newContent + self.content[target:]
        print('File content successfully moved.')

    def truncate(self, maxSize):
        self.content = self.content[:maxSize]
        self.size = maxSize
        print("File size reduced to {} bytes".format(maxSize))

M1 = memoryManager.Memory()
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


def create(fileName, fileContent = ""):
    global currentDir

    if (len(fileContent) <= 50):
        fileobj = File(fileName, fileContent, currentDir)
    else:
        fileobj = File(fileName, fileContent[0:50], currentDir)
    
    block_returned = M1.write_to_block(fileobj.name, fileobj.content)

    if (block_returned == None):
        delete(fileobj.name)
        print(f'File creation failed. Not enough space in memory')
    else:
        print(f'File creation successful.\n{block_returned}')


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
                M1.deallocate_memory(child.name)
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
    return "empty"


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
        #print("empty")
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

# To help users understand which command to enter to carry out desired operation
def manual():
    print("\tOperation Manual")
    print("1. Make a directory - mkdir <folder>")
    print("2. Change the directory - cd <folder>\n NOTE: cd .. to return to root directory")
    print("3. Create a file - touch <file> <<optional:file content>>")
    print("4. Delete a file - del <file>")
    print("5. Move a file - mov <source folder/file> <destination folder>")
    print("6. Open a file - open <file>")
    print("7. Close a file - close <file>")
    print("8. Write to end of file - write_to_file <file> <content>")
    print("9. Write to a file at said position - write_at_pos <file> <write-at position> <content>")
    print("10. Read from a file - rd <file> <<optional: starting index>> <<optional: content size>>")
    print("11. Move within a file - movwithin <file> <starting index> <target index> <content size>")
    print("12. Truncate a file - trunc <file> <size>")
    print("13. Display memory map - show_memory_map")
    print("14. Display directory map - filemap")
    print("15. List all files & folders in current directory - ls")
    print("16. Exit the system - exit")

# Initializing variable to store opened file in
child = ""

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
                completeString = ""
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
            if (child != "" and child != "empty"):
                print('Opened {}'.format(child.name))
            else:
                print('File opening failed.')
        case 'close':
            if(child != ""):
                print('{} has been closed'.format(child.name))
                child = ""
            else:
                print('File already closed.')
        case 'write_to_file':
            if (child == ""): # Opening file for write if not already opened
                child = open_file(command[1])

            if (child != "" and child != "empty" and len(command) >= 3): # Write at end of file
                completeString = ""
                for string in command:
                    if (command.index(string) >= 2):
                        if (command.index(string) < len(command)):
                            if (completeString == ""):
                                completeString = string
                            else:
                                completeString = completeString + " " + string
                        else:
                            break
               
                child.write_to_file(completeString)
            else:
                print('Invalid Format. Enter "man" for operations manual')
        case 'write_at_pos':
            if (child == ""): # Opening file for write if not already opened
                child = open_file(command[1])

            if (child != "" and child != "empty" and len(command) >= 4): # Write at specified position in file
                completeString = ""
                for string in command:
                    if (command.index(string) >= 3):
                        if (command.index(string) < len(command)):
                            if (completeString == ""):
                                completeString = string
                            else:
                                completeString = completeString + " " + string
                        else:
                            break
                child.write_to_file(completeString, int(command[2]))
            else:
                print('Invalid Format. Enter "man" for operations manual')
        case 'rd':
            if (child == ""): # Opening file for write if not already opened
                child = open_file(command[1])

            if (child != "" and child != "empty" and len(command) == 2):
                file_content = child.read_from_file()
                print(file_content)
            elif (child != "" and child != "empty" and len(command) == 4):
                file_content = child.read_from_file(int(command[2]), int(command[3]))
                print(file_content)
            elif (child == "" or child == "empty"):
                print("No file was opened")
            else:
                print('Invalid Format. Enter "man" for operations manual')
        case 'movwithin': 
            if (child == ""): # Opening file for write if not already opened
                child = open_file(command[1])

            if (child != "" and child != "empty" and len(command) == 5):
                if(int(command[3]) > int(command[2])):
                    child.move_within_file(int(command[2]), int(command[3]), int(command[4]))
                else:
                    print("Target index out of range. Try again")
            elif (child == "" or child == "empty"):
                print("No file was opened")
            else:
                print('Invalid Format. Enter "man" for operations manual')
        case 'trunc':
            if (child == ""): # Opening file for write if not already opened
                child = open_file(command[1])

            if (child != "" and child != "empty" and len(command) == 3):
                child.truncate(int(command[2]))
            elif (child == "" or child == "empty"):
                print("No file was opened")
            else:
                print('Invalid Format. Enter "man" for operations manual')
        case 'ls':
            ls()
        case 'show_memory_map':
            M1.memory_map()
        case 'filemap':
            newCurrentDir = root
            print_directory_structure(newCurrentDir)
        case 'exit':
            saveToJson()
            M1.memory_to_json()
            print("Shutting down system & saving... Goodbye!")
            break
        case _:
            print("Command not recognized")
