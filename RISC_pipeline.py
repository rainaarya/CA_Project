# pip install bitarray
# bitarray documentation : https://pypi.org/project/bitarray/
import ctypes

import bitarray
from bitarray import bitarray
from bitarray.util import ba2int
import math
import numpy as np

class IFClass:  # FETCH: fetches instruction and updates PC
    PC = bitarray(32)
    nop = bool(0)

    def __repr__(self):
        print("PC: ", self.PC, "nop: ", self.nop)

class IDClass:  # DECODE: reads from the register RF and generates control signals required in subsequent stages.
    Instr = bitarray(32)
    nop = bool(0)
    def __repr__(self):
        print("Instr: ", self.Instr, "nop: ", self.nop)

class EXClass:  # EXECUTE: performs ALU
    # convert bitset to bit array
    Read_data1 = bitarray(32)
    Read_data2 = bitarray(32)
    # bitset<16>  Imm
    Imm = bitarray(16)
    # bitset<5>   Rs
    Rs = bitarray(5)
    # bitset<5>   Rt
    Rt = bitarray(5)
    # bitset<5>   Wrt_reg_addr
    Wrt_reg_addr = bitarray(5)
    # bool        is_I_type
    is_I_type = bool(0)
    # bool        rd_mem
    rd_mem = bool(0)
    # bool        wrt_mem
    wrt_mem = bool(0)
    # bool        alu_op      //1 for addu, lw, sw, 0 for subu
    alu_op = bool(1)
    # bool        wrt_enable
    wrt_enable = bool(0)
    # bool        nop
    nop = bool(0)

    def __repr__(self):
        print("Read_data1: ", self.Read_data1, "Read_data2: ", self.Read_data2, "Imm: ", self.Imm, "Rs: ", self.Rs,"Rt: ", self.Rt, "Wrt_reg_addr: ", self.Wrt_reg_addr, "is_I_type: ", self.is_I_type, "rd_mem: ", self.rd_mem, "wrt_mem: ", self.wrt_mem, "alu_op: ", self.alu_op, "wrt_enable: ", self.wrt_enable, "nop: ", self.nop)

class MEMClass:  # MEMORY: loads or stores a 32 bit word from data memory
    # bitset<32>  ALUresult
    ALUresult = bitarray(32)
    # bitset<32>  Store_data
    Store_data = bitarray(32)
    # bitset<5>   Rs
    Rs = bitarray(5)
    # bitset<5>   Rt
    Rt = bitarray(5)
    # bitset<5>   Wrt_reg_addr
    Wrt_reg_addr = bitarray(5)
    # bool        rd_mem
    rd_mem = bool(0)
    # bool        wrt_mem
    wrt_mem = bool(0)
    # bool        wrt_enable
    wrt_enable = bool(0)
    # bool        nop
    nop = bool(0)

    def __repr__(self):
        print("ALUresult: ", self.ALUresult, "Store_data: ", self.Store_data, "Rs: ", self.Rs, "Rt: ", self.Rt, "Wrt_reg_addr: ", self.Wrt_reg_addr, "rd_mem: ", self.rd_mem, "wrt_mem: ", self.wrt_mem, "wrt_enable: ", self.wrt_enable, "nop: ", self.nop)

class WBClass:  # Writeback: writes back data to the RF.
    # bitset<32>  Wrt_data
    Wrt_data = bitarray(32)
    # bitset<5>   Rs
    Rs = bitarray(5)
    # bitset<5>   Rt
    Rt = bitarray(5)
    # bitset<5>   Wrt_reg_addr
    Wrt_reg_addr = bitarray(5)
    # bool        wrt_enable
    wrt_enable = bool(0)
    # bool        nop
    nop = bool(0)

    def __repr__(self):
        print("Wrt_data: ", self.Wrt_data, "Rs: ", self.Rs, "Rt: ", self.Rt, "Wrt_reg_addr: ", self.Wrt_reg_addr, "wrt_enable: ", self.wrt_enable, "nop: ", self.nop)

