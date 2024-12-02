with open("../inputtest.txt", 'r') as file:
    llist = []
    rlist = []
    print(file.readlines())
    for line in file.readlines():
        line = line.replace("   ", " ").split()
        llist.append(int(line[0]))
        rlist.append(int(line[1]))

llist = sorted(llist)
rlist = sorted(rlist)

total = 0
for i in range(len(llist)):
    total += max(llist[i], rlist[i]) - min(llist[i], rlist[i])

print(total)