from bitarray.util import ba2int
import matplotlib.pyplot as plt
import bitarray

total_reg_instr = 0
total_mem_instr = 0
check_PC = -1

WB_pc,WB_is_I_type,WB_is_R_type,WB_is_B_type,WB_is_S_type,WB_is_L_type,WB_is_P_type = 0,0,0,0,0,0,0


file1 = open('snapshot.txt', 'r')
Lines = file1.readlines()
yaxis=[]
instr_type = ['Register', 'Memory']
for line in Lines:
    if (line.startswith("WB.PC:")):
        WB_pc = line[6:39]
        print(WB_pc)
    elif (line.startswith("WB.is_I_type:")):
        # if value after WB.is_I_type: in snapshot.txt is True then increment WB_is_I_type to 1
        WB_is_I_type = WB_is_I_type + 1 if line[13:19] == 'True' else WB_is_I_type
        print(line[13:19])
    elif (line.startswith("WB.is_R_type:")):
        # if value after WB.is_R_type: in snapshot.txt is True then increment WB_is_R_type to 1
        WB_is_R_type = WB_is_R_type + 1 if line[13:19] == 'True' else WB_is_R_type
    elif (line.startswith("WB.is_B_type:")):
        # if value after WB.is_B_type: in snapshot.txt is True then increment WB_is_B_type to 1
        WB_is_B_type = WB_is_S_type + 1 if line[13:19] == 'True' else WB_is_S_type
    elif (line.startswith("WB.is_S_type:")):
        # if value after WB.is_S_type: in snapshot.txt is True then increment WB_is_S_type to 1
        WB_is_S_type = WB_is_S_type + 1 if line[13:19] == 'True' else WB_is_S_type
    elif (line.startswith("WB.is_L_type:")):
        # if value after WB.is_L_type: in snapshot.txt is True then increment WB_is_L_type to 1
        WB_is_L_type = WB_is_L_type + 1 if line[13:19] == 'True' else WB_is_L_type
    elif (line.startswith("WB.is_P_type:")):
        # if value after WB.is_P_type: in snapshot.txt is True then increment WB_is_P_type to 1
        WB_is_P_type = WB_is_P_type + 1 if line[13:19] == 'True' else WB_is_P_type
        if (check_PC != WB_pc):
            if (WB_is_P_type or WB_is_L_type or WB_is_S_type):
                total_mem_instr += 1
                check_PC = WB_pc
            elif (WB_is_I_type or WB_is_R_type or WB_is_B_type):
                total_reg_instr += 1
                check_PC = WB_pc
        WB_pc,WB_is_I_type,WB_is_R_type,WB_is_B_type,WB_is_S_type,WB_is_L_type,WB_is_P_type = 0,0,0,0,0,0,0

print("Total number of register instructions: ", total_reg_instr)
print("Total number of memory instructions: ", total_mem_instr)
        
        
        
        


