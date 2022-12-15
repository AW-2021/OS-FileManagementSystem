# Importing libraries and our own modules
import json
import os.path
import Folders_Files as fileManager
import Memory as memoryManager

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
        fileManager.convertJsonToTree(jsonFile, parent)

print("\t|| FILE MANAGEMENT SYSTEM ||\n")
print("Enter <man> command  to open the operations manual\n")

while (True):
    command = [command for command in input("\n{}> ".format(fileManager.currentDir.name)).split()]

    match command[0]:
        case 'man':
            manual()
        case 'mkdir':
            if (len(command) == 2):
                fileManager.mkdir(command[1])
            else:
                print('Invalid Format. Enter "man" for operations manual')
        case 'cd':
            if (len(command) == 2):
                fileManager.cd(command[1])
            else:
                print('Invalid Format. Enter "man" for operations manual')
        case 'touch':
            if (len(command) == 2):
                fileManager.create(command[1])
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
                fileManager.create(command[1], completeString)
            else:
                print('Invalid Format. Enter "man" for operations manual')
        case 'del':
            if (len(command) == 2):
                fileManager.delete(command[1])
            else:
                print('Invalid Format. Enter "man" for operations manual')
        case 'mov':
            if (len(command) == 3):
                fileManager.move(command[1], command[2])
            else:
                print('Invalid Format. Enter "man" for operations manual')
        case 'open':
            child = fileManager.open_file(command[1])
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
            fileManager.ls()
        case 'map':
            print('TO BE IMPLEMENTED. WAITTTT')
        case 'fmap':
            newCurrentDir = fileManager.root
            fileManager.print_directory_structure(newCurrentDir)
        case 'exit':
            fileManager.saveToJson()
            print("Shutting down system & saving... Goodbye!")
            break
        case _:
            print("Command not recognized")
