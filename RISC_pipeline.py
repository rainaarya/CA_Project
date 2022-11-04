# pip install bitarray 
# bitarray documentation : https://pypi.org/project/bitarray/

import bitarray
import ctypes

MemSize = 1000 # need to change it to 2^32, but for simulation purposes its kept 1000


# all fields are public

class IFClass : #FETCH: fetches instruction and updates PC
    PC = bitarray(32)
    nop = bool(0)

class IDClass : # DECODE: reads from the register RF and generates control signals required in subsequent stages.
    Instr = bitarray(32)
    nop = bool(0)

# class EXClass : # EXECUTE: performs ALU
# convert bitset to bit array
    # bitset<32>  Read_data1;
    # bitset<32>  Read_data2;
    # bitset<16>  Imm;
    # bitset<5>   Rs;
    # bitset<5>   Rt;
    # bitset<5>   Wrt_reg_addr;
    # bool        is_I_type;
    # bool        rd_mem;
    # bool        wrt_mem; 
    # bool        alu_op;     //1 for addu, lw, sw, 0 for subu 
    # bool        wrt_enable;
    # bool        nop;

# class MEMClass : # MEMORY: loads or stores a 32 bit word from data memory
#     bitset<32>  ALUresult;
#     bitset<32>  Store_data;
#     bitset<5>   Rs;
#     bitset<5>   Rt;    
#     bitset<5>   Wrt_reg_addr;
#     bool        rd_mem;
#     bool        wrt_mem; 
#     bool        wrt_enable;    
#     bool        nop;    

# class WBClass : # Writeback: writes back data to the RF.
    # bitset<32>  Wrt_data;
    # bitset<5>   Rs;
    # bitset<5>   Rt;     
    # bitset<5>   Wrt_reg_addr;
    # bool        wrt_enable;
    # bool        nop;   

# class stateClass : # state class of instructions
#  basically here are we creating class objects from
    # IFClass    IF;
    # IDClass    ID;
    # EXClass    EX;
    # MEMClass   MEM;
    # WBClass    WB;

# class RegFile: 
# 	private:
		# vector<bitset<32> >Registers;	
        # So pseudo code for above line of code is:
        # Registers = Empty array of bitarray(32)
    # public: 
        #  Reg_data = bitarray(32);
        # def __init(self):
        # now resize the same Register array in this constructor to 32 coz we have 32 registers ig
			# Registers.resize(32);
            # first element is 0000...0 of 32 bits
			# Registers[0] = bitarray(32);  
        # a function which returns bit array by reading the reg address
        # bitset<32> readRF(bitset<5> Reg_addr)
        # {                         takes register address and converts to unsigned long int and returns it , basically reading data
        #     This below line should actually be typecasting as ctypes.c_ulong(Reg_addr) instead of Reg_addr.ctypes.c_ulong()
        #     So plz change this kind of line everywhere u find below everywhere present
        #     Reg_data = Registers[Reg_addr.ctypes.c_ulong()];
        #     return Reg_data;
        # }

        # a function which writes in a reg addr by reading a reg address
        # void writeRF(bitset<5> Reg_addr, bitset<32> Wrt_reg_data)
        # {
        #     Registers[Reg_addr.ctypes.c_ulong()] = Wrt_reg_data;
        # }
		 
		# void outputRF():
        # file writing stream reg file output
			# ofstream rfout;
            # opening text file
			# rfout.open("RFresult.txt",std::ios_base::app);
            # if succefull in opening do the thing inside the if block
			# if (rfout.is_open()) :
                # write this in file
				# rfout<<"State of RF:\t"<<endl;
			# 	for (int j = 0; j<32; j++)
			# 	{        
			# 		rfout << Registers[j]<<endl;
			# 	}
			# else:
            #   cout<<"Unable to open file";
			# rfout.close();

# class INSMem # instruction memory
#   private:
#         vector<bitset<8> > IMem;
#         Pseudo Code: 
#         IMem = Empty array of bitarray(32)
# 	public:
#         bitset<32> Instruction;
#         def init(self):
#           Resizing to MemSize = 1000 (this var is init in the top)
# 			IMem.resize(MemSize);
#           file stream imem
#           ifstream imem;
# 			line = "";
# 			int i=0;
# 			imem.open("imem.txt");
# 			if (imem.is_open()) :
# 				while (getline(imem,line)) :
# 					IMem[i] = bitset<8>(line);
# 					i++;
#             else:
#               cout<<"Unable to open file";
#           Closing the file
# 			imem.close();                     
#
# a function which returns bit array by reading the reg address
# 		bitset<32> readInstr(bitset<32> ReadAddress) : 
# 			string insmem;
# 			insmem.append(IMem[ReadAddress.ctypes.c_ulong()].to_string());
# 			insmem.append(IMem[ReadAddress.ctypes.c_ulong()+1].to_string());
# 			insmem.append(IMem[ReadAddress.ctypes.c_ulong()+2].to_string());
# 			insmem.append(IMem[ReadAddress.ctypes.c_ulong()+3].to_string());
# 			Instruction = bitset<32>(insmem);		//read instruction memory
# 			return Instruction;
#
#
#
# class DataMem:
#     private:
# 		vector<bitset<8> > DMem;      
#     public:
#         bitset<32> ReadData;
#         def init(self):  
#             DMem.resize(MemSize); 
#             ifstream dmem;
#             string line;
#             int i=0;
#             dmem.open("dmem.txt");
#             if (dmem.is_open())
#                 while (getline(dmem,line))
#                     DMem[i] = bitset<8>(line);
#                     i++;
#             else 
#                 cout<<"Unable to open file";
#             dmem.close();		
#         bitset<32> readDataMem(bitset<32> Address)
#         {	
# 			string datamem;
#             datamem.append(DMem[Address.ctypes.c_ulong()].to_string());
#             datamem.append(DMem[Address.ctypes.c_ulong()+1].to_string());
#             datamem.append(DMem[Address.ctypes.c_ulong()+2].to_string());
#             datamem.append(DMem[Address.ctypes.c_ulong()+3].to_string());
#             ReadData = bitset<32>(datamem);		//read data memory
#             return ReadData;               
# 		}
            
