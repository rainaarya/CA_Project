import bitarray
from bitarray import bitarray
from bitarray.util import ba2int, int2ba
import copy
import os
import numpy as np
import matplotlib.pyplot as plt

MemSize = 1024

class IFClass:
    def __init__(self):
        self.pc = bitarray(32)
        self.pc.setall(0)
        self.nop = True
        self.isStalled = False
    
class IDClass:
    def __init__(self):
        self.instr= bitarray(32)
        self.instr.setall(0)
        self.nop = True
        self.pc = bitarray(32)
        self.isStalled = False

class EXClass:
    def __init__(self):
        self.instr= bitarray(32)
        self.instr.setall(0)
        self.Read_data1 = bitarray(32)
        self.Read_data1.setall(0)
        self.Read_data2 = bitarray(32)
        self.Read_data2.setall(0)
        self.Imm = bitarray(12)
        self.Imm.setall(0)
        self.Rs2 = bitarray(5)
        self.Rs2.setall(0)
        self.Rs1 = bitarray(5)
        self.Rs1.setall(0)
        self.Rd = bitarray(5)
        self.Rd.setall(0)
        self.is_I_type = False
        self.is_R_type = False
        self.is_B_type = False
        self.is_S_type = False
        self.is_L_type = False
        self.is_P_type = False
        self.rd_mem = False
        self.wrt_mem = False
        self.alu_op = bitarray(10)
        self.alu_op.setall(0)
        self.wrt_enable = False
        self.nop = True
        self.pc = bitarray(32)
        self.isStalled = False

class MEMClass:
    def __init__(self):
        self.instr= bitarray(32)
        self.instr.setall(0)
        self.ALUresult = bitarray(32)
        self.ALUresult.setall(0)
        self.Store_data = bitarray(32) # check for this if needed for risc !!!!!!!!!
        self.Store_data.setall(0)
        self.Rs2 = bitarray(5)
        self.Rs2.setall(0)
        self.Rs1 = bitarray(5)
        self.Rs1.setall(0)
        self.Rd = bitarray(5)
        self.Rd.setall(0)
        self.rd_mem = False
        self.wrt_mem = False
        self.wrt_enable = False
        self.nop = True
        self.is_I_type = False
        self.is_R_type = False
        self.is_B_type = False
        self.is_S_type = False
        self.is_L_type = False
        self.is_P_type = False
        self.pc = bitarray(32)
        self.isStalled = False
    
class WBClass:
    def __init__(self):
        self.instr= bitarray(32)
        self.instr.setall(0)
        self.Wrt_data = bitarray(32)
        self.Wrt_data.setall(0)
        self.Rs2 = bitarray(5)
        self.Rs2.setall(0)
        self.Rs1 = bitarray(5)
        self.Rs1.setall(0)
        self.Rd = bitarray(5)
        self.Rd.setall(0)
        self.wrt_enable = False
        self.nop = True
        self.is_I_type = False
        self.is_R_type = False
        self.is_B_type = False
        self.is_S_type = False
        self.is_L_type = False
        self.is_P_type = False
        self.pc = bitarray(32)
        self.isStalled = False

class stateClass:
    def __init__(self):
        self.IF = IFClass()
        self.ID = IDClass()
        self.EX = EXClass()
        self.MEM = MEMClass()
        self.WB = WBClass()

class RegisterFile:
    def __init__(self):
        self.Registers = [bitarray(32) for i in range(32)]
        for i in range(32):
            self.Registers[i].setall(0)
        self.Reg_data = bitarray(32)
        self.Reg_data.setall(0)
        self.Registers[25] = bitarray("00000000000000000100000000000000") # intializing register for LOADNOC etc
    
    def readRF(self, Reg_addr):
        self.Reg_data = self.Registers[ba2int(Reg_addr)]
        return self.Reg_data
    
    def writeRF(self, Reg_addr, Wrt_reg_data):
        self.Registers[ba2int(Reg_addr)] = Wrt_reg_data
    
    def outputRF(self,cycle):
        with open ("RFresult.txt", "a") as rfout:
            rfout.write("\n\nCycle :\t"+str(cycle)+ "\t\n")
            rfout.write("State of RF:\t\n")
            for i in range(32):
                rfout.write(self.Registers[i].to01())
                rfout.write("\n")
    

