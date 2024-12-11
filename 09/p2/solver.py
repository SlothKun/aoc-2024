diskMap = ""

freeBlock = {}
fileBlock = {}
blockId = []
total = 0
filePosID = 0
freePosID = 0

with open("../tinput",'r') as ofile:
    for line in ofile.readlines():
        line = line.strip("\n")
        idCount = 0

        for layoutIdx in range(len(line)):
            if layoutIdx % 2 == 0: # file space
                fileBlock[f'fi{filePosID}'] = (int(line[layoutIdx]), idCount) # NB - ID
                blockId.append(f'fi{filePosID}')
                diskMap += str(idCount)*int(line[layoutIdx])
                idCount += 1
                filePosID += 1
            else: # free space
                if int(line[layoutIdx]) != 0:
                    freeBlock[f'fr{freePosID}'] = int(line[layoutIdx]) # NB
                    blockId.append(f'fr{freePosID}')
                    freePosID += 1
                    diskMap += '.'*int(line[layoutIdx])

print(f"freeBlock : {freeBlock}")
print(f"fileBlock : {fileBlock}")
print(f"blockId :", blockId)
print(diskMap)

fileTurn = True 


def draw(blockId):
    diskMap=''
    for id in blockId:
        if 'fr' in id:
            diskMap += '.'*freeBlock[id]
        else: 
            diskMap += str(fileBlock[id][1])*fileBlock[id][0]
    print(diskMap)





