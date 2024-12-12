import copy
import time

start_time = time.time()

sPosList = []
defaultTrail = {'0': {'next':'1','coord': []},
        '1': {'next':'2','coord': []},
        '2': {'next':'3','coord': []},
        '3': {'next':'4','coord': []},
        '4': {'next':'5','coord': []},
        '5': {'next':'6','coord': []},
        '6': {'next':'7','coord': []},
        '7': {'next':'8','coord': []},
        '8': {'next':'9','coord': []},
        '9': {'next':'','coord': []}
         }
trailMap = []
total = 0

with open("../input",'r') as ofile:
    lIdx = 0
    for line in ofile.readlines():
        line = line.strip("\n")
        sPosList += [(lIdx,pos) for pos, char in enumerate(line) if char == '0']
        lIdx+=1
        trailMap.append(line)
    #print(sPosList)

for sPos in sPosList:
    stepNb = '0'
    trail = copy.deepcopy(defaultTrail)
    trail[stepNb]['coord'].append(sPos)

    while stepNb != '9': # stop when '9' is reached
        for c in trail[stepNb]['coord']:
            nextNb = trail[stepNb]['next']
            # verify top
            if c[0] != 0:
                if trailMap[c[0]-1][c[1]] == nextNb and \
                   ((c[0]-1,c[1]) not in trail[nextNb]['coord']):
                    trail[nextNb]['coord'].append((c[0]-1,c[1]))
            # bottom
            if c[0] != len(trailMap)-1:
                if trailMap[c[0]+1][c[1]] == nextNb and \
                   ((c[0]+1,c[1]) not in trail[nextNb]['coord']):
                    trail[nextNb]['coord'].append((c[0]+1,c[1]))
            # left
            if c[1] != 0:
                if trailMap[c[0]][c[1]-1] == nextNb and \
                   ((c[0],c[1]-1) not in trail[nextNb]['coord']):
                    trail[nextNb]['coord'].append((c[0],c[1]-1))
            # right
            if c[1] != len(trailMap[0])-1:
                if trailMap[c[0]][c[1]+1] == nextNb and \
                   ((c[0],c[1]+1) not in trail[nextNb]['coord']):
                    trail[nextNb]['coord'].append((c[0],c[1]+1))
        # Get nex step nb
        #print(f'{stepNb} - {trail[stepNb]}')
        stepNb = trail[stepNb]['next']

    #print(f'{stepNb} - {trail[stepNb]}')
    #print(len(trail['9']['coord']))
    total += len(trail['9']['coord'])

print(total)

elapsed_time = time.time() - start_time
hours, rem = divmod(elapsed_time, 3600)
minutes, seconds = divmod(rem, 60)
milliseconds = (seconds - int(seconds)) * 1000

print("Total time : "+f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}:{int(milliseconds):03}")