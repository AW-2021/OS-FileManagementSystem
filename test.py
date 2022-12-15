memory = [
    {
        'no': 0, 
        'size': 20,
        'isfull': True, 
        'bytesOccupied': 16, 
        'fileName': 'newFile1', 
        'fileSize': 16
    }, 
    {
        'no': 1, 
        'size': 20, 
        'isfull': True, 
        'bytesOccupied': 18, 
        'fileName': 'newFile2', 
        'fileSize': 18
    },
    {
        'no': 2, 
        'size': 20, 
        'isfull': False, 
        'bytesOccupied': 0, 
        'fileName': '', 
        'fileSize': 0
    }
]

nextObject = {'no': 3, 'size': 20, 'isfull': True, 'bytesOccupied': 10, 'fileName': 'newFile3', 'fileSize': 10}
memory.append(nextObject)

# print(memory[0]['size'])

# memory.pop()
# print(memory)

# memory.insert(0,nextObject)
# print(memory)

# [print(x) for x in memory]

namepassed = 'newFile4'
content = 'HI THERE! COLD OUTSIDE ISNT IT?'
sizepassed = len(content)

namepassed2 = 'newFile5'
content2 = 'HI THERE!'
sizepassed2 = len(content2)

for x in memory:
    if x['isfull'] == False and sizepassed2 <= x['size']:
        x['fileName'] = namepassed2
        x['fileSize'] = sizepassed2
        x['bytesOccupied'] = sizepassed2
        x['isfull'] = True

        print('File store successful.')
        break


[print(x) for x in memory]

