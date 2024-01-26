"""
This class performs all the operations that are required. 
It has functions for all the 21 instructions present in the
IAS and the instructions that we have made by ourselves,
namely increment, decrement, input, display, and arithmethic right shift.

@author Aryan Bansal and Abhirath Adamane
@version 1.0
@data 13/01/24
"""

from Memory import Memory
from Utilities import *
from ProcessorSupport import *

class Control:
    """
    Defines the controller class in order to decide what to do in execute phase.
    """
    
    def __init__(self, registers:HoldRegisters, memory:Memory, writeRegisters, writeMemory):
        """
        @param registers : the register object
        @param memory : the memory object
        @param writeRegisters : write Registers method to print registers to output file.
        @param writeMemory : write Memory method to print memory to output file. 
        """
        
        checkType([(registers, HoldRegisters), (memory, Memory)])
        
        self.__registers = registers
        self.__memory = memory
        self.__writeRegisters = writeRegisters
        self.__writeMemory = writeMemory

        self.__functions = {
            Opcode.INC               : self.__INC,
            Opcode.DEC               : self.__DEC,
            Opcode.INP_MX            : self.__INP_MX,
            Opcode.DISP_MX           : self.__DISP_MX,
            Opcode.LOAD_MQ            : self.__LOAD_MQ,
            Opcode.LOAD_MQ_MX         : self.__LOAD_MQ_MX,
            Opcode.STOR_MX            : self.__STOR_MX,
            Opcode.LOAD_MX            : self.__LOAD_MX,
            Opcode.LOAD_NEG_MX        : self.__LOAD_NEG_MX,
            Opcode.LOAD_ABS_MX        : self.__LOAD_ABS_MX,
            Opcode.LOAD_NEG_ABS_MX    : self.__LOAD_NEG_ABS_MX,
            Opcode.JUMP_MX_0_19       : self.__JUMP_MX_0_19,
            Opcode.JUMP_MX_20_39      : self.__JUMP_MX_20_39,
            Opcode.JUMP_PLUS_MX_0_19  : self.__JUMP_PLUS_MX_0_19,
            Opcode.JUMP_PLUS_MX_20_39 : self.__JUMP_PLUS_MX_20_39,
            Opcode.ADD_MX             : self.__ADD_MX,
            Opcode.ADD_ABS_MX         : self.__ADD_ABS_MX,
            Opcode.SUB_MX             : self.__SUB_MX,
            Opcode.SUB_ABS_MX         : self.__SUB_ABS_MX,
            Opcode.MUL_MX             : self.__MUL_MX,
            Opcode.DIV_MX             : self.__DIV_MX,
            Opcode.LSH                : self.__LSH,
            Opcode.RSH                : self.__RSH,
            Opcode.ARSH                : self.__ARSH,
            Opcode.STOR_MX_8_19       : self.__STOR_MX_8_19,
            Opcode.STOR_MX_28_39      : self.__STOR_MX_28_39,
            Opcode.HALT               : self.__HALT,
            Opcode.NOP                : self.__NOP
            }

    def execute(self, instruction:str, code:Opcode):
        """
        Excecutes the instruction based on the opcode given.
        @param instruction : the instruction performed
        @param code : the opcode
        """
        
        checkType([(instruction, str), (code, Opcode)])
        
        if(self.__functions.get(code) != None):
            return self.__functions.get(code)()

        printErrorAndExit("No such opcode : ", code.name)
    
    def __check(self, status:Status):
        """
        Returns the status if the PC has not reached the end, i.e., line 1001.
        Otherwise, it returns Status.Exit
        """
        
        if(self.__registers.PC().getVal() != 1001):
            return status
        
        return Status.EXIT
        
    def __LOAD_MQ(self):
        print("Control signal generated : Transferring contents of MQ to AC : AC <-- MQ")

        self.__registers.AC().write(self.__registers.MQ().getSV())
        
        self.__writeRegisters("AC <-- MQ")
        print("AC : ", self.__registers.AC())
        
        return self.__check(Status.CONTINUE)

    def __LOAD_MQ_MX(self):
        self.__MEM_TO_MBR()
        
        self.__MBR_TO_MQ()
        
        return self.__check(Status.CONTINUE)

    def __LOAD_MX(self):
        self.__MEM_TO_MBR()
        
        self.__MBR_TO_AC()
        
        return self.__check(Status.CONTINUE)

    def __LOAD_ABS_MX(self):
        self.__MEM_TO_MBR()

        print(f"Control signal generated : Absolute Value of MBR : MBR <-- |MBR|")
        self.__registers.MBR().write(self.__registers.MBR().getVal())
        print("MBR : ", self.__registers.MBR())
        self.__writeRegisters("MBR <-- |MBR|")
        
        self.__MBR_TO_AC()

        return self.__check(Status.CONTINUE)

    def __MBR_TO_MQ(self):
        print(f"Control signal generated : Transferring contents of MBR to MQ : MQ <-- MBR")
        self.__registers.MQ().write(self.__registers.MBR().getSV())
        self.__writeRegisters("MQ <-- MBR")
        print("MQ : ", self.__registers.MQ())
    
    def __MBR_TO_MEM(self, position: int):
        print(f"Control signal generated : Transferring contents of MBR to Memory : M[{position}] <-- MBR")
        self.__memory.dump(position, str(self.__registers.MBR()))
        print(f"M[{position}] :", self.__memory.load(position))
        self.__writeMemory(f"M[{position}] <-- MBR", 'W', position, str(self.__registers.MBR()))
        return self.__check(Status.CONTINUE)
    
    def __STOR_MX(self):
        
        position = self.__registers.MAR().getSV()

        print(f"Control signal generated : Transferring contents of AC to MBR: MBR <-- AC")
        self.__registers.MBR().write(self.__registers.AC().getSV())
        print("MBR :", self.__registers.MBR())
        self.__writeRegisters("MBR <-- AC")

        return self.__MBR_TO_MEM(position)

    def __MBR_TO_AC(self):
        print(f"Control signal generated : Transferring contents of MBR to AC : AC <-- MBR")
        self.__registers.AC().write(self.__registers.MBR().getSV())
        self.__writeRegisters("AC <-- MBR")
        print("AC : ", self.__registers.AC())
    
    def __MAR_TO_PC(self):
        print(f"Control signal generated : Transferring contents of MAR to PC : PC <-- MAR")
        self.__registers.PC().write(self.__registers.MAR().getSV())
        self.__writeRegisters("PC <-- MAR")
        print("PC :", self.__registers.PC())

    def __MEM_TO_MBR(self):
        position = self.__registers.MAR().getSV()

        print(f"Control signal generated : Transferring contents of Memory to MBR : MBR <-- M[{position}]")
        self.__registers.MBR().write(int("0b" + self.__memory.load(position), 2))
        print("MBR : ", self.__registers.MBR())
        self.__writeMemory("Reading", "R", position, self.__memory.load(position))
        self.__writeRegisters("Printing")

    def __LOAD_NEG_MX(self):
        self.__MEM_TO_MBR()

        print(f"Control signal generated : Negating MBR : MBR <-- -MBR")
        self.__registers.MBR().write(self.__registers.MBR().negate())
        print("MBR :", self.__registers.MBR())
        self.__writeRegisters("MBR <-- -MBR")

        self.__MBR_TO_AC()

        return self.__check(Status.CONTINUE)
    
    def __LOAD_NEG_ABS_MX(self):
        self.__MEM_TO_MBR()

        print(f"Control signal generated : Absolute Value of MBR : MBR <-- |MBR|")
        self.__registers.MBR().write(self.__registers.MBR().getVal())
        print("MBR : ", self.__registers.MBR())
        self.__writeRegisters("MBR <-- |MBR|")

        print(f"Control signal generated : Negating MBR : MBR <-- -MBR")
        self.__registers.MBR().write(self.__registers.MBR().negate())
        print("MBR : ", self.__registers.MBR())
        self.__writeRegisters("MBR <-- -MBR")
        
        self.__MBR_TO_AC()

        return self.__check(Status.CONTINUE)

    def __JUMP_MX_0_19(self):
        print(f"Control signal generated : Jumping to left Instruction")
        self.__MAR_TO_PC()
        return self.__check(Status.JUMP_LEFT)
    
    def __JUMP_MX_20_39(self):
        print(f"Control signal generated : Jumping to right Instruction")
        self.__MAR_TO_PC()
        return self.__check(Status.JUMP_RIGHT)

    def __JUMP_PLUS_MX_0_19(self):
        print(f"Control signal generated: Checking if AC >= 0")

        if(self.__registers.AC().getSign() == 0):
            print(f"Control signal generated : Jumping to left instruction")
            self.__MAR_TO_PC()
            return self.__check(Status.JUMP_LEFT)

        print(f"Continuing with normal execution")
        return self.__check(Status.CONTINUE)

    def __JUMP_PLUS_MX_20_39(self):
        print(f"Control signal generated: Checking if AC >= 0")

        if(self.__registers.AC().getSign() == 0):
            print(f"Control signal generated : Jumping to right instruction")
            self.__MAR_TO_PC()
            return self.__check(Status.JUMP_RIGHT)

        print(f"Continuing with normal execution")
        return self.__check(Status.CONTINUE)

    def __ADD_MX(self):
        self.__MEM_TO_MBR()

        print(f"Control signal generated : AC <-- AC + MBR")

        self.__registers.AC().write(self.__registers.AC().getSV() + self.__registers.MBR().getSV())
        self.__writeRegisters("AC <-- AC + MBR")

        return self.__check(Status.CONTINUE)

    def __SUB_MX(self):
        self.__MEM_TO_MBR()

        print(f"Control signal generated : AC <-- AC - MBR")

        self.__registers.AC().write(self.__registers.AC().getSV() - self.__registers.MBR().getSV())
        self.__writeRegisters("AC <-- AC - MBR")

        return self.__check(Status.CONTINUE)
    
    def __ADD_ABS_MX(self):
        self.__MEM_TO_MBR()

        print(f"Control signal generated : AC <-- AC + |MBR|")

        self.__registers.AC().write(self.__registers.AC().getSV() + self.__registers.MBR().getVal())
        print("AC :", self.__registers.AC())
        self.__writeRegisters("AC <-- AC + |MBR|")

        return self.__check(Status.CONTINUE)
    
    def __SUB_ABS_MX(self):
        self.__MEM_TO_MBR()

        print(f"Control signal generated : AC <-- AC - |MBR|")

        self.__registers.AC().write(self.__registers.AC().getSV() - self.__registers.MBR().getVal())
        print("AC :", self.__registers.AC())
        self.__writeRegisters("AC <-- AC - |MBR|")

        return self.__check(Status.CONTINUE)
    
    def __DIV_MX(self):
        self.__MEM_TO_MBR()

        print(f"Control signal generated : MQ <-- AC / MBR")
        q=(self.__registers.AC().getSV()) // (self.__registers.MBR().SV())
        r=((self.__registers.AC().getSV()) % (self.__registers.MBR().SV()))
        self.__registers.MQ().write(q)
        print("MQ :", self.__registers.MQ())
        self.__writeRegisters("MQ <-- AC / MBR")

        print(f"Control signal generated : AC <-- AC % MBR")
        self.__registers.AC().write(r)
        print("AC :", self.__registers.AC())
        self.__writeRegisters("AC <-- AC % MBR")

        return self.__check(Status.CONTINUE)

    def __MUL_MX(self):
        self.__MEM_TO_MBR()

        prod = bin(self.__registers.MQ().getVal() * self.__registers.MBR().getVal())[2::]
        a = (self.__registers.MQ().getSign()) ^ (self.self.__registers.MBR().getSign())
        while len(prod)<80:
            prod='0' + prod
        prod=bin(a)[2::] + prod
        
        print(f"Control signal generated : MQ <-- LSBs(MQ * MBR)")
        self.__registers.MQ().write(int(prod[-40::],2))
        print("MQ :", self.__registers.MQ())
        self.__writeRegisters("MQ <-- LSBs(MQ * MBR)")

        del prod[-40::]
        
        print(f"Control signal generated : AC <-- MSBs(MQ * MBR)")
        self.__registers.AC().write(int(prod,2))
        print("AC :", self.__registers.AC())
        self.__writeRegisters("AC <-- MSBs(MQ * MBR)")

        return self.__check(Status.CONTINUE)
    
    def __RSH(self):
        print(f"Control signal generated : AC l>> 1")
        self.__registers.AC().write(int(('0' + str(self.__registers.AC())[:-1:]), 2))
        print("AC :", self.__registers.AC())
        self.__writeRegisters("AC <-- AC l>> 1")

        return self.__check(Status.CONTINUE)

    def __LSH(self):
        print(f"Control signal generated : AC << 1")
        self.__registers.AC().write(int((str(self.__registers.AC())[1::]+'0'), 2))
        print("AC :", self.__registers.AC())
        self.__writeRegisters("AC <-- AC << 1")

        return self.__check(Status.CONTINUE)

    def __ARSH(self):
        print(f"Control signal generated : AC a>> 1")
        self.__registers.AC().write(int((str(self.__registers.AC().getSign()) + '0' + str(self.__registers.AC())[1:-1:]), 2))
        print("AC :", self.__registers.AC())
        self.__writeRegisters("AC <-- AC a>> 1")

        return self.__check(Status.CONTINUE)
    
    def __STOR_MX_8_19(self):
        position = self.__registers.MAR().read()

        print(f"Control signal generated : MBR <-- AC[28:39]")
        self.__registers.MBR().write(self.__registers.AC().read(Positions.RIGHTMOST_BITS_START.value, Positions.RIGHTMOST_BITS_END.value))
        print("MBR :", self.__registers.MBR())
        self.__writeRegisters("MBR <-- AC[28:39]")

        print(f"Control signal generated : MEM[8:19] <-- MBR[0:11]")
        self.__memory.dump(position, str(Register(12, self.__registers.MBR().read(Positions.RIGHTMOST_BITS_START.value, Positions.RIGHTMOST_BITS_END.value))), 8, 20)
        print(f"M[{position}] :", self.__memory.load(position))
        self.__writeMemory("MEM[8:19]", "W", position, self.__memory.load(position))
        
        return self.__check(Status.CONTINUE)

    def __STOR_MX_28_39(self):
        position = self.__registers.MAR().read()

        print(f"Control signal generated : MBR <-- AC[28:39]")
        self.__registers.MBR().write(self.__registers.AC().read(Positions.RIGHTMOST_BITS_START.value, Positions.RIGHTMOST_BITS_END.value))
        print("MBR :", self.__registers.MBR())
        self.__writeRegisters("MBR <-- AC[28:39]")

        print(f"Control signal generated : MEM2[28:39] <-- MBR[0:11]")
        self.__memory.dump(position, str(Register(12, self.__registers.MBR().read(Positions.RIGHTMOST_BITS_START.value, Positions.RIGHTMOST_BITS_END.value))), 28, 40)
        print(f"M[{position}] :", self.__memory.load(position))
        self.__writeMemory("MEM[28:39]", "W", position, self.__memory.load(position))
        
        return self.__check(Status.CONTINUE)

    def __NOP(self):
        return self.__check(Status.CONTINUE)
        
    def __HALT(self):
        return Status.EXIT

    def __INC(self):
        print(f"Control signal generated : AC++ ")
        self.__registers.AC().write( self.__registers.AC().getSV() + 1 )
        print("AC :", self.__registers.AC())
        self.__writeRegisters("AC <-- AC + 1")

        return self.__check(Status.CONTINUE)       

    def __DEC(self):
        print(f"Control signal generated : AC-- ")
        self.__registers.AC().write( self.__registers.AC().getSV() - 1 )
        print("AC :", self.__registers.AC())
        self.__writeRegisters("AC <-- AC - 1")

        return self.__check(Status.CONTINUE)  

    def __INP_MX(self):
        position = self.__registers.MAR().read()

        print(f"Control signal generated: Getting user input")
        
        while(True):
            try:
                val = int(input("Please enter a number : "))
            except ValueError:
                continue
            else:
                break
        
        print(f"Value entered is {val}")
        print(f"MBR <-- {val}")
        self.__registers.MBR().write(val)
        self.__writeRegisters(f"MBR <-- {val}")

        return self.__MBR_TO_MEM(position)
    
    def __DISP_MX(self):
        position = self.__registers.MAR().read()

        print(f"Control signal generated : MBR <-- M[{position}]")
        self.__registers.MBR().write(int("0b" + self.__memory.load(position), 2))
        self.__writeRegisters(f"MBR <-- M[{position}]")

        print(f"Value : {self.__registers.MBR().read()}")
        self.__writeRegisters(f"Value : {self.__registers.MBR().read()}")

        return self.__check(Status.CONTINUE)