area = []
antennas = {}
antinodes = []
with open("../input",'r') as ofile:
    lIdx = 0
    for line in ofile.readlines():
        line = line.strip("\n")
        area.append(list(line))
        freqIdx = 0
        for freq in line:
            if freq != '.':
                if freq not in antennas:
                    antennas[freq] = [(lIdx,freqIdx)]
                else:
                    antennas[freq].append((lIdx,freqIdx))
            freqIdx+=1
        lIdx +=1

for ant, cList in antennas.items():
    for c in cList:
        for c2 in cList:
            print("c1 - c2", c, c2)
            if c != c2:
                print("h")
                for mul in range(1, max(len(area), len(area[0]))):
                    vector = (c2[0]-c[0], c2[1]-c[1])
                    pa = [(c[0]-vector[0]*mul, c[1]-vector[1]*mul),(c2[0]-vector[0]*mul, c2[1]-vector[1]*mul)]
                    for a in pa:
                        if 0 <= a[0] < len(area) and 0 <= a[1] < len(area[0]):
                            antinodes.append(a)

print(antinodes)
print(len(set(antinodes)))
