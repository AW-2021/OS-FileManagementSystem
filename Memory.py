import json
import pickle

class Block:
    def __init__(self, name, size = 30, isFull = False, isOccupied = False, byteOccupied = 0, fileName = None, fileSize = 0, content = None):
        self.name = name
        self.size = size
        self.isFull = isFull
        self.isOccupied = isOccupied
        self.byteOccupied = byteOccupied
        self.fileName = fileName
        self.fileSize = fileSize
        self.content = content


class Memory:
    def __init__(self):
        self.memory = [None] * 20
        self.size = 20
        self.occupied = False

        for i in range(self.size):
            block_obj = Block(f'block {i}')
            self.memory[i] = {
                'name' : block_obj.name,
                'size' : block_obj.size,
                'isFull' : block_obj.isFull,
                'isOccupied' : block_obj.isOccupied,
                'byteOccupied' : block_obj.byteOccupied,
                'fileName' : block_obj.fileName,
                'fileSize' :  block_obj.fileSize,
                'content' : block_obj.content           
            }
        

    def write_to_block(self, inputblock, fName, content):
        for block in self.memory:
            if block != None and block['name'] == inputblock:
                if block['isOccupied'] == False and len(content) <= block['size']:
                    block['fileName'] = fName
                    block['fileSize'] = len(content)
                    block['content'] = content
                    block['byteOccupied'] = len(content)
                    block['isOccupied'] = True
                    if block['byteOccupied'] == block['size']:
                        block['isFull'] = True

                    print('File store successful.')
                    return block
                else:
                    print('File size too large. Try to truncate first.')
            else:
                print('Block not found. Try again')
                          

    def get_value(self, inputblock):
        for block in self.memory:
            if block['name'] == inputblock:
                print('Block found.')
                return block
        
        print('Block not found. Try again...')

    def deallocate_memory(self, fname):
        for block in self.memory:
            if block['fileName'] == fname: 
                block['fileName'] = None
                block['byteOccupied'] = 0
                block['isOccupied'] = False
                block['isFull'] = False
                block['fileSize'] = 0
                block['content'] = None

                print('Successfully dealloacted memory.')
                return
        print('File not allocated in block')

    def memory_map(self):
        map = "MEMORY MAP:\n"
        for block in self.memory:
            map += f"{block['name']}: {block['fileName']} of size {block['fileSize']} bytes\n"
        return map

    def memory_to_json(self):
        mem = self.memory
        memoryStructure = dict()

        for i in range(len(mem)):
            memoryStructure[i] = [mem[i], mem[i]['content']]
            
        #Serializing json
        json_object = json.dumps(memoryStructure, indent=2)
 
        # Writing to memory.json
        with open("memory.json", "w") as outfile:
            outfile.write(json_object)

    def SaveMem(self, savepath_pickle):
        with open(savepath_pickle, "wb") as file:
            pickle.dump(self.memory, file)

    def LoadMem(self, loadpath_pickle):
        with open(loadpath_pickle, 'rb') as file:
            self.memory = pickle.load(file)
    

######################## TESTING FUNCTIONS BELOW ###########################
m1 = Memory()
print(m1.memory[0])

m1.write_to_block('block 0', 'newfile1', 'Hi there hello hello amina')
print(m1.memory[0])
m1.write_to_block('block 1', 'newfile2', 'Good Morning starshine')
print(m1.memory[1])
m1.write_to_block('block 3', 'newfile3', 'Sweet dreams forever')
print(m1.memory[1])

output_block = m1.get_value('block 1')
print(output_block)

m1.deallocate_memory('newfile3')
print(m1.memory[1])

outputmap = m1.memory_map()
print(outputmap)

m1.memory_to_json()
# m1.LoadMem('memory.json')