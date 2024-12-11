diskMap = ""
freeBlock = []
fileBlock = []
total = 0

with open("../input",'r') as ofile:
    for line in ofile.readlines():
        line = line.strip("\n")
        idCount = 0
        for layoutIdx in range(len(line)):
            if layoutIdx % 2 == 0: # file space
                fileBlock.append([int(line[layoutIdx]), idCount]) # NB - ID
                idCount += 1
            else: # free space
                freeBlock.append(int(line[layoutIdx])) # NB of free space available

#print(f"freeBlock : {freeBlock}")
#rint(f"fileBlock : {fileBlock}")


posCount = 0
fileTurn = True 
while True:
    # 2 cas : Si fichier ou si espace vide
    if fileTurn: # file space
        print('File')
        for i in range(fileBlock[0][0]): # Count the current file block
            total += posCount*fileBlock[0][1]
            diskMap += str(fileBlock[0][1])
            posCount += 1
        fileBlock.pop(0)
        fileTurn = not fileTurn
    else: # Free space
        print('free')
        for i in range(freeBlock[0]): # Fill free space
            fileBlock[-1][0] -= 1
            total += posCount*fileBlock[-1][1]
            diskMap += str(fileBlock[-1][1])
            if fileBlock[-1][0] == 0:
                fileBlock.pop(-1)
            posCount += 1
        freeBlock.pop(0)
        fileTurn = not fileTurn
    
    if len(fileBlock) == 0:
        break

print(total)
#print(diskMap)