class IMem:
    def __init__(self,x):
        self.x=x
        self.clock =0
        self.IMem = [bitarray(8) for i in range(MemSize)]
        #initialize to 0
        for i in range(MemSize):
            self.IMem[i].setall(0)
        with open("imem.txt", "r") as imem:
            i = 0
            for line in imem:
                self.IMem[i] = bitarray(line)
                i += 1
        self.Instruction = bitarray(32)
        self.Instruction.setall(0)
    
    def readInstr(self, ReadAddress):
        insmem = ""
        insmem += self.IMem[ba2int(ReadAddress)].to01()
        insmem += self.IMem[ba2int(ReadAddress)+1].to01()     
        insmem += self.IMem[ba2int(ReadAddress)+2].to01()
        insmem += self.IMem[ba2int(ReadAddress)+3].to01()
        if(self.clock==self.x):
            self.clock =0 
            self.Instruction = bitarray(insmem)
            return (1,self.Instruction)
        self.clock+=1
        failure_bit = bitarray(32)
        failure_bit.setall(0)
        return (0,failure_bit)


class DMem:
    def __init__(self,x):
        self.x=x
        self.clock =0
        self.DMem = [bitarray(8) for i in range(MemSize)]
        #initialize to 0
        for i in range(MemSize):
            self.DMem[i].setall(0)
        with open("dmem.txt", "r") as dmem:
            i = 0
            for line in dmem:
                self.DMem[i] = bitarray(line)
                i += 1
        self.ReadData = bitarray(32)
        self.ReadData.setall(0)
    
    def readDataMem(self, Address):
        if(self.clock==self.x):
            datamem = ""
            datamem += self.DMem[ba2int(Address)].to01()
            datamem += self.DMem[ba2int(Address)+1].to01()
            datamem += self.DMem[ba2int(Address)+2].to01()
            datamem += self.DMem[ba2int(Address)+3].to01()
            self.clock =0 
            self.ReadData = bitarray(datamem)
            return (1,self.ReadData)
        self.clock+=1
        failure_bit = bitarray(32)
        failure_bit.setall(0)
        return (0,failure_bit)
    
    def writeDataMem(self, Address, WriteData):
        if(self.clock<self.x):
            self.clock += 1
            return 0
        self.DMem[ba2int(Address)] = bitarray(WriteData.to01()[:8])
        self.DMem[ba2int(Address)+1] = bitarray(WriteData.to01()[8:16])
        self.DMem[ba2int(Address)+2] = bitarray(WriteData.to01()[16:24])
        self.DMem[ba2int(Address)+3] = bitarray(WriteData.to01()[24:32])
        self.clock=0
        return 1

    def outputDataMem(self,cycle):
        with open("dmemresult.txt", "a") as dmemout:
            dmemout.write("\nCycle :\t"+str(cycle)+ "\t\n")
            for j in range(MemSize):
                dmemout.write(self.DMem[j].to01())
                dmemout.write("\n")

class MMR :
    def __init__(self):
        # for LOADNOC
        self.MMR0 = []
        self.MMR1 = []
        self.MMR2 = []
        self.MMR3 = []
        # for STORENOC
        self.MMR4 = []

    # assume addr in int format
    def writeMem(self,regVal,addr):
        if(addr >= 16384 and addr <= 16387):
            self.MMR0.append(regVal)
        elif (addr >= 16388 and addr <= 16391):
            self.MMR1.append(regVal)
        elif (addr >= 16392 and addr <= 16395 ):
            self.MMR2.append(regVal)
        elif(addr >= 16396 and addr <= 16399):
            self.MMR3.append(regVal)
        else:
            print("Invalid address")
    
    def storeMem(self):
        self.MMR4.append(1)
    
    def outputDataMem(self,cycle):
        with open("mmrresult.txt", "w") as mmrout:
            mmrout.write("Cycle :\t"+str(cycle)+ "\t\n")
            mmrout.write("MMR0: \t" + str(self.MMR0)+" \n ")
            mmrout.write("MMR1: \t" + str(self.MMR1)+" \n ")
            mmrout.write("MMR2: \t" + str(self.MMR2)+" \n ")
            mmrout.write("MMR3: \t" + str(self.MMR3)+" \n ")
            mmrout.write("MMR4: \t" + str(self.MMR4)+" \n ")

    def __repr__(self) -> str:
        print("MMR0: " , self.MMR0)
        print("MMR1: " , self.MMR1)
        print("MMR2: " , self.MMR2)
        print("MMR3: " , self.MMR3)
        print("MMR4: " , self.MMR4)
        return ""


