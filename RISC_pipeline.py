# pip install bitarray 
# bitarray documentation : https://pypi.org/project/bitarray/

import bitarray

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
			# Registers[0] = bitset<32> (0);  
        # a function which returns bit array by reading the reg address
        # bitset<32> readRF(bitset<5> Reg_addr)
        # {                         takes register address and converts to unsigned long int and returns it , basically reading data
        #     Reg_data = Registers[Reg_addr.to_ulong()];
        #     return Reg_data;
        # }

        # a function which writes in a reg addr by reading a reg address
        # void writeRF(bitset<5> Reg_addr, bitset<32> Wrt_reg_data)
        # {
        #     Registers[Reg_addr.to_ulong()] = Wrt_reg_data;
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
# 			insmem.append(IMem[ReadAddress.to_ulong()].to_string());
# 			insmem.append(IMem[ReadAddress.to_ulong()+1].to_string());
# 			insmem.append(IMem[ReadAddress.to_ulong()+2].to_string());
# 			insmem.append(IMem[ReadAddress.to_ulong()+3].to_string());
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
#             datamem.append(DMem[Address.to_ulong()].to_string());
#             datamem.append(DMem[Address.to_ulong()+1].to_string());
#             datamem.append(DMem[Address.to_ulong()+2].to_string());
#             datamem.append(DMem[Address.to_ulong()+3].to_string());
#             ReadData = bitset<32>(datamem);		//read data memory
#             return ReadData;               
# 		}
            
#         void writeDataMem(bitset<32> Address, bitset<32> WriteData)            
#         {
#             DMem[Address.to_ulong()] = bitset<8>(WriteData.to_string().substr(0,8));
#             DMem[Address.to_ulong()+1] = bitset<8>(WriteData.to_string().substr(8,8));
#             DMem[Address.to_ulong()+2] = bitset<8>(WriteData.to_string().substr(16,8));
#             DMem[Address.to_ulong()+3] = bitset<8>(WriteData.to_string().substr(24,8));  
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