class stateClass:  # state class of instructions
    #  basically here are we creating class objects from
    # IFClass    IF
    IF = IFClass()
    # IDClass    ID
    ID = IDClass()
    # EXClass    EX
    EX = EXClass()
    # MEMClass   MEM
    MEM = MEMClass()
    # WBClass    WB
    WB = WBClass()

class RegFile:
    # 	private:
    # vector<bitset<32> >Registers
    Reg_data = bitarray(32)
    __Registers = [bitarray(32)]

    # 	public:
    # So pseudocode for above line of code is:
    # Registers = Empty array of bitarray(32)
    # public:
    def __init__(self):
        self.__Registers = self.__Registers * 32
        self.__Registers[0].setall(0)

    # now resize the same Register array in this constructor to 32 coz we have 32 registers ig
    # Registers.resize(32)
    # first element is 0000...0 of 32 bits
    # Registers[0] = bitarray(32)
    # a function which returns bit array by reading the reg address

    def readRF(self, reg_addr):
        print(ba2int(reg_addr))
        if(ba2int(reg_addr)==0):
            return  self.__Registers[0]
        elif (ba2int(reg_addr)==1):
            return  self.__Registers[1]
        Reg_data = self.__Registers[int(math.log(2,ba2int(reg_addr)))]
        return Reg_data

    # bitset<32> readRF(bitset<5> Reg_addr)
    # {                         takes register address and converts to unsigned long int and returns it , basically reading data
    #     This below line should actually be typecasting as ctypes.c_ulong(Reg_addr) instead of Reg_addr.ctypes.c_ulong()
    #     So plz change this kind of line everywhere u find below everywhere present
    #     Reg_data = Registers[Reg_addr.ctypes.c_ulong()]
    #     return Reg_data
    # }

    # a function which writes in a reg addr by reading a reg address
    # void writeRF(bitset<5> Reg_addr, bitset<32> Wrt_reg_data)
    # {
    #     Registers[Reg_addr.ctypes.c_ulong()] = Wrt_reg_data
    # }

    def writeRF(self, reg_addr, wrt_reg_data):
        self.__Registers[ba2int(reg_addr)] = wrt_reg_data

    # void outputRF():
    # file writing stream reg file output
    # ofstream rfout
    # opening text file
    # rfout.open("RFresult.txt",std::ios_base::app)
    # if succefull in opening do the thing inside the if block
    # if (rfout.is_open()) :
    # write this in file
    # rfout<<"State of RF:\t"<<endl
    # 	for (int j = 0  j<32  j++)
    # 	{
    # 		rfout << Registers[j]<<endl
    # 	}
    # else:
    #   cout<<"Unable to open file"
    # rfout.close()

    def outputRF(self):
        while True:
            try:
                rfout = open("RFresult.txt", 'a+')
                rfout.write("State of RF:\t" + "\n")
                for j in range(32):
                    rfout.write(str(self.__Registers[j]) + "\n")
                rfout.close()
                break
            except IOError:
                input("Could not open file!  Press Enter to retry.")


class INSMem:
    __IMem = [bitarray(8)]
    Instruction = bitarray(32)

    def __init__(self):
        self.__IMem = self.__IMem * 1000000000
        line = ""
        i = 0
        while True:
            try:
                imem = open("imem.txt", 'r')

                # 			if (imem.is_open()) :
                # 				while (getline(imem,line)) :
                # 					IMem[i] = bitset<8>(line)
                # 					i++
                #             else:
                #               cout<<"Unable to open file"
                #           Closing the file
                # 			imem.close()

                for line in imem:
                    self.__IMem[i] = bitarray(line)
                    i = i + 1
                imem.close()
                break
            except IOError:
                input("Could not open file! Press Enter to retry.")

    #
    # a function which returns bit array by reading the reg address
    # 		bitset<32> readInstr(bitset<32> ReadAddress) {
    # 			string insmem
    # 			insmem.append(IMem[ReadAddress.ctypes.c_ulong()].to_string())
    # 			insmem.append(IMem[ReadAddress.ctypes.c_ulong()+1].to_string())
    # 			insmem.append(IMem[ReadAddress.ctypes.c_ulong()+2].to_string())
    # 			insmem.append(IMem[ReadAddress.ctypes.c_ulong()+3].to_string())
    # 			Instruction = bitset<32>(insmem) 		//read instruction memory
    # 			return Instruction
    #       }
    #
    def readInstr(self, read_address):
        insmem = "".join(((self.__IMem[ba2int(read_address)].to01()), (self.__IMem[ba2int(read_address) + 1].to01()),
                          (self.__IMem[ba2int(read_address) + 2].to01()),
                          (self.__IMem[ba2int(read_address) + 3].to01())))
        self.Instruction = bitarray(insmem)
        return self.Instruction