def printState(state, cycle):
    global total_mem_instr
    global total_reg_instr
    global check_PC
    with open ("snapshot.txt", "a") as snap:
        
        snap.write("\n\ncycle " + str(cycle) + "\t\n")
        # IF stage
        snap.write("IF.PC:\t" + state.IF.pc.to01() + "\t\n")
        snap.write("IF.nop:\t" + str(state.IF.nop) + "\t\n")
        snap.write("IF.isStalled:\t" + str(state.IF.isStalled) + "\t\n")
        # ID stage
        snap.write("ID.PC:\t" + state.ID.pc.to01() + "\t\n")
        snap.write("ID.instr:\t" + state.ID.instr.to01() + "\t\n")
        snap.write("ID.nop:\t" + str(state.ID.nop) + "\t\n")
        snap.write("ID.isStalled:\t" + str(state.ID.isStalled) + "\t\n")

        # EX stage
        snap.write("EX.PC:\t" + state.EX.pc.to01() + "\t\n")
        snap.write("EX.instr:\t" + state.EX.instr.to01() + "\t\n")
        snap.write("EX.Read_data1:\t" + state.EX.Read_data1.to01() + "\t\n")
        snap.write("EX.Read_data2:\t" + state.EX.Read_data2.to01() + "\t\n")
        snap.write("EX.Imm:\t" + state.EX.Imm.to01() + "\t\n")
        snap.write("EX.Rs1:\t" + state.EX.Rs1.to01() + "\t\n")
        snap.write("EX.Rs2:\t" + state.EX.Rs2.to01() + "\t\n")
        snap.write("EX.Rd:\t" + state.EX.Rd.to01() + "\t\n")
        snap.write("EX.is_I_type:\t" + str(state.EX.is_I_type) + "\t\n")
        snap.write("EX.is_R_type:\t" + str(state.EX.is_R_type) + "\t\n")
        snap.write("EX.is_B_type:\t" + str(state.EX.is_B_type) + "\t\n")
        snap.write("EX.is_S_type:\t" + str(state.EX.is_S_type) + "\t\n")
        snap.write("EX.is_L_type:\t" + str(state.EX.is_L_type) + "\t\n")
        snap.write("EX.is_P_type:\t" + str(state.EX.is_P_type) + "\t\n")
        snap.write("EX.rd_mem:\t" + str(state.EX.rd_mem) + "\t\n")
        snap.write("EX.wrt_mem:\t" + str(state.EX.wrt_mem) + "\t\n")
        snap.write("EX.alu_op:\t" + state.EX.alu_op.to01() + "\t\n")
        snap.write("EX.wrt_enable:\t" + str(state.EX.wrt_enable) + "\t\n")
        snap.write("EX.isStalled:\t" + str(state.EX.isStalled) + "\t\n")
        snap.write("EX.nop:\t" + str(state.EX.nop) + "\t\n")

        # MEM stage
        snap.write("MEM.PC:\t" + state.MEM.pc.to01() + "\t\n")
        snap.write("MEM.instr:\t" + state.MEM.instr.to01() + "\t\n")
        snap.write("MEM.ALUresult:\t" + state.MEM.ALUresult.to01() + "\t\n")
        snap.write("MEM.Store_data:\t" + state.MEM.Store_data.to01() + "\t\n")
        snap.write("MEM.Rs2:\t" + state.MEM.Rs2.to01() + "\t\n")
        snap.write("MEM.Rs1:\t" + state.MEM.Rs1.to01() + "\t\n")
        snap.write("MEM.Rd:\t" + state.MEM.Rd.to01() + "\t\n")
        snap.write("MEM.rd_mem:\t" + str(state.MEM.rd_mem) + "\t\n")
        snap.write("MEM.wrt_mem:\t" + str(state.MEM.wrt_mem) + "\t\n")
        snap.write("MEM.wrt_enable:\t" + str(state.MEM.wrt_enable) + "\t\n")
        snap.write("MEM.is_I_type:\t" + str(state.MEM.is_I_type) + "\t\n")
        snap.write("MEM.is_R_type:\t" + str(state.MEM.is_R_type) + "\t\n")
        snap.write("MEM.is_B_type:\t" + str(state.MEM.is_B_type) + "\t\n")
        snap.write("MEM.is_S_type:\t" + str(state.MEM.is_S_type) + "\t\n")
        snap.write("MEM.is_L_type:\t" + str(state.MEM.is_L_type) + "\t\n")
        snap.write("MEM.is_P_type:\t" + str(state.MEM.is_P_type) + "\t\n")
        snap.write("MEM.isStalled:\t" + str(state.MEM.isStalled) + "\t\n")
        snap.write("MEM.nop:\t" + str(state.MEM.nop) + "\t\n")

        # WB stage        
        snap.write("WB.PC:\t" + state.WB.pc.to01() + "\t\n")       
        snap.write("WB.instr:\t" + state.WB.instr.to01() + "\t\n")
        snap.write("WB.Wrt_data:\t" + state.WB.Wrt_data.to01() + "\t\n")
        snap.write("WB.Rs2:\t" + state.WB.Rs2.to01() + "\t\n")
        snap.write("WB.Rs1:\t" + state.WB.Rs1.to01() + "\t\n")
        snap.write("WB.Rd:\t" + state.WB.Rd.to01() + "\t\n")
        snap.write("WB.wrt_enable:\t" + str(state.WB.wrt_enable) + "\t\n")
        snap.write("WB.is_I_type:\t" + str(state.WB.is_I_type) + "\t\n")
        snap.write("WB.is_R_type:\t" + str(state.WB.is_R_type) + "\t\n")
        snap.write("WB.is_B_type:\t" + str(state.WB.is_B_type) + "\t\n")
        snap.write("WB.is_S_type:\t" + str(state.WB.is_S_type) + "\t\n")
        snap.write("WB.is_L_type:\t" + str(state.WB.is_L_type) + "\t\n")
        snap.write("WB.is_P_type:\t" + str(state.WB.is_P_type) + "\t\n")
        snap.write("WB.isStalled:\t" + str(state.WB.isStalled) + "\t\n")
        snap.write("WB.nop:\t" + str(state.WB.nop) + "\t\n")
    