print("\n\n\n")
for fib in list(fileBlock.keys())[::-1]:
    fiIdx = -1
    frIdx = -1
    for frb in freeBlock.keys():
        fiIdx = blockId.index(fib)
        frIdx = blockId.index(frb)
        #print("frIdx:", frIdx)
        #print("fiIdx:", fiIdx)
        if freeBlock[frb] > fileBlock[fib][0] and frIdx < fiIdx:
            print(f"------------------\n{frb} > {fib}\n{freeBlock[frb]} > {fileBlock[fib][0]}")
            delfiBlock = False
            freeBlock[frb] = freeBlock[frb] - fileBlock[fib][0] # Compute space left
            # Create a new freeBlock
            freeBlock[f'fr{freePosID}'] = fileBlock[fib][0]
            if fiIdx+1 < len(blockId):
                if "fr" in blockId[fiIdx-1] and "fr" in blockId[fiIdx+1]: # if the space before and after current fileBlock is a freeBlock, merge
                    print("1")
                    freeBlock[f'fr{freePosID}'] += freeBlock[blockId[fiIdx+1]]
                    freeBlock[blockId[fiIdx-1]] += freeBlock[f'fr{freePosID}']
                    print(f"Deleting {blockId[fiIdx+1]}")
                    print(f"Deleting fr{freePosID}")
                    del freeBlock[blockId[fiIdx+1]]
                    del freeBlock[f'fr{freePosID}'] # Empty space no longer exist, delete it
                    delfiBlock = True
                    #blockId.remove(f'fr{freePosID-1}') # then delete fileBlock from BlockId
                    #blockId.remove(f'fr{freePosID+1}') # then delete fileBlock from BlockId
                    blockId.pop(fiIdx+1) # then delete fileBlock from BlockId
                elif "fr" in blockId[fiIdx-1]: # if the space before/after current fileBlock is a freeBlock, merge
                    print("0")
                    freeBlock[blockId[fiIdx-1]] += freeBlock[f'fr{freePosID}']
                    del freeBlock[f'fr{freePosID}'] # Empty space no longer exist, delete it
                    delfiBlock = True

                elif "fr" in blockId[fiIdx+1]: # if the space before/after current fileBlock is a freeBlock, merge
                    print("2")
                    freeBlock[blockId[fiIdx+1]] += freeBlock[f'fr{freePosID}']
                    del freeBlock[f'fr{freePosID}'] # Empty space no longer exist, delete it
                    delfiBlock = True
                else: # no freespace
                    print("3")
                    blockId[fiIdx] = f'fr{freePosID}' # then replace fileBlock from BlockId to new FreeBlock
            else:
                if "fr" in blockId[fiIdx-1]: # if the space before/after current fileBlock is a freeBlock, merge
                    print("4")
                    freeBlock[blockId[fiIdx-1]] += freeBlock[f'fr{freePosID}']
                    del freeBlock[f'fr{freePosID}'] # Empty space no longer exist, delete it
                    delfiBlock = True
                else: # no freespace
                    print("5")
                    blockId[fiIdx] = f'fr{freePosID}' # then replace fileBlock from BlockId to new FreeBlock

            blockId.insert(frIdx, fib) # Move FileBlock before space
            freePosID += 1
            print(f"BEF blockId :", blockId)
            print(f"BEF blockId :", fiIdx)
            if delfiBlock: blockId.pop(fiIdx+1) # delete fileBlock from BlockId
            print(f"freeBlock : {freeBlock}")
            print(f"fileBlock : {fileBlock}")
            print(f"blockId :", blockId)
            draw(blockId)
            break # No need to iterate much longer, next fileblock
        elif freeBlock[frb] == fileBlock[fib][0] and frIdx < fiIdx:
            print(f"------------------\n{frb} == {fib}\n{freeBlock[frb]} == {fileBlock[fib][0]}")
            print(f"blockId :", blockId)
            delfiBlock = False
            delfrBlock = False
            if fiIdx+1 < len(blockId):
                if "fr" in blockId[fiIdx-1] and "fr" in blockId[fiIdx+1]: # if the space before and after current fileBlock is a freeBlock, merge
                    print("1")
                    freeBlock[frb] += freeBlock[blockId[fiIdx+1]]
                    freeBlock[blockId[fiIdx-1]] += freeBlock[frb]
                    delfiBlock = True
                    delfrBlock = True
                    del freeBlock[blockId[fiIdx+1]]
                    blockId.pop(fiIdx+1) # then delete fileBlock from BlockId
                else: 
                    blockId[fiIdx] = frb
                    blockId[frIdx] = fib
                    delfiBlock = False
                    delfrBlock = False
                """
                elif "fr" in blockId[fiIdx-1]: # if the space before/after current fileBlock is a freeBlock, merge
                    # Si == et block seulemnt avant : swap les positions
                    print("0a")
                    blockId[fiIdx] = frb
                    blockId[frIdx] = fib
                    delfiBlock = False
                    delfrBlock = False
                elif "fr" in blockId[fiIdx+1]: # if the space before/after current fileBlock is a freeBlock, merge
                    print("2")
                    freeBlock[blockId[fiIdx+1]] += freeBlock[frb] 
                    delfiBlock = True
                else:
                    print("4a")
                    blockId[fiIdx] = frb
                    blockId[frIdx] = fib
                    delfiBlock = False
                    delfrBlock = False
                    #freeBlock[f'fr{freePosID}'] = freeBlock[frb]
                    #blockId[fiIdx] = f'fr{freePosID}' # then replace fileBlock from BlockId to new FreeBlock
                    #freePosID += 1
                """
            else:
                if "fr" in blockId[fiIdx-1]: # if the space before/after current fileBlock is a freeBlock, merge
                    # Si == et block seulent avant : swap les positions
                    print("0b")
                    blockId[fiIdx] = frb
                    blockId[frIdx] = fib
                    delfiBlock = False
                    delfrBlock = False
                else:
                    print("4b")
                    freeBlock[f'fr{freePosID}'] = freeBlock[frb]
                    blockId[fiIdx] = f'fr{freePosID}' # then replace fileBlock from BlockId to new FreeBlock
                    freePosID += 1
                

            #print(frIdx)
            #print(f"blockId :", blockId)
            print(f"freeBlock 1: {freeBlock}")
            if delfiBlock: blockId.remove(fib) # delete fileBlock from BlockId
            print(f"freeBlock 2: {freeBlock}")
            print(f"blockId 2:", blockId)
            blockId[frIdx] = fib # Fill freeBlock with fileBlock

            print(f"freeBlock 3: {freeBlock}")
            if delfrBlock : del freeBlock[frb] # Empty space no longer exist, delete it
            print(f"n freeBlock : {freeBlock}")
            print(f"fileBlock : {fileBlock}")
            print(f"n blockId :", blockId)
            draw(blockId)
            break # No need to iterate much longer, next fileblock
        #print(frb) 



print(diskMap)
draw(blockId)
print(diskMap)

posCount = 0
for id in blockId:
    if 'fr' in id:
        posCount+=freeBlock[id]
    else: 
        for oc in range(fileBlock[id][0]):
            total += posCount*fileBlock[id][1]
            
            posCount += 1

print(total)

