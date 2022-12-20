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
        xaxis.append(ins)

for line in Lines:
    if line.startswith("IF.PC"):
        mem=line[6:39]
        bit = bitarray.bitarray(mem)
        bit=ba2int(bit)
        yaxis.append(bit)
    else:
        continue;
plt.plot(xaxis,yaxis,'ro')
plt.show()