#         void writeDataMem(bitset<32> Address, bitset<32> WriteData)            
#         {
#             DMem[Address.ctypes.c_ulong()] = bitset<8>(WriteData.to_string().substr(0,8));
#             DMem[Address.ctypes.c_ulong()+1] = bitset<8>(WriteData.to_string().substr(8,8));
#             DMem[Address.ctypes.c_ulong()+2] = bitset<8>(WriteData.to_string().substr(16,8));
#             DMem[Address.ctypes.c_ulong()+3] = bitset<8>(WriteData.to_string().substr(24,8));  
#         }   
                     
#         void outputDataMem()
#         {
#             ofstream dmemout;
#             dmemout.open("dmemresult.txt");
#             if (dmemout.is_open())
#             {
#                 for (int j = 0; j< 1000; j++)
#                 {     
#                     dmemout << DMem[j]<<endl;
#                 }
                     
#             }
#             else cout<<"Unable to open file";
#             dmemout.close();               
#         }      
# };

def shiftbits(inst, int start) :
    # params:
#       inst : bitarray(32)
#       start : integer
    return ((inst.ctypes.c_ulong())>>start)
    # return type bit array (32)

def signextend (imm):
    # params:
#       imm: bitarray(16)
    sestring = "";
    if (imm[15]==0):
        sestring = "0000000000000000"+string(imm);    
    else:
        sestring = "1111111111111111"+string(imm);
    # plz check below line typecasting we need to return bit array of size 32 specificaly so we need to tpyecast
    # return (bitarray(sestring) (32 size));

