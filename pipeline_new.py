import bitarray
from bitarray import bitarray
from bitarray.util import ba2int, int2ba
import copy

MemSize = 1024

class IFClass:
    def __init__(self):
        self.pc = bitarray(32)
        self.pc.setall(0)
        self.nop = True
    
class IDClass:
    def __init__(self):
        self.instr= bitarray(32)
        self.instr.setall(0)
        self.nop = True

class EXClass:
    def __init__(self):
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
        self.rd_mem = False
        self.wrt_mem = False
        self.alu_op = bitarray(10)
        self.alu_op.setall(0)
        self.wrt_enable = False
        self.nop = True

class MEMClass:
    def __init__(self):
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
    
class WBClass:
    def __init__(self):
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
    
    def readRF(self, Reg_addr):
        self.Reg_data = self.Registers[ba2int(Reg_addr)]
        return self.Reg_data
    
    def writeRF(self, Reg_addr, Wrt_reg_data):
        self.Registers[ba2int(Reg_addr)] = Wrt_reg_data
    
    def outputRF(self):
        with open ("RFresult.txt", "a") as rfout:
            rfout.write("State of RF:\t\n")
            for i in range(32):
                rfout.write(self.Registers[i].to01())
                rfout.write("\n")
    

class IMem:
    def __init__(self):
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
        self.Instruction = bitarray(insmem)
        return self.Instruction


class DMem:
    def __init__(self):
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
        datamem = ""
        datamem += self.DMem[ba2int(Address)].to01()
        datamem += self.DMem[ba2int(Address)+1].to01()
        datamem += self.DMem[ba2int(Address)+2].to01()
        datamem += self.DMem[ba2int(Address)+3].to01()
        self.ReadData = bitarray(datamem)
        return self.ReadData
    
    def writeDataMem(self, Address, WriteData):
        self.DMem[ba2int(Address)] = bitarray(WriteData.to01()[:8])
        self.DMem[ba2int(Address)+1] = bitarray(WriteData.to01()[8:16])
        self.DMem[ba2int(Address)+2] = bitarray(WriteData.to01()[16:24])
        self.DMem[ba2int(Address)+3] = bitarray(WriteData.to01()[24:32])
    
    def outputDataMem(self):
        with open("dmemresult.txt", "w") as dmemout:
            for j in range(MemSize):
                dmemout.write(self.DMem[j].to01())
                dmemout.write("\n")

def printState(state, cycle):
    with open ("snapshot.txt", "a") as snap:
        snap.write("cycle " + str(cycle) + "\t\n")
        # IF stage
        snap.write("IF.PC:\t" + state.IF.pc.to01() + "\t\n")
        snap.write("IF.nop:\t" + str(state.IF.nop) + "\t\n")
        # ID stage
        snap.write("ID.instr:\t" + state.ID.instr.to01() + "\t\n")
        snap.write("ID.nop:\t" + str(state.ID.nop) + "\t\n")

        # EX stage
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
        snap.write("EX.rd_mem:\t" + str(state.EX.rd_mem) + "\t\n")
        snap.write("EX.wrt_mem:\t" + str(state.EX.wrt_mem) + "\t\n")
        snap.write("EX.alu_op:\t" + state.EX.alu_op.to01() + "\t\n")
        snap.write("EX.wrt_enable:\t" + str(state.EX.wrt_enable) + "\t\n")
        snap.write("EX.nop:\t" + str(state.EX.nop) + "\t\n")

        # MEM stage
        snap.write("MEM.ALUresult:\t" + state.MEM.ALUresult.to01() + "\t\n")
        snap.write("MEM.Store_data:\t" + state.MEM.Store_data.to01() + "\t\n")
        snap.write("MEM.Rs2:\t" + state.MEM.Rs2.to01() + "\t\n")
        snap.write("MEM.Rs1:\t" + state.MEM.Rs1.to01() + "\t\n")
        snap.write("MEM.Rd:\t" + state.MEM.Rd.to01() + "\t\n")
        snap.write("MEM.rd_mem:\t" + str(state.MEM.rd_mem) + "\t\n")
        snap.write("MEM.wrt_mem:\t" + str(state.MEM.wrt_mem) + "\t\n")
        snap.write("MEM.wrt_enable:\t" + str(state.MEM.wrt_enable) + "\t\n")
        snap.write("MEM.nop:\t" + str(state.MEM.nop) + "\t\n")

        # WB stage        
        snap.write("WB.Wrt_data:\t" + state.WB.Wrt_data.to01() + "\t\n")
        snap.write("WB.Rs2:\t" + state.WB.Rs2.to01() + "\t\n")
        snap.write("WB.Rs1:\t" + state.WB.Rs1.to01() + "\t\n")
        snap.write("WB.Rd:\t" + state.WB.Rd.to01() + "\t\n")
        snap.write("WB.wrt_enable:\t" + str(state.WB.wrt_enable) + "\t\n")
        snap.write("WB.nop:\t" + str(state.WB.nop) + "\t\n")




