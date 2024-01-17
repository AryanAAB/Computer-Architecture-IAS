from Processor import Status, HoldRegisters, Positions
from Memory import Memory
from Utilities import *

class Control:
    def __init__(self, registers:HoldRegisters, memory:Memory):
        checkType([(registers, HoldRegisters), (memory, Memory)])
        
        self.__registers = registers
        self.__memory = memory

        self.__functions = {
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
            Opcode.STOR_MX_8_19       : self.__STOR_MX_8_19,
            Opcode.STOR_MX_28_39      : self.__STOR_MX_28_39,
            Opcode.HALT               : self.__HALT,
            Opcode.NOP                : self.__NOP
            }

    def execute(self, instruction:str, code:Opcode):
        checkType([(instruction, str), (code, Opcode)])
        
        if(self.__functions.get(code) != None):
            self.__perform(self.__functions.get(code)(instruction))

        printErrorAndExit("No such opcode : ", code.name)
    
    def __LOAD_MQ(self):
        print("Control signal generated : Transferring contents of MQ to AC : AC <-- MQ")

        self.__registers.AC().write(self.__registers.MQ().read())

        return True
    
    def __STOR_MX(self):
        
        position = self.__registers.MAR().read()

        print(f"Control signal generated : Transferring contents of AC to MBR: MBR <-- AC")
        self.__registers.MBR().write(self.__registers.AC().read())

        print(f"Control signal generated : Transferring contents of MBR to Memory : M[{position}] <-- MBR")
        self.__memory.dump(position, self.__registers.MBR().read())

        return True

    def __JustLOAD(self):
        print(f"Control signal generated : Transferring contents of MBR to AC : AC <-- MBR")
        self.__registers.AC().write(self.__registers.MBR().read())

        return True
    
    def __LOAD_NEG_MX(self):
        position = self.__registers.MAR().read()

        print(f"Control signal generated : Transferring contents of Memory to MBR : MBR <-- M[{position}]")
        self.__registers.MBR().write(self.__memory.load(position))

        print(f"Control signal generated : Negating MBR : MBR <-- -MBR")
        self.__registers.MBR().negate()

        return self.__JustLOAD()
    
    def __LOAD_NEG_ABS_MX(self):
        position = self.__registers.MAR().read()

        print(f"Control signal generated : Transferring contents of Memory to MBR : MBR <-- M[{position}]")
        self.__registers.MBR().write(self.__memory.load(position))

        print(f"Control signal generated : Negating MBR : MBR <-- |MBR|")
        self.__registers.MBR().abs()

        print(f"Control signal generated : Negating MBR : MBR <-- -MBR")
        self.__registers.MBR().negate()
        
        return self.__JustLOAD()

    