from bitarray.util import ba2int
import matplotlib.pyplot as plt
import bitarray

total_reg_instr = 0
total_mem_instr = 0
check_PC = -1

WB_pc, WB_is_I_type, WB_is_R_type, WB_is_B_type, WB_is_S_type, WB_is_L_type, WB_is_P_type = 0, 0, 0, 0, 0, 0, 0


file1 = open('snapshot.txt', 'r')
Lines = file1.readlines()
for line in Lines:
    if (line.startswith("WB.PC:")):
        WB_pc = line[6:38]
    elif (line.startswith("WB.is_I_type:")):
        # if value after WB.is_I_type: in snapshot.txt is True then increment WB_is_I_type to 1
        WB_is_I_type = (
            WB_is_I_type + 1) if line[len(line)-6:len(line)-5] == "T" else WB_is_I_type
    elif (line.startswith("WB.is_R_type:")):
        # if value after WB.is_R_type: in snapshot.txt is True then increment WB_is_R_type to 1
        WB_is_R_type = (
            WB_is_R_type + 1) if line[len(line)-6:len(line)-5] == "T" else WB_is_R_type
    elif (line.startswith("WB.is_B_type:")):
        # if value after WB.is_B_type: in snapshot.txt is True then increment WB_is_B_type to 1
        WB_is_B_type = (
            WB_is_B_type + 1) if line[len(line)-6:len(line)-5] == "T" else WB_is_B_type
    elif (line.startswith("WB.is_S_type:")):
        # if value after WB.is_S_type: in snapshot.txt is True then increment WB_is_S_type to 1
        WB_is_S_type = (
            WB_is_S_type + 1)if line[len(line)-6:len(line)-5] == "T" else WB_is_S_type
    elif (line.startswith("WB.is_L_type:")):
        # if value after WB.is_L_type: in snapshot.txt is True then increment WB_is_L_type to 1
        WB_is_L_type = (
            WB_is_L_type + 1) if line[len(line)-6:len(line)-5] == "T" else WB_is_L_type
    elif (line.startswith("WB.is_P_type:")):
        # if value after WB.is_P_type: in snapshot.txt is True then increment WB_is_P_type to 1
        WB_is_P_type = (
            WB_is_P_type + 1) if line[len(line)-6:len(line)-5] == "T" else WB_is_P_type
        if (check_PC != WB_pc):
            if (WB_is_P_type or WB_is_L_type or WB_is_S_type):
                total_mem_instr += 1
                check_PC = WB_pc
            elif (WB_is_I_type or WB_is_R_type or WB_is_B_type):
                total_reg_instr += 1
                check_PC = WB_pc
        WB_pc, WB_is_I_type, WB_is_R_type, WB_is_B_type, WB_is_S_type, WB_is_L_type, WB_is_P_type = 0, 0, 0, 0, 0, 0, 0


instr_type = ['Register', 'Memory']
instr_count = [total_reg_instr, total_mem_instr]
fig = plt.figure(figsize=(10, 5))
plt.bar(instr_type, instr_count, color='blue', width=0.4)
plt.xlabel("Instruction Type")
plt.ylabel("Number of Instructions")
plt.title("Number of Instructions of each type")
plt.show()