def signextend(bits):
    bits=bits.to01()
    if bits[0] == '1':
        bits = '1' * (32 - len(bits)) + bits
    else:
        bits = '0' * (32 - len(bits)) + bits
    return bitarray(bits)

def main():
    RF = RegisterFile()
    DM = DMem()
    IM = IMem()
    state = stateClass()
    newstate = stateClass()

    state.IF.nop = False # initially only IF stage should execute

    # copy values of state to newstate
    newstate = copy.deepcopy(state)

    cycle = 1

    while True:
        # WB stage
        if not state.WB.nop:
            if state.WB.wrt_enable:
                #print("WB stage")
                RF.writeRF(state.WB.Rd, state.WB.Wrt_data)
        
        newstate.WB.nop = state.MEM.nop
        
        # MEM stage
        if not state.MEM.nop:
            if state.MEM.rd_mem:
                newstate.WB.Wrt_data = DM.readDataMem(state.MEM.ALUresult)
            elif state.MEM.wrt_mem:
                DM.writeDataMem(state.MEM.ALUresult, state.MEM.Store_data)
                print("MEM stage", state.MEM.ALUresult, state.MEM.Store_data)
            else:
                newstate.WB.Wrt_data = state.MEM.ALUresult

            newstate.WB.Rs1 = state.MEM.Rs1
            newstate.WB.Rs2 = state.MEM.Rs2
            newstate.WB.Rd = state.MEM.Rd
            newstate.WB.wrt_enable = state.MEM.wrt_enable

        newstate.MEM.nop = state.EX.nop

        # EX stage
        if not state.EX.nop:

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

            
            newstate.MEM.rd_mem = state.EX.rd_mem
            newstate.MEM.wrt_mem = state.EX.wrt_mem
            newstate.MEM.Rs1 = state.EX.Rs1
            newstate.MEM.Rs2 = state.EX.Rs2
            newstate.MEM.Rd = state.EX.Rd
            newstate.MEM.wrt_enable = state.EX.wrt_enable

        newstate.EX.nop = state.ID.nop

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

            newstate.EX.is_I_type = IType
            newstate.EX.is_R_type = RType
            newstate.EX.is_B_type = BType
            newstate.EX.is_S_type = SType
            newstate.EX.is_L_type = LType

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

        newstate.ID.nop = state.IF.nop

        # IF stage
        if not state.IF.nop:
            newstate.ID.instr = IM.readInstr(state.IF.pc)
            newstate.IF.pc = int2ba(ba2int(state.IF.pc) + 4, length=32)
            if newstate.ID.instr.to01() == '11111111111111111111111111111111':
                newstate.IF.pc=state.IF.pc
                newstate.ID.nop = True
                newstate.IF.nop = True
            
        if state.IF.nop and state.ID.nop and state.EX.nop and state.MEM.nop and state.WB.nop:
            printState(newstate,cycle)
            break

        printState(newstate, cycle)
        state = newstate
        cycle += 1

    print("machine halted")
    print("total of ", cycle, " cycles executed")
    RF.outputRF()  # dump RF; uncomment to write RF to file
    DM.outputDataMem()  # dump data mem

if __name__ == "__main__":
    main()








    