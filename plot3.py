from bitarray.util import ba2int
import matplotlib.pyplot as plt
import bitarray

file1 = open('snapshot.txt', 'r')
Lines = file1.readlines()
yaxis=[]
xaxis=[]
count = 0
ins=1
for line in Lines:
    if line.startswith("cycle"):
        ins=line[6:-2]
        print("cycle = ",ins)
        xaxis.append(ins)

for line in Lines:
    if line.startswith("IF.isStalled:"):
        flag = line[len(line)-6:len(line)-5]
        # print(flag)
        if(flag == "T"):
            count+=1
        # print(count)
    if line.startswith("ID.isStalled:"):
        flag = line[len(line)-6:len(line)-5]
        # print(flag)
        if(flag == "T"):
            count+=1
        # print(count)
    if line.startswith("EX.isStalled:"):
        flag = line[len(line)-6:len(line)-5]
        # print(flag)
        if(flag == "T"):
            count+=1
        # print(count)
    if line.startswith("MEM.isStalled:"):
        flag = line[len(line)-6:len(line)-5]
        # print(flag)
        if(flag == "T"):
            count+=1
        # print(count)
    if line.startswith("WB.nop:"):
        yaxis.append(count)
        count = 0
    
plt.plot(xaxis,yaxis,'ro')
plt.show()