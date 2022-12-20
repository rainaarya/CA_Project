from bitarray import bitarray
from bitarray.util import ba2int
import matplotlib.pyplot as plt
# import bitarray

file1 = open('snapshot.txt', 'r')
Lines = file1.readlines()
yaxis=[]
xaxis=[]
mem = 0
ins=1
for line in Lines:
    if line.startswith("cycle"):
        ins=line[6:-2]
    if line.startswith("MEM.ALUresult:"):
        mem  = ba2int(bitarray(line[len(line)-33:len(line)-1]))
    if (line.startswith("MEM.rd_mem:") or line.startswith("MEM.wrt_mem:")):
        flag = line[len(line)-6:len(line)-5]
        # print(flag)
        if(flag == "T"):
            print("int(ins)+1 = ",int(ins)+1)
            if(len(yaxis)>0 and yaxis[-1]!=mem):
                yaxis.pop()
                xaxis.pop()
            xaxis.append(int(ins)+1)
            yaxis.append(mem)
yaxis.pop()
xaxis.pop()
plt.plot(xaxis,yaxis,'ro')
plt.show()