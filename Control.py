from Memory import Memory
from Utilities import *
from ProcessorSupport import *

class Control:
    def __init__(self, registers:HoldRegisters, memory:Memory, writeStage, writeRegisters, writeMemory):
        checkType([(registers, HoldRegisters), (memory, Memory)])
        
        self.__registers = registers
        self.__memory = memory
        self.__writeRegisters = writeRegisters
        self.__writeStage = writeStage
        self.__writeMemory = writeMemory

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
            return self.__functions.get(code)()

        printErrorAndExit("No such opcode : ", code.name)
    
    def __check(self, status:Status):
        if(self.__registers.PC().read() != 1001):
            return status
        
        return Status.EXIT
        
    def __LOAD_MQ(self):
        print("Control signal generated : Transferring contents of MQ to AC : AC <-- MQ")

        self.__registers.AC().write(self.__registers.MQ().read())
        
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
        self.__registers.MBR().write(self.__registers.MBR().abs())
        print("MBR : ", self.__registers.MBR())
        self.__writeRegisters("MBR <-- |MBR|")
        
        self.__MBR_TO_AC()

        return self.__check(Status.CONTINUE)

    def __MBR_TO_MQ(self):
        print(f"Control signal generated : Transferring contents of MBR to MQ : MQ <-- MBR")
        self.__registers.MQ().write(self.__registers.MBR().read())
        self.__writeRegisters("MQ <-- MBR")
        print("MQ : ", self.__registers.MQ())
    
    def __STOR_MX(self):
        
        position = self.__registers.MAR().read()

        print(f"Control signal generated : Transferring contents of AC to MBR: MBR <-- AC")
        self.__registers.MBR().write(self.__registers.AC().read())
        print("MBR :", self.__registers.MBR())
        self.__writeRegisters("MBR <-- AC")

        print(f"Control signal generated : Transferring contents of MBR to Memory : M[{position}] <-- MBR")
        self.__memory.dump(position, str(self.__registers.MBR()))
        print(f"M[{position}] :", self.__memory.load(position))
        self.__writeMemory(f"M[{position}] <-- MBR", 'W', position, str(self.__registers.MBR()))
        return self.__check(Status.CONTINUE)

    def __MBR_TO_AC(self):
        print(f"Control signal generated : Transferring contents of MBR to AC : AC <-- MBR")
        self.__registers.AC().write(self.__registers.MBR().read())
        self.__writeRegisters("AC <-- MBR")
        print("AC : ", self.__registers.AC())
    
    def __MAR_TO_PC(self):
        print(f"Control signal generated : Transferring contents of MAR to PC : PC <-- MAR")
        self.__registers.PC().write(self.__registers.MAR().read())
        self.__writeRegisters("PC <-- MAR")
        print("PC :", self.__registers.PC())

    def __MEM_TO_MBR(self):
        position = self.__registers.MAR().read()

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
        self.__registers.MBR().write(self.__registers.MBR().abs())
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

        self.__registers.AC().write(self.__registers.AC().getVal() + self.__registers.MBR().getVal())
        self.__writeRegisters("AC <-- AC + MBR")

        return self.__check(Status.CONTINUE)

    def __SUB_MX(self):
        self.__MEM_TO_MBR()

        print(f"Control signal generated : AC <-- AC - MBR")

        self.__registers.AC().write(self.__registers.AC().getVal() - self.__registers.MBR().getVal())
        self.__writeRegisters("AC <-- AC - MBR")

        return self.__check(Status.CONTINUE)
    
    def __ADD_ABS_MX(self):
        self.__MEM_TO_MBR()

        print(f"Control signal generated : AC <-- AC + |MBR|")

        self.__registers.AC().write(self.__registers.AC().getVal() + self.__registers.MBR().abs())
        print("AC :", self.__registers.AC())
        self.__writeRegisters("AC <-- AC + |MBR|")

        return self.__check(Status.CONTINUE)
    
    def __SUB_ABS_MX(self):
        self.__MEM_TO_MBR()

        print(f"Control signal generated : AC <-- AC - |MBR|")

        self.__registers.AC().write(self.__registers.AC().getVal() - self.__registers.MBR().abs())
        print("AC :", self.__registers.AC())
        self.__writeRegisters("AC <-- AC - |MBR|")

        return self.__check(Status.CONTINUE)
    
    def __DIV_MX(self):
        self.__MEM_TO_MBR()

        print(f"Control signal generated : MQ <-- AC / MBR")
        self.__registers.MQ().write(self.__registers.AC().getVal() // self.__registers.MBR().getVal())
        print("MQ :", self.__registers.MQ())
        self.__writeRegisters("MQ <-- AC / MBR")

        print(f"Control signal generated : AC <-- AC % MBR")
        self.__registers.AC().write(self.__registers.AC().getVal() % self.__registers.MBR().getVal())
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
        print(f"Control signal generated : AC >> 1")
        self.__registers.AC().write(self.__registers.AC().read() // 2)
        print("AC :", self.__registers.AC())
        self.__writeRegisters("AC <-- AC >> 1")

        return self.__check(Status.CONTINUE)

    def __LSH(self):
        print(f"Control signal generated : AC << 1")
        self.__registers.AC().write(self.__registers.AC().read() * 2)
        print("AC :", self.__registers.AC())
        self.__writeRegisters("AC <-- AC << 1")

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