class DataMem:
    #     private:
    # 		vector<bitset<8> > DMem
    __DMem = [bitarray(8)]
    #     public:
    #         bitset<32> ReadData
    ReadData = bitarray(32)

    #         def init(self):
    def __init__(self):
        self.__DMem = self.__DMem * 1000000000
        line = ""
        i = 0
        while True:
            try:
                dmem = open("dmem.txt", 'r')
                for line in dmem:
                    self.__DMem[i] = bitarray(line)
                    i = i + 1
                dmem.close()
                break
            except IOError:
                input("Could not open file! Press Enter to retry.")

    #             DMem.resize(MemSize)
    #             ifstream dmem
    #             string line
    #             int i=0
    #             dmem.open("dmem.txt")
    #             if (dmem.is_open())
    #                 while (getline(dmem,line))
    #                     DMem[i] = bitset<8>(line)
    #                     i++
    #             else
    #                 cout<<"Unable to open file"
    #             dmem.close()

    def readDataMem(self, address):
        datamem = "".join(((self.__DMem[int(math.log(ba2int(address)))].to01()), (self.__DMem[int(math.log(ba2int(address))) + 1].to01()),
                           (self.__DMem[int(math.log(ba2int(address))) + 2].to01()), (self.__DMem[int(math.log(ba2int(address))) + 3].to01())))
        self.ReadData = bitarray(datamem)
        return self.ReadData

    #         bitset<32> readDataMem(bitset<32> Address)
    #         {
    # 			string datamem
    #             datamem.append(DMem[Address.ctypes.c_ulong()].to_string())
    #             datamem.append(DMem[Address.ctypes.c_ulong()+1].to_string())
    #             datamem.append(DMem[Address.ctypes.c_ulong()+2].to_string())
    #             datamem.append(DMem[Address.ctypes.c_ulong()+3].to_string())
    #             ReadData = bitset<32>(datamem) 		//read data memory
    #             return ReadData
    # 		}

    #         void writeDataMem(bitset<32> Address, bitset<32> WriteData)
    #         {
    #             DMem[Address.ctypes.c_ulong()] = bitset<8>(WriteData.to_string().substr(0,8))
    #             DMem[Address.ctypes.c_ulong()+1] = bitset<8>(WriteData.to_string().substr(8,8))
    #             DMem[Address.ctypes.c_ulong()+2] = bitset<8>(WriteData.to_string().substr(16,8))
    #             DMem[Address.ctypes.c_ulong()+3] = bitset<8>(WriteData.to_string().substr(24,8))
    #         }
    def writeDataMem(self, address, write_data):
        self.__DMem[ba2int(address)] = bitarray(write_data.to01()[0:8])
        self.__DMem[ba2int(address) + 1] = bitarray(write_data.to01()[8:16])
        self.__DMem[ba2int(address) + 2] = bitarray(write_data.to01()[16:24])
        self.__DMem[ba2int(address) + 3] = bitarray(write_data.to01()[24:32])

    #         void outputDataMem()
    #         {
    #             ofstream dmemout
    #             dmemout.open("dmemresult.txt")
    #             if (dmemout.is_open())
    #             {
    #                 for (int j = 0  j< 1000  j++)
    #                 {
    #                     dmemout << DMem[j]<<endl
    #                 }

    #             }
    #             else cout<<"Unable to open file"
    #             dmemout.close()
    #         }
    def outputDataMem(self):
        while True:
            try:
                dmemout = open("dmemresult.txt", 'w')
                for j in range(0, 1000):
                    dmemout.write(self.__DMem[j].to01() + "\n")
                dmemout.close()
                break
            except IOError:
                input("Could not open file! Press Enter to retry.")


