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
