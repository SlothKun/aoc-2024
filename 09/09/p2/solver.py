import time
start_time = time.time()

diskMap = ""
freeBlock = {}
fileBlock = {}
blockId = []
total = 0
filePosID = 0
freePosID = 0

with open("../input",'r') as ofile:
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
                freeBlock[f'fr{freePosID}'] = int(line[layoutIdx]) # NB
                blockId.append(f'fr{freePosID}')
                freePosID += 1
                diskMap += '.'*int(line[layoutIdx])


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
statusCount = 0
for fib in list(fileBlock.keys())[::-1]:
    # check if space available before, if not quit
    fiIdx = blockId.index(fib)
    if 'fr' not in ''.join(blockId[:fiIdx]): break

    print(f"FileBlock {fib} - {time.time()-start_time}.")
    statusCount+=1
    fiIdx = -1
    frIdx = -1
    fileMoved = False
    if len(set(range(1, fileBlock[fib][0]+1)) & set(freeBlock.values())) != 0:
        for frb in freeBlock.keys():
            fiIdx = blockId.index(fib)
            frIdx = blockId.index(frb)
            if freeBlock[frb] > fileBlock[fib][0] and frIdx < fiIdx:
                freeBlock[frb] = freeBlock[frb] - fileBlock[fib][0] # update Freespace with spaceleft
                # Create a new freeBlock
                freeBlock[f'fr{freePosID}'] = fileBlock[fib][0]
                # Replace old fi pos by new freeblock
                blockId[fiIdx] = f'fr{freePosID}'
                # Add fi before currentFreeBlock
                blockId.insert(frIdx, fib) # Move FileBlock before space
                # incr FreeposID
                freePosID += 1
                fiIdx += 1 # icrement because allpos moved by one
                fileMoved = True
                #print(f"1blockId :", blockId)
            elif freeBlock[frb] == fileBlock[fib][0] and frIdx < fiIdx:
                #print(f"------------------\n{frb} == {fib}\n{freeBlock[frb]} == {fileBlock[fib][0]}")
                blockId[fiIdx] = frb
                blockId[frIdx] = fib
                fileMoved = True

            # Check merge
            # fiIdx when we are here rpz the pos of moved/created freeblock
            if fileMoved:
                if fiIdx+1 < len(blockId):
                    # If no free space, do nothing (no merge needed)
                    if "fr" in blockId[fiIdx-1] and "fr" in blockId[fiIdx+1]: # FreeBlock before & After
                        nextFiId = blockId[fiIdx+1]
                        currentFiId = blockId[fiIdx]
                        previousFiId = blockId[fiIdx-1]
                        #print(f"p: {previousFiId} | c: {currentFiId} | n: {nextFiId}")
                        freeBlock[previousFiId] += freeBlock[currentFiId] + freeBlock[nextFiId]
                        del freeBlock[currentFiId]
                        del freeBlock[nextFiId]
                        blockId.pop(fiIdx+1)
                        blockId.pop(fiIdx)
                    elif "fr" in blockId[fiIdx-1]: # Freeblock only before
                        currentFiId = blockId[fiIdx]
                        previousFiId = blockId[fiIdx-1]
                        freeBlock[previousFiId] += freeBlock[currentFiId]
                        del freeBlock[currentFiId]
                        blockId.pop(fiIdx)
                    elif "fr" in blockId[fiIdx+1]: # Freeblock only after
                        nextFiId = blockId[fiIdx+1]
                        currentFiId = blockId[fiIdx]
                        freeBlock[currentFiId] += freeBlock[nextFiId]
                        del freeBlock[nextFiId]
                        blockId.pop(fiIdx+1)
                else:
                    if "fr" in blockId[fiIdx-1]: # Freeblock only before
                        currentFiId = blockId[fiIdx]
                        previousFiId = blockId[fiIdx-1]
                        freeBlock[previousFiId] += freeBlock[currentFiId]
                        del freeBlock[currentFiId]
                        blockId.pop(fiIdx)
                break


print("\n\n\---- END ----")
print(diskMap)
draw(blockId)

posCount = 0
for id in blockId:
    if 'fr' in id:
        posCount+=freeBlock[id]
    else: 
        for oc in range(fileBlock[id][0]):
            total += posCount*fileBlock[id][1]
            posCount += 1

print(total)
print("--- %s seconds ---" % (time.time() - start_time))