def main():
    myRF = RegFile() 
    myInsMem = INSMem() 
    myDataMem = DataMem()
    state = stateStruct()  
    newState = stateStruct()  
    state.IF.PC=bitarray(32)
    state.IF.nop=0
    # initially only IF stage should execute
    state.ID.nop=state.EX.nop=state.MEM.nop=state.WB.nop=state.EX.alu_op=1
    # //set every value to 0 to avoid garbage
    state.ID.Instr=bitarray(32);
    state.EX.Read_data1=bitarray(32);
    state.EX.Read_data2=bitarray(32);
    state.EX.Rs=bitarray(5)
    state.EX.Imm=bitarray(16);
    state.EX.Rt=bitarray(5)
    state.EX.Wrt_reg_addr=bitarray(5)
    state.EX.is_I_type=0;
    state.EX.rd_mem=0;
    state.EX.wrt_mem=0;
    state.EX.wrt_enable=0;
    state.MEM.ALUresult=bitarray(32);
    state.MEM.Rs=bitarray(5)
    state.MEM.Rt=bitarray(5)
    state.MEM.Store_data=bitarray(32);
    state.MEM.Wrt_reg_addr=bitarray(5)
    state.MEM.rd_mem=0;
    state.MEM.wrt_mem=0;
    state.MEM.wrt_enable= 0;
    state.WB.Rs=bitarray(5)
    state.WB.Rt=bitarray(5)
    state.WB.Wrt_reg_addr=bitarray(5)
    state.WB.Wrt_data=bitarray(32);
    state.WB.wrt_enable=0;

    # //copy values of state to newState
    newState=state;

    # // instruction
    instruction=bitarray(32);
    opcode=bitarray(6);
    funct=bitarray(6);

    # //control signals
    IType=bitarray(1);
    RType=bitarray(1);
    IsBranch=bitarray(1);
 
    # // ALU signals
    signext=bitarray(32);
    
    # // pc signals
    braddr=bitarray(32);

    # //cycle signal
    int cycle=0;
           
    while (True):
        # /*stages will only execute when the nop bit is zero, so therefore we put nop 1 for all except IF stage initially*/
        # /* --------------------- WB stage --------------------- */
        if (state.WB.nop==0) :
            if(state.WB.wrt_enable) :
                # /*Putting result data in destination register*/
                myRF.writeRF(state.WB.Wrt_reg_addr, state.WB.Wrt_data);
        # /* --------------------- MEM stage --------------------- */
        newState.WB.nop=state.MEM.nop;
        if(state.MEM.nop==0):
            if(state.MEM.wrt_mem):
                myDataMem.writeDataMem(state.MEM.ALUresult,state.MEM.Store_data);# //write to dmem
            if(state.MEM.rd_mem):
                newState.WB.Wrt_data=myDataMem.readDataMem(state.MEM.ALUresult); #//read from dmem
            else:
                newState.WB.Wrt_data=state.MEM.ALUresult; #//dmem not involved, value forwarded
            newState.WB.Rs=state.MEM.Rs;
            newState.WB.Rt=state.MEM.Rt;
            newState.WB.Wrt_reg_addr=state.MEM.Wrt_reg_addr;
            newState.WB.wrt_enable=state.MEM.wrt_enable;
        # /* --------------------- EX stage --------------------- */
        newState.MEM.nop=state.EX.nop;
        if(state.EX.nop==0):
            newState.MEM.Store_data = state.EX.Read_data2;
            if(state.EX.is_I_type):
                signext = signextend (state.EX.Imm);
                state.EX.Read_data2=signext;
            if(state.EX.alu_op):
                newState.MEM.ALUresult=bitarray(32) 
                newState.MEM.ALUresult = (state.EX.Read_data1.ctypes.c_ulong() + state.EX.Read_data2.ctypes.c_ulong());
            else:
                newState.MEM.ALUresult=bitarray(32)
                newState.MEM.ALUresult=(state.EX.Read_data1.ctypes.c_ulong() - state.EX.Read_data2.ctypes.c_ulong());
            newState.MEM.rd_mem=state.EX.rd_mem;
            newState.MEM.wrt_mem=state.EX.wrt_mem;
            newState.MEM.Rt=state.EX.Rt;
            newState.MEM.Rs=state.EX.Rs;
            newState.MEM.wrt_enable=state.EX.wrt_enable;
            newState.MEM.Wrt_reg_addr=state.EX.Wrt_reg_addr;
        # /* --------------------- ID stage --------------------- */
        newState.EX.nop=state.ID.nop;
        if(state.ID.nop==0):
            instruction=state.ID.Instr;
            opcode = bitarray(6)
            opcode = (shiftbits(instruction, 26));
            RType = (opcode.ctypes.c_ulong()==0)if 1   else  0 # /*r-type has opcode 000000*/
            IType = (opcode.ctypes.c_ulong()!=0 and opcode.ctypes.c_ulong()!=2)if 1  else 0;
            IsBranch = (opcode.ctypes.c_ulong()==4)if 1  else 0;
            newState.EX.rd_mem = (opcode.ctypes.c_ulong()==35)if 1  else 0;
            newState.EX.wrt_mem = (opcode.ctypes.c_ulong()==43)if 1  else 0;
            newState.EX.wrt_enable = (newState.EX.wrt_mem==1 or IsBranch.ctypes.c_ulong()==1) if 0  else 1; #//shouldn't be either store word or branch
            newState.EX.is_I_type=(IType==1 and IsBranch==0)if 1  else 0; #//to make sure it's not a branch instruction
            funct = bitarray(6)( (shiftbits(instruction, 0)));
            newState.EX.alu_op = (funct.ctypes.c_ulong()==35)if 0  else 1; #/*subu function is 0, hex 23= dec 35*/
            newState.EX.Rs = bitarray<5> (shiftbits(instruction, 21));
            newState.EX.Rt = bitarray<5> (shiftbits(instruction, 16));
            newState.EX.Read_data1=myRF.readRF(newState.EX.Rs);
            newState.EX.Read_data2=myRF.readRF(newState.EX.Rt);
            newState.EX.Wrt_reg_addr =  (newState.EX.is_I_type)if newState.EX.Rt   else  bitarray(5)( (shiftbits(instruction, 11))); #/*if i-type wrreg=reg2, else wrreg is seperate*/
            newState.EX.Imm = bitarray(16)( (shiftbits(instruction, 0)));
            braddr = bitarray(32)(ctypes.c_ulong((state.IF.PC.ctypes.c_ulong() + 4 + str((bitarray(32)(((bitarray(30) ((shiftbits(signext,0)))))+"00"))))));
        # /* --------------------- IF stage --------------------- */
        newState.ID.nop=state.IF.nop;
        if(state.IF.nop==0):
            newState.ID.Instr=myInsMem.readInstr(state.IF.PC);
            newState.IF.PC=state.IF.PC.ctypes.c_ulong()+4;
            if (str(newState.ID.Instr)=="11111111111111111111111111111111"):
                 newState.IF.PC=state.IF.PC;# //PC remains the same//
                 newState.ID.nop=newState.IF.nop=1;
        if (state.IF.nop and state.ID.nop and state.EX.nop and state.MEM.nop and state.WB.nop) :
            break;
        printState(newState, cycle); #//print states after executing cycle 0, cycle 1, cycle 2 ... 
        state = newState; #/*The end of the cycle and updates the current state with the values calculated in this cycle */ 
        cycle+=1;        	
    myRF.outputRF(); #// dump RF;	
	myDataMem.outputDataMem();# // dump data mem