def bitarray_add(size, a, b):
    return bitarray(str(bin((ctypes.c_ulong(ba2int(a) + ba2int(b))).value)[2:]).zfill(size))


def bitarray_sub(size, a, b):
    return bitarray(str(bin((ctypes.c_ulong(ba2int(a) - ba2int(b))).value)[2:]).zfill(size))


def printState(state, cycle):
    while True:
        try:
            printstate = open("stateresult.txt", "a+")
            # print(state.IF)
            # print(state.ID)
            # print(state.EX)
            # print(state.MEM)
            # print(state.WB)
            printstate.write("State after executing cycle:\t" + str(cycle) + "\n")

            printstate.write("IF.PC:\t" + str(ba2int(state.IF.PC)) + "\n")

            printstate.write("IF.nop:\t" + str(state.IF.nop) + "\n")

            # printstate<<"ID.Instr:\t"<<state.ID.Instr<<endl  in python
            printstate.write("ID.Instr:\t" + str(state.ID.Instr) + "\n")

            # printstate<<"ID.nop:\t"<<state.ID.nop<<endl  in python
            printstate.write("ID.nop:\t" + str(state.ID.nop) + "\n")

            # printstate<<"EX.Read_data1:\t"<<state.EX.Read_data1<<endl  in py
            printstate.write("EX.Read_data1:\t" + str(state.EX.Read_data1) + "\n")

            # printstate<<"EX.Read_data2:\t"<<state.EX.Read_data2<<endl  in py
            printstate.write("EX.Read_data2:\t" + str(state.EX.Read_data2.to01) + "\n")

            # printstate<<"EX.Imm:\t"<<state.EX.Imm<<endl  in py
            printstate.write("EX.Imm:\t" + str(state.EX.Imm.to01) + "\n")

            # printstate<<"EX.Rs:\t"<<state.EX.Rs<<endl  in py
            printstate.write("EX.Rs:\t" + str(state.EX.Rs) + "\n")

            # printstate<<"EX.Rt:\t"<<state.EX.Rt<<endl  in py
            printstate.write("EX.Rt:\t" + str(state.EX.Rt) + "\n")

            # printstate<<"EX.Wrt_reg_addr:\t"<<state.EX.Wrt_reg_addr<<endl  in py
            printstate.write("EX.Wrt_reg_addr:\t" + str(state.EX.Wrt_reg_addr) + "\n")

            # printstate<<"EX.is_I_type:\t"<<state.EX.is_I_type<<endl   in py
            printstate.write("EX.is_I_type:\t" + str(state.EX.is_I_type) + "\n")

            # printstate<<"EX.rd_mem:\t"<<state.EX.rd_mem<<endl
            printstate.write("EX.rd_mem:\t" + str(state.EX.rd_mem) + "\n")

            # printstate<<"EX.wrt_mem:\t"<<state.EX.wrt_mem<<endl  in py
            printstate.write("EX.wrt_mem:\t" + str(state.EX.wrt_mem) + "\n")

            # printstate<<"EX.alu_op:\t"<<state.EX.alu_op<<endl  in py
            printstate.write("EX.alu_op:\t" + str(state.EX.alu_op) + "\n")

            # printstate<<"EX.wrt_enable:\t"<<state.EX.wrt_enable<<endl  in py
            printstate.write("EX.wrt_enable:\t" + str(state.EX.wrt_enable) + "\n")

            # printstate<<"EX.nop:\t"<<state.EX.nop<<endl  in py
            printstate.write("EX.nop:\t" + str(state.EX.nop) + "\n")

            # printstate<<"MEM.ALUresult:\t"<<state.MEM.ALUresult<<endl
            printstate.write("MEM.ALUresult:\t" + str(state.MEM.ALUresult) + "\n")

            # printstate<<"MEM.Store_data:\t"<<state.MEM.Store_data<<endl
            printstate.write("MEM.Store_data:\t" + str(state.MEM.Store_data) + "\n")

            # printstate<<"MEM.Rs:\t"<<state.MEM.Rs<<endl
            printstate.write("MEM.Rs:\t" + str(state.MEM.Rs) + "\n")

            # printstate<<"MEM.Rt:\t"<<state.MEM.Rt<<endl
            printstate.write("MEM.Rt:\t" + str(state.MEM.Rt) + "\n")

            # printstate<<"MEM.Wrt_reg_addr:\t"<<state.MEM.Wrt_reg_addr<<endl
            printstate.write("MEM.Wrt_reg_addr:\t" + str(state.MEM.Wrt_reg_addr) + "\n")

            # printstate<<"MEM.rd_mem:\t"<<state.MEM.rd_mem<<endl
            printstate.write("MEM.rd_mem:\t" + str(state.MEM.rd_mem) + "\n")

            # printstate<<"MEM.wrt_mem:\t"<<state.MEM.wrt_mem<<endl
            printstate.write("MEM.wrt_mem:\t" + str(state.MEM.wrt_mem) + "\n")

            # printstate<<"MEM.wrt_enable:\t"<<state.MEM.wrt_enable<<endl
            printstate.write("MEM.wrt_enable:\t" + str(state.MEM.wrt_enable) + "\n")

            # printstate<<"MEM.nop:\t"<<state.MEM.nop<<endl
            printstate.write("MEM.nop:\t" + str(state.MEM.nop) + "\n")

            # printstate<<"WB.Wrt_data:\t"<<state.WB.Wrt_data<<endl
            printstate.write("WB.Wrt_data:\t" + str(state.WB.Wrt_data) + "\n")

            # printstate<<"WB.Rs:\t"<<state.WB.Rs<<endl
            printstate.write("WB.Rs:\t" + str(state.WB.Rs) + "\n")

            # printstate<<"WB.Rt:\t"<<state.WB.Rt<<endl
            printstate.write("WB.Rt:\t" + str(state.WB.Rt) + "\n")

            # printstate<<"WB.Wrt_reg_addr:\t"<<state.WB.Wrt_reg_addr<<endl
            printstate.write("WB.Wrt_reg_addr:\t" + str(state.WB.Wrt_reg_addr) + "\n")

            # printstate<<"WB.wrt_enable:\t"<<state.WB.wrt_enable<<endl
            printstate.write("WB.wrt_enable:\t" + str(state.WB.wrt_enable) + "\n")

            # printstate<<"WB.nop:\t"<<state.WB.nop<<endl
            printstate.write("WB.nop:\t" + str(state.WB.nop) + "\n")

            printstate.close()
            break
        except IOError:
            input("Could not open file! Press Enter to retry.")