def signextend(bits):
    bits=bits.to01()
    if bits[0] == '1':
        bits = '1' * (32 - len(bits)) + bits
    else:
        bits = '0' * (32 - len(bits)) + bits
    return bitarray(bits)


class CPU():
    def __init__(self,x,y):
        self.x = x
        self.y = y
    
    def run(self):
        RF = RegisterFile()
        DM = DMem(self.y)

        # read instructions from instructions.txt and store in imem.txt by having 8 bits per line
        with open("instructions.txt", "r") as inst:
            with open("imem.txt", "w") as imem:
                for line in inst:
                    imem.write(line[:8])
                    imem.write("\n")
                    imem.write(line[8:16])
                    imem.write("\n")
                    imem.write(line[16:24])
                    imem.write("\n")
                    imem.write(line[24:32])
                    imem.write("\n")
        mmr=MMR()
        IM = IMem(self.x)
        state = stateClass()
        newstate = stateClass()

        state.IF.nop = False # initially only IF stage should execute
        # copy values of state to newstate
        cycle = 1
        newstate = copy.deepcopy(state)
        while True:
            # WB stage
            if not state.WB.nop:
                if state.WB.wrt_enable:
                    RF.writeRF(state.WB.Rd, state.WB.Wrt_data)
                                
            # MEM stage
            if not state.MEM.nop:
                if state.MEM.rd_mem:
                    (status,wrt_data) = DM.readDataMem(state.MEM.ALUresult)
                    if(status == 0):
                        newstate.MEM = state.MEM
                        newstate.MEM.isStalled = True
                        newstate.EX = state.EX
                        newstate.EX.isStalled = True
                        newstate.ID = state.ID
                        newstate.ID.isStalled = True
                        newstate.IF = state.IF
                        newstate.IF.isStalled = True
                        newstate.WB.nop= True
                        printState(newstate, cycle)
                        state = newstate
                        mmr.outputDataMem(cycle)
                        DM.outputDataMem(cycle)  # dump data mem
                        RF.outputRF(cycle)  # dump RF; uncomment to write RF to file
                        cycle += 1            
                        continue
                    else:
                        newstate.MEM.isStalled = False
                        newstate.EX.isStalled = False
                        newstate.ID.isStalled = False
                        newstate.IF.isStalled = False
                        newstate.WB.Wrt_data = wrt_data
                elif state.MEM.wrt_mem:
                    if state.MEM.is_P_type:
                        if state.MEM.alu_op[7:10] == bitarray('111'):
                            mmr.writeMem(ba2int(RF.readRF(state.MEM.Rd)) , ba2int(state.MEM.Imm) + ba2int(RF.readRF(state.MEM.Rs1)) )
                        if state.MEM.alu_op[7:10] == bitarray('000'):
                            mmr.storeMem()
                    else:
                        status = DM.writeDataMem(state.MEM.ALUresult, state.MEM.Store_data)
                        if(status ==0):
                            newstate.MEM = state.MEM
                            newstate.MEM.isStalled = True
                            newstate.EX = state.EX
                            newstate.EX.isStalled = True
                            newstate.ID = state.ID
                            newstate.ID = state.ID
                            newstate.IF = state.IF
                            newstate.IF.isStalled = True
                            newstate.WB.nop= True
                            printState(newstate, cycle)
                            state = newstate
                            mmr.outputDataMem(cycle)
                            DM.outputDataMem(cycle)  # dump data mem
                            RF.outputRF(cycle)  # dump RF; uncomment to write RF to file
                            cycle += 1                      
                            continue
                        if state.WB.nop == False and state.WB.wrt_enable and state.WB.Rd == state.MEM.Rs2:
                            newstate.MEM.isStalled = False
                            newstate.EX.isStalled = False
                            newstate.ID.isStalled = False
                            newstate.IF.isStalled = False
                            state.MEM.Store_data = state.WB.Wrt_data
                            print("MEM-MEM sw forwarding") # probably wont happen in this project
                else: 
                    newstate.WB.Wrt_data = state.MEM.ALUresult
                newstate.WB.Rs1 = state.MEM.Rs1
                newstate.WB.Rs2 = state.MEM.Rs2
                newstate.WB.Rd = state.MEM.Rd
                newstate.WB.wrt_enable = state.MEM.wrt_enable
                newstate.WB.instr = state.MEM.instr
                newstate.WB.is_I_type = newstate.MEM.is_I_type
                newstate.WB.is_R_type = newstate.MEM.is_R_type
                newstate.WB.is_B_type = newstate.MEM.is_B_type
                newstate.WB.is_S_type = newstate.MEM.is_S_type
                newstate.WB.is_L_type = newstate.MEM.is_L_type
                newstate.WB.is_P_type = newstate.MEM.is_P_type
                newstate.WB.pc = state.MEM.pc
                newstate.MEM.isStalled = False
                newstate.EX.isStalled = False
                newstate.ID.isStalled = False
                newstate.IF.isStalled = False

            newstate.WB.nop = state.MEM.nop

            # EX stage
            if not state.EX.nop:

                newstate.MEM.is_I_type = newstate.EX.is_I_type
                newstate.MEM.is_R_type = newstate.EX.is_R_type
                newstate.MEM.is_B_type = newstate.EX.is_B_type
                newstate.MEM.is_S_type = newstate.EX.is_S_type
                newstate.MEM.is_L_type = newstate.EX.is_L_type
                newstate.MEM.is_P_type = newstate.EX.is_P_type
                newstate.MEM.pc = state.EX.pc
                # forwarding/bypassing logic

                if state.MEM.nop == False and state.MEM.wrt_enable and state.MEM.rd_mem == False and state.MEM.wrt_mem == False:
                    if state.EX.is_I_type:
                        if state.EX.Rs1 == state.MEM.Rd:
                            state.EX.Read_data1 = state.MEM.ALUresult
                            # print("EX->EX forwarding I-type")
                    
                    if state.EX.is_R_type:
                        if state.EX.Rs1 == state.MEM.Rd:
                            state.EX.Read_data1 = state.MEM.ALUresult
                            # print("EX->EX forwarding R-type Rs1")
                        if state.EX.Rs2 == state.MEM.Rd:
                            state.EX.Read_data2 = state.MEM.ALUresult
                            # print("EX->EX forwarding R-type Rs2") 
                    
                    if state.EX.is_B_type:
                        if state.EX.Rs1 == state.MEM.Rd:
                            state.EX.Read_data1 = state.MEM.ALUresult
                            # print("EX->EX forwarding B-type Rs1")
                        if state.EX.Rs2 == state.MEM.Rd:
                            state.EX.Read_data2 = state.MEM.ALUresult
                            # print("EX->EX forwarding B-type Rs2")

                    if state.EX.is_S_type:
                        if state.EX.Rs1 == state.MEM.Rd:
                            state.EX.Read_data1 = state.MEM.ALUresult
                            # print("EX->EX forwarding S-type Rs1")
                        if state.EX.Rs2 == state.MEM.Rd:
                            state.EX.Read_data2 = state.MEM.ALUresult
                            # print("EX->EX forwarding S-type Rs2")
                    
                    if state.EX.is_L_type:
                        if state.EX.Rs1 == state.MEM.Rd:
                            state.EX.Read_data1 = state.MEM.ALUresult
                            # print("EX->EX forwarding L-type Rs1")

                elif state.WB.nop == False and state.WB.wrt_enable:
                    if state.EX.is_I_type:
                        if state.EX.Rs1 == state.WB.Rd:
                            state.EX.Read_data1 = state.WB.Wrt_data
                            # print("MEM->EX forwarding I-type")
                    
                    if state.EX.is_R_type:
                        if state.EX.Rs1 == state.WB.Rd:
                            state.EX.Read_data1 = state.WB.Wrt_data
                            # print("MEM->EX forwarding R-type Rs1")
                        if state.EX.Rs2 == state.WB.Rd:
                            state.EX.Read_data2 = state.WB.Wrt_data
                            # print("MEM->EX forwarding R-type Rs2")  

                    if state.EX.is_B_type:
                        if state.EX.Rs1 == state.WB.Rd:
                            state.EX.Read_data1 = state.WB.Wrt_data
                            # print("MEM->EX forwarding B-type Rs1")
                        if state.EX.Rs2 == state.WB.Rd:
                            state.EX.Read_data2 = state.WB.Wrt_data
                            # print("MEM->EX forwarding B-type Rs2")

                    if state.EX.is_S_type:
                        if state.EX.Rs1 == state.WB.Rd:
                            state.EX.Read_data1 = state.WB.Wrt_data
                            # print("MEM->EX forwarding S-type Rs1")
                        if state.EX.Rs2 == state.WB.Rd:
                            state.EX.Read_data2 = state.WB.Wrt_data
                            # print("MEM->EX forwarding S-type Rs2")

                    if state.EX.is_L_type:
                        if state.EX.Rs1 == state.WB.Rd:
                            state.EX.Read_data1 = state.WB.Wrt_data
                            # print("MEM->EX forwarding L-type Rs1")            


                if state.EX.is_I_type:
                    if state.EX.alu_op[7:10] == bitarray('000'):
                        signext=signextend(state.EX.Imm)
                        newstate.MEM.ALUresult = int2ba((ba2int(state.EX.Read_data1) + ba2int(signext)) % (2**32), length=32)
                
                if state.EX.is_R_type:
                    if state.EX.alu_op[7:10] == bitarray('000'):
                        if state.EX.alu_op[0:7] == bitarray('0000000'):
                            newstate.MEM.ALUresult = int2ba((ba2int(state.EX.Read_data1) + ba2int(state.EX.Read_data2)) % (2**32), length=32)
                        elif state.EX.alu_op[0:7] == bitarray('0100000'):
                            newstate.MEM.ALUresult = int2ba((ba2int(state.EX.Read_data1) - ba2int(state.EX.Read_data2)) % (2**32), length=32)
                    #elif for AND and OR
                    elif state.EX.alu_op[7:10] == bitarray('111') or state.EX.alu_op[7:10] == bitarray('110'):
                        if state.EX.alu_op[7:10] == bitarray('111'):
                            newstate.MEM.ALUresult = state.EX.Read_data1 & state.EX.Read_data2
                        elif state.EX.alu_op[7:10] == bitarray('110'):
                            newstate.MEM.ALUresult = state.EX.Read_data1 | state.EX.Read_data2
                    
                    #elif for SLL
                    elif state.EX.alu_op[7:10] == bitarray('001'):
                        newstate.MEM.ALUresult = state.EX.Read_data1 << ba2int(state.EX.Read_data2)
                    
                    #elif for SRA
                    elif state.EX.alu_op[7:10] == bitarray('101'):
                        if state.EX.alu_op[0:7] == bitarray('0100000'):
                            msb=state.EX.Read_data1[0]
                            newbits=state.EX.Read_data1 >> ba2int(state.EX.Read_data2)
                            for i in range(ba2int(state.EX.Read_data2)):
                                newbits[i]=msb
                            newstate.MEM.ALUresult=newbits     

                if state.EX.is_L_type:
                    if state.EX.alu_op[7:10] == bitarray('010'):
                        signext=signextend(state.EX.Imm)
                        newstate.MEM.ALUresult = int2ba((ba2int(state.EX.Read_data1) + ba2int(signext)) % (2**32), length=32)
                
                if state.EX.is_S_type:
                    if state.EX.alu_op[7:10] == bitarray('010'):
                        signext=signextend(state.EX.Imm)
                        newstate.MEM.Store_data = state.EX.Read_data2 # this is the data to be stored in memory (rs2)
                        newstate.MEM.ALUresult = int2ba((ba2int(state.EX.Read_data1) + ba2int(signext)) % (2**32), length=32) # this is the address to store the data at (rs1 + imm-offset)
                
                if state.EX.is_B_type:
                    if state.EX.alu_op[7:10] == bitarray('000'):
                        signext=signextend(state.EX.Imm+bitarray('0')) # add 0 to the end of the immediate to make it 13 bits
                        if state.EX.Read_data1 == state.EX.Read_data2:
                            newstate.MEM.nop = False
                            newstate.EX.nop = True
                            newstate.ID.nop = True
                            newstate.IF.pc= int2ba((ba2int(state.IF.pc) + ba2int(signext) - 8), length=32) # -8 because PC is incremented by 4 when the branch instruc is in IF stage and again by 4 when it is in ID stage. So we need to subtract 2*4=8 to get the correct PC value
                            newstate.IF.nop = False
                            newstate.MEM.rd_mem = state.EX.rd_mem
                            newstate.MEM.wrt_mem = state.EX.wrt_mem
                            newstate.MEM.Rs1 = state.EX.Rs1
                            newstate.MEM.Rs2 = state.EX.Rs2
                            newstate.MEM.Rd = state.EX.Rd
                            newstate.MEM.wrt_enable = state.EX.wrt_enable
                            newstate.MEM.ALUresult = bitarray('00000000000000000000000000000000') # dummy value, not actually used or needed
                            newstate.MEM.instr = state.EX.instr
                            

                            printState(newstate, cycle)
                            state = newstate
                            cycle += 1
                            continue

                if state.EX.is_P_type:
                    newstate.MEM.is_P_type = True
                    newstate.MEM.alu_op = state.EX.alu_op
                    newstate.MEM.Imm = state.EX.Imm
                    
                newstate.MEM.rd_mem = state.EX.rd_mem
                newstate.MEM.wrt_mem = state.EX.wrt_mem
                newstate.MEM.Rs1 = state.EX.Rs1
                newstate.MEM.Rs2 = state.EX.Rs2
                newstate.MEM.Rd = state.EX.Rd
                newstate.MEM.wrt_enable = state.EX.wrt_enable
                newstate.MEM.instr = state.EX.instr
            newstate.MEM.nop = state.EX.nop
            # ID stage
            if not state.ID.nop:
                instruction = state.ID.instr
                opcode = instruction[25:32]
                funct3 = instruction[17:20]
                funct7 = instruction[0:7]
                Rd = instruction[20:25]
                Rs1 = instruction[12:17]
                Rs2 = instruction[7:12]
                Imm = instruction[0:12]
                
                RType = opcode == int2ba(51, 7)
                IType = opcode == int2ba(19, 7)
                BType = opcode == int2ba(99, 7)
                SType = opcode == int2ba(35, 7)
                LType = opcode == int2ba(3, 7)
                PType = opcode == int2ba(55, 7) #int2ba means integer to bitarray of length 7 for number 55

                newstate.EX.is_I_type = IType
                newstate.EX.is_R_type = RType
                newstate.EX.is_B_type = BType
                newstate.EX.is_S_type = SType
                newstate.EX.is_L_type = LType
                newstate.EX.is_P_type = PType
                newstate.EX.instr = state.ID.instr

                                # # code for stalling
                if state.EX.nop==False and state.EX.wrt_enable:

                    if state.EX.is_I_type:
                        if state.EX.Rd == Rs1:
                            newstate.ID = state.ID
                            newstate.EX.nop = True
                            newstate.IF = state.IF
                            newstate.ID.isStalled = True
                            newstate.IF.isStalled = True
                            printState(newstate,cycle)
                            cycle += 1
                            continue

                    elif state.EX.is_R_type:
                        if state.EX.Rd == Rs1 or state.EX.Rd == Rs2:
                            newstate.EX.nop = True
                            newstate.ID = state.ID
                            newstate.IF = state.IF
                            newstate.ID.isStalled = True
                            newstate.IF.isStalled = True

                            printState(newstate,cycle)
                            cycle += 1
                            continue
                    
                    elif state.EX.is_B_type:
                        if state.EX.Rd == Rs1 or state.EX.Rd == Rs2:
                            newstate.EX.nop = True
                            newstate.ID = state.ID
                            newstate.IF = state.IF

                            newstate.ID.isStalled = True
                            newstate.IF.isStalled = True
                            printState(newstate,cycle)
                            cycle += 1
                            continue
                    
                    elif state.EX.is_S_type:
                        if state.EX.Rd == Rs1 or state.EX.Rd == Rs2:
                            newstate.EX.nop = True
                            newstate.ID = state.ID
                            newstate.IF = state.IF

                            newstate.IF.isStalled = True
                            newstate.ID.isStalled = True
                            printState(newstate,cycle)
                            cycle += 1
                            continue

                    elif state.EX.is_L_type:
                        # print("is lytpe")
                        if state.EX.Rd == Rs1:
                            newstate.EX.nop = True
                            newstate.ID = state.ID
                            newstate.IF = state.IF
                            newstate.ID.isStalled = True
                            newstate.IF.isStalled = True
                            printState(newstate,cycle)
                            cycle += 1
                            continue
                newstate.ID.isStalled = False
                newstate.IF.isStalled = False            
                if RType:
                    newstate.EX.alu_op = funct7 + funct3
                    newstate.EX.rd_mem = False
                    newstate.EX.wrt_mem = False
                    newstate.EX.wrt_enable = True
                    newstate.EX.Rd = Rd
                    newstate.EX.Rs1 = Rs1
                    newstate.EX.Rs2 = Rs2
                    newstate.EX.Read_data1 = RF.readRF(Rs1)
                    newstate.EX.Read_data2 = RF.readRF(Rs2)
                elif IType:
                    newstate.EX.alu_op = bitarray('0000000') + funct3
                    newstate.EX.rd_mem = False
                    newstate.EX.wrt_mem = False
                    newstate.EX.wrt_enable = True
                    newstate.EX.Rd = Rd
                    newstate.EX.Rs1 = Rs1
                    #newstate.EX.Rs2 = Rs2
                    newstate.EX.Read_data1 = RF.readRF(Rs1)
                    newstate.EX.Imm = Imm
                elif LType:
                    newstate.EX.alu_op = bitarray('0000000') + funct3
                    newstate.EX.rd_mem = True
                    newstate.EX.wrt_mem = False
                    newstate.EX.wrt_enable = True
                    newstate.EX.Rd = Rd
                    newstate.EX.Rs1 = Rs1
                    #newstate.EX.Rs2 = Rs2
                    newstate.EX.Read_data1 = RF.readRF(Rs1)
                    newstate.EX.Imm = Imm
                elif SType:
                    newstate.EX.alu_op = bitarray('0000000') + funct3
                    newstate.EX.rd_mem = False
                    newstate.EX.wrt_mem = True
                    newstate.EX.wrt_enable = False
                    #newstate.EX.Rd = Rd
                    newstate.EX.Rs1 = Rs1
                    newstate.EX.Rs2 = Rs2
                    newstate.EX.Read_data1 = RF.readRF(Rs1)
                    newstate.EX.Read_data2 = RF.readRF(Rs2)
                    newstate.EX.Imm = instruction[0:7] + instruction[20:25]
                
                # write code for branch
                elif BType:
                    newstate.EX.alu_op = bitarray('0000000') + funct3
                    newstate.EX.rd_mem = False
                    newstate.EX.wrt_mem = False
                    newstate.EX.wrt_enable = False
                    newstate.EX.Rs1 = Rs1
                    newstate.EX.Rs2 = Rs2
                    newstate.EX.Read_data1 = RF.readRF(Rs1)
                    newstate.EX.Read_data2 = RF.readRF(Rs2)
                    newstate.EX.Imm = bitarray(instruction[0]) + bitarray(instruction[24]) + instruction[1:7] + instruction[20:24] # + bitarray('0')

                # peripheral type
                elif PType:
                    newstate.EX.alu_op = bitarray('0000000') + funct3
                    newstate.EX.rd_mem = False
                    newstate.EX.wrt_mem = True
                    newstate.EX.wrt_enable = False
                    newstate.EX.Rd = Rd
                    newstate.EX.Rs1 = Rs1
                    newstate.EX.Read_data1 = RF.readRF(Rs1)
                    newstate.EX.Imm = Imm

                newstate.EX.pc = state.ID.pc
                    # if (state.EX.Rd == Rs1 or stzate.EX.Rd == Rs2):
                    #     newstate.EX.nop = True
                    #     newstate.ID = state.ID
                    #     newstate.IF = state.IF

                    #     printState(newstate,cycle)
                    #     cycle += 1
                    #     print("Stalling")
                    #     continue


            

            newstate.EX.nop = state.ID.nop
            
            # IF stage
            if not state.IF.nop:
                (status,instr) = IM.readInstr(state.IF.pc)
                if(status == 0):     
                    newstate.IF =state.IF
                    newstate.IF.isStalled = True
                    newstate.ID.nop = True
                    printState(newstate, cycle)
                    state = newstate
                    mmr.outputDataMem(cycle)
                    DM.outputDataMem(cycle)  # dump data mem
                    RF.outputRF(cycle)  # dump RF; uncomment to write RF to file
                    cycle += 1
                    continue
                else:                    
                    newstate.IF.isStalled = False
                    newstate.ID.instr = instr
                    newstate.ID.pc = state.IF.pc
                    newstate.IF.pc = int2ba(ba2int(state.IF.pc) + 4, length=32)
                    if newstate.ID.instr.to01() == '11111111111111111111111111111111':
                        newstate.IF.pc=state.IF.pc
                        newstate.ID.nop = True
                        newstate.IF.nop = True
            
            newstate.ID.nop = state.IF.nop
                
            if state.IF.nop and state.ID.nop and state.EX.nop and state.MEM.nop and state.WB.nop:
                printState(newstate,cycle)
                mmr.outputDataMem(cycle)
                DM.outputDataMem(cycle)  # dump data mem
                RF.outputRF(cycle)  # dump RF; uncomment to write RF to file
                break
            printState(newstate, cycle)
            state = newstate
            mmr.outputDataMem(cycle)
            DM.outputDataMem(cycle)  # dump data mem
            RF.outputRF(cycle)  # dump RF; uncomment to write RF to file
            cycle += 1
        self.cycle = cycle
        # print("memory mapped registers = ",'\n',mmr)        


def main():
    x = int(input("Enter the delay of cycles for Imem: "))
    y = int(input("Enter the delay of cycles for Dmem: "))
        # if RFresult.txt exists, remove it
    if os.path.isfile("RFresult.txt"):
        os.remove("RFresult.txt")
    if os.path.isfile("snapshot.txt"):
        os.remove("snapshot.txt")
    if os.path.isfile("dmemresult.txt"):
        os.remove("dmemresult.txt")
        
    cpu = CPU(x,y)
    cpu.run()
    print("machine halted")
    print("total of ", cpu.cycle, " cycles executed") 


if __name__ == "__main__":
    main()








    