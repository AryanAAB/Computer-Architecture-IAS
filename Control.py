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
            return self.__functions.get(code)(instruction)

        printErrorAndExit("No such opcode : ", code.name)
    
    def __check(self, status:Status):
        if(self.__registers.PC().read() != 1001):
            return status
        
        return Status.EXIT
        
    def __LOAD_MQ(self):
        print("Control signal generated : Transferring contents of MQ to AC : AC <-- MQ")

        self.__registers.AC().write(self.__registers.MQ().read())

        return self.__check(Status.CONTINUE)
    
    def __STOR_MX(self):
        
        position = self.__registers.MAR().read()

        print(f"Control signal generated : Transferring contents of AC to MBR: MBR <-- AC")
        self.__registers.MBR().write(self.__registers.AC().read())

        print(f"Control signal generated : Transferring contents of MBR to Memory : M[{position}] <-- MBR")
        self.__memory.dump(position, self.__registers.MBR().read())

        return self.__check(Status.CONTINUE)

    def __MBR_TO_AC(self):
        print(f"Control signal generated : Transferring contents of MBR to AC : AC <-- MBR")
        self.__registers.AC().write(self.__registers.MBR().read())
    
    def __MAR_TO_PC(self):
        print(f"Control signal generated : Transferring contents of MAR to PC : PC <-- MAR")
        self.__registers.PC().write(self.__registers.MAR().read())

    def __MEM_TO_MBR(self):
        position = self.__registers.MAR().read()

        print(f"Control signal generated : Transferring contents of Memory to MBR : MBR <-- M[{position}]")
        self.__registers.MBR().write(self.__memory.load(position))

    def __LOAD_NEG_MX(self):
        self.__MEM_TO_MBR()

        print(f"Control signal generated : Negating MBR : MBR <-- -MBR")
        self.__registers.MBR().write(self.__registers.MBR().negate())

        self.__MBR_TO_AC()

        return self.__check(Status.CONTINUE)
    
    def __LOAD_NEG_ABS_MX(self):
        self.__MEM_TO_MBR()

        print(f"Control signal generated : Negating MBR : MBR <-- |MBR|")
        self.__registers.MBR().write(self.__registers.MBR().abs())

        print(f"Control signal generated : Negating MBR : MBR <-- -MBR")
        self.__registers.MBR().write(self.__registers.MBR().negate())
        
        self.__MBR_TO_AC()

        return self.__check(Status.CONTINUE)

    def __JUMP_MX_20_39(self):
        print(f"Control signal generated : Jumping to right Instruction : PC <-- MAR")
        self.__MAR_TO_PC()

        return self.__check(Status.JUMP_RIGHT)

    def __JUMP_PLUS_MX_0_19(self):
        print(f"Control signal generated: Checking if AC >= 0")

        if(self.__registers.AC().read() >= 0):
            print(f"Control signal generated : Jumping to left instruction : PC <-- MAR")
            self.__MAR_TO_PC()
            return self.__check(Status.JUMP_LEFT)

        print(f"Continuing with normal execution")
        return self.__check(Status.CONTINUE)

    def __ADD_MX(self):
        self.__MEM_TO_MBR()

        print(f"Control signal generated : AC <-- AC + MBR")

        self.__registers.AC().write(self.__registers.AC().read() + self.__registers.MBR().read())
        return self.__check(Status.CONTINUE)
    
    def __SUB_ABS_MX(self):
        self.__MEM_TO_MBR()

        print(f"Control signal generated : AC <-- AC - |MBR|")

        self.__registers.AC().write(self.__registers.AC().read() + self.__registers.MBR().abs())
        return self.__check(Status.CONTINUE)
    
    def __DIV_MX(self):
        self.__MEM_TO_MBR()

        print(f"Control signal generated : MQ <-- AC / MBR")
        self.__registers.MQ().write(self.__registers.AC().read() // self.__registers.MBR().abs())

        print(f"Control signal generated : AC <-- AC % MBR")
        self.__registers.AC().write(self.__registers.AC().read() % self.__registers.MBR().abs())
        return self.__check(Status.CONTINUE)
    
    def __RSH(self):
        print(f"Control signal generated : AC / 2")
        self.__registers.AC().write(self.__registers.AC().read() % self.__registers.MBR().abs())
        return self.__check(Status.CONTINUE)
    
    def __STOR_MX_8_19(self):
        position = self.__registers.MAR().read()

        print(f"Control signal generated : MBR <-- AC[0:11]")
        self.__registers.MBR().write(self.__registers.AC().read(Positions.START, Positions.RIGHTMOST_BITS_END))

        print(f"Control signal generated : MEM[8:19] <-- MBR[0:11]")
        self.__memory.dump(position, str(self.__registers.MBR().read(Positions.START, Positions.RIGHTMOST_BITS_END)), 8, 19)

        return self.__check(Status.CONTINUE)