def shiftbits(inst, start):
    inst_int = ba2int(inst)
    return ((str(bin(ctypes.c_ulong(inst_int >> start).value))[2:]).zfill(32))[:32]


# return type bit array (32)

def signextend(imm):
    # params:
    #       imm: bitarray(16)
    sestring = ""
    if imm[15] == 0:
        sestring = "0000000000000000" + imm.to01()
    else:
        sestring = "1111111111111111" + imm.to01()
    return bitarray(sestring)
    # plz check below line typecasting we need to return bit array of size 32 specificaly so we need to tpyecast
    # return (bitarray(sestring) (32 size)) 


def main():
    myRF = RegFile()
    myInsMem = INSMem()
    myDataMem = DataMem()
    state = stateClass()
    newState = stateClass()
    state.IF.PC = bitarray(32)
    state.IF.nop = 0
    # initially only IF stage should execute
    state.ID.nop = state.EX.nop = state.MEM.nop = state.WB.nop = state.EX.alu_op = 1
    # //set every value to 0 to avoid garbage
    state.ID.Instr = bitarray(32)
    state.EX.Read_data1 = bitarray(32)
    state.EX.Read_data2 = bitarray(32)
    state.EX.Rs = bitarray(5)
    state.EX.Imm = bitarray(16)
    state.EX.Rt = bitarray(5)
    state.EX.Wrt_reg_addr = bitarray(5)
    state.EX.is_I_type = 0
    state.EX.rd_mem = 0
    state.EX.wrt_mem = 0
    state.EX.wrt_enable = 0
    state.MEM.ALUresult = bitarray(32)
    state.MEM.Rs = bitarray(5)
    state.MEM.Rt = bitarray(5)
    state.MEM.Store_data = bitarray(32)
    state.MEM.Wrt_reg_addr = bitarray(5)
    state.MEM.rd_mem = 0
    state.MEM.wrt_mem = 0
    state.MEM.wrt_enable = 0
    state.WB.Rs = bitarray(5)
    state.WB.Rt = bitarray(5)
    state.WB.Wrt_reg_addr = bitarray(5)
    state.WB.Wrt_data = bitarray(32)
    state.WB.wrt_enable = 0

    # //copy values of state to newState
    newState = state

    # // instruction
    instruction = bitarray(32)
    opcode = bitarray(6)
    funct = bitarray(6)

    # //control signals
    IType = bitarray(1)
    RType = bitarray(1)
    IsBranch = bitarray(1)

    # // ALU signals
    signext = bitarray(32)

    # // pc signals
    braddr = bitarray(32)

    # //cycle signal
    cycle = 0

    while (True):
        if(ba2int(state.IF.PC)==12):
            print( 12)
        # /*stages will only execute when the nop bit is zero, so therefore we put nop 1 for all except IF stage initially*/
        # /* --------------------- WB stage --------------------- */
        if (state.WB.nop == int(0)):
            if (state.WB.wrt_enable):
                # /*Putting result data in destination register*/
                myRF.writeRF(state.WB.Wrt_reg_addr, state.WB.Wrt_data)
                # /* --------------------- MEM stage --------------------- */
        newState.WB.nop = state.MEM.nop
        if (state.MEM.nop == int(0)):
            if (state.MEM.wrt_mem):
                myDataMem.writeDataMem(state.MEM.ALUresult, state.MEM.Store_data)  # //write to dmem
            if (state.MEM.rd_mem):
                newState.WB.Wrt_data = myDataMem.readDataMem(state.MEM.ALUresult)  # //read from dmem
            else:
                newState.WB.Wrt_data = state.MEM.ALUresult  # //dmem not involved, value forwarded
            newState.WB.Rs = state.MEM.Rs
            newState.WB.Rt = state.MEM.Rt
            newState.WB.Wrt_reg_addr = state.MEM.Wrt_reg_addr
            newState.WB.wrt_enable = state.MEM.wrt_enable
            # /* --------------------- EX stage --------------------- */
        newState.MEM.nop = state.EX.nop
        if (state.EX.nop == int(0)):
            newState.MEM.Store_data = state.EX.Read_data2
            if (state.EX.is_I_type):
                signext = signextend(state.EX.Imm)
                state.EX.Read_data2 = signext
            if (state.EX.alu_op):
                newState.MEM.ALUresult = bitarray("00000000000000000000000000000000")
                newState.MEM.ALUresult = bitarray_add(32, state.EX.Read_data1, state.EX.Read_data2)
            else:
                newState.MEM.ALUresult = bitarray(32)
                newState.MEM.ALUresult = bitarray_sub(32, state.EX.Read_data1,state.EX.Read_data2)
            newState.MEM.rd_mem = state.EX.rd_mem
            newState.MEM.wrt_mem = state.EX.wrt_mem
            newState.MEM.Rt = state.EX.Rt
            newState.MEM.Rs = state.EX.Rs
            newState.MEM.wrt_enable = state.EX.wrt_enable
            newState.MEM.Wrt_reg_addr = state.EX.Wrt_reg_addr
            # /* --------------------- ID stage --------------------- */
        newState.EX.nop = state.ID.nop
        if state.ID.nop == int(0):
            instruction = state.ID.Instr
            opcode = bitarray(6)
            opcode = bitarray(shiftbits(instruction, 26))
            if(ctypes.c_ulong(ba2int(opcode)).value == int(0)):
                RType = 1
            else:
                Rtype= 0
            if(ctypes.c_ulong(ba2int(opcode)).value != int(0) and ctypes.c_ulong(ba2int(opcode)).value != 2):
                IType = int(1)
            else:
                IType = int(0)
            if(ctypes.c_ulong(ba2int(opcode)).value == 4):
                IsBranch = int(1)
            else:
                IsBranch = int(0)

            if(ctypes.c_ulong(ba2int(opcode)).value == 35):
                newState.EX.rd_mem = int(1)
            else:
                newState.EX.rd_mem = int(0)

            if(ctypes.c_ulong(ba2int(opcode)).value == 43):
                newState.EX.wrt_mem = int(1)
            else:
                newState.EX.wrt_mem= int(0)
            
            if(newState.EX.wrt_mem == int(1) or ctypes.c_ulong(IsBranch).value == int(1)):
                newState.EX.wrt_enable = int(1)
            else:
                newState.EX.wrt_enable= int(0)

            if(IType == int(1) and IsBranch == int(0)):
                newState.EX.is_I_type = int(1)
            else:
                newState.EX.is_I_type= int(0)

            funct = bitarray((shiftbits(instruction, int(0)))) [:6]

            if(ctypes.c_ulong(ba2int(funct)).value == 35):
                newState.EX.alu_op = int(1)
            else:
                newState.EX.alu_op= int(0)

            newState.EX.Rs = bitarray(shiftbits(instruction, 21))
            newState.EX.Rt = bitarray(shiftbits(instruction, 16))
            newState.EX.Read_data1 = myRF.readRF(newState.EX.Rs)
            newState.EX.Read_data2 = myRF.readRF(newState.EX.Rt)
            if(newState.EX.is_I_type):
                newState.EX.Wrt_reg_addr =  newState.EX.Rt
            else:
                newState.EX.Wrt_reg_addr =  bitarray((shiftbits(instruction, 11)))
            # /*if i-type wrreg=reg2, else wrreg is seperate*/
            newState.EX.Imm = bitarray((shiftbits(instruction, int(0))))
            # braddr = bitarray(str(ctypes.c_ulong((ctypes.c_ulong(ba2int(state.IF.PC)).value))) + "4" + str((bitarray(((bitarray((shiftbits(signext, int(0)))))) + "00")
            # braddr = bitarray(ctypes.c_ulong(ba2int(state.IF.PC)).value + 4 + ctypes.c_ulong(ba2int(bitarray(str(ba2int(bitarray(shiftbits(signext,int(0)))))+"00"))).value) ISKO BAADMEIN DEKHNA HAI
            # /* --------------------- IF stage --------------------- */
        newState.ID.nop = state.IF.nop
        if state.IF.nop == int(0):
            newState.ID.Instr = myInsMem.readInstr(state.IF.PC)
            newState.IF.PC = bitarray((str(bin(ba2int(state.IF.PC) + 4))[2:]).zfill(32))
            if str(newState.ID.Instr) == "11111111111111111111111111111111":
                newState.IF.PC = state.IF.PC  # //PC remains the same//
                newState.ID.nop = newState.IF.nop = 1
        if state.IF.nop and state.ID.nop and state.EX.nop and state.MEM.nop and state.WB.nop:
            break
        printState(newState, cycle)  # //print states after executing cycle 0, cycle 1, cycle 2 ...
        state = newState  # /*The end of the cycle and updates the current state with the values calculated in this cycle */
        cycle += 1
    myRF.outputRF()  # // dump RF
    myDataMem.outputDataMem()  # // dump data mem

if __name__ == '__main__':
    main()