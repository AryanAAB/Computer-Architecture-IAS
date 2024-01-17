"""
This class is used for simulating the processor.

@author Aryan and Abhirath
@version 1.0
@data 13/01/24
"""

from Control import Control
from Memory import Memory
from Register import Register
from Utilities import *
from enum import Enum

class Positions(Enum):
    #Declaring constants that specify the first bit(inclusive)
    START                       =  0
    MBR_LEFT_OPCODE_START       =  0
    MBR_LEFT_ADDRESS_START      =  8
    MBR_RIGHT_INSTRUCTION_START = 20
    IBR_RIGHT_OPCODE_START      =  0
    IBR_RIGHT_ADDRESS_START     =  8

    #Declaring constants that specify the last bit(exclusive)
    PC_END                      = 12
    MAR_END                     = 12
    MBR_LEFT_OPCODE_END         =  8
    MBR_LEFT_ADDRESS_END        = 20
    MBR_RIGHT_INSTRUCTION_END   = 40
    IBR_RIGHT_OPCODE_END        =  8
    IBR_RIGHT_ADDRESS_END       = 20
    MBR_END                     = 40
    IBR_END                     = 20
    IR_END                      =  8
    AC_END                      = 40
    MQ_END                      = 40

class Status(Enum):
    #Declaring constants that specify status after execution
    CONTINUE                    = 0 # Continue means to continue processing the input
    EXIT                        = 1 # Exit means that we have reached HALT or end of PC has been reached
    CLEAR_IBR                   = 2 # Clear IBR means that we want to clear IBR because we don't want to execute the right statement

"""
Creates a PC, MAR, MBR, IBR, IR, AC, and MQ registers.
"""
class HoldRegisters:
    """
    Holds the registers PC, MAR, MBR, IBR, IR, AC, MQ
    """

    def __init__(self):
        self.__PC  = Register(size = Positions.PC_END.value)  # declaring 12 bit Program Counter
        self.__MAR = Register(size = Positions.MAR_END.value) # declaring 12 bit Memory Address Register
        self.__MBR = Register(size = Positions.MBR_END.value) # declaring 40 bit Memory Buffer Register
        self.__IBR = Register(size = Positions.IBR_END.value) # declaring 20 bit Instruction Buffer Register
        self.__IR  = Register(size = Positions.IR_END.value)  # declaring 8 bit Instruction Register
        self.__AC  = Register(size = Positions.AC_END.value)  # declaring 40 bit Accumulator
        self.__MQ  = Register(size = Positions.MQ_END.value)  # declaring 40 bit Multiplier Quotient
    
    def PC(self):
        """
        @return the PC register.
        """

        return self.__PC

    def MAR(self):
        """
        @return the MAR register.
        """

        return self.__MAR

    def MBR(self):
        """
        @return the MBR register.
        """

        return self.__MBR

    def IBR(self):
        """
        @return the IBR register.
        """

        return self.__IBR
    
    def IR(self):
        """
        @return the IR register.
        """

        return self.__IR

    def AC(self):
        """
        @return the AC register.
        """

        return self.__AC
    
    def MQ(self):
        """
        @return the MQ register.
        """

        return self.__MQ
    
class Processor:
    """
    Defines the processor and runs the program.
    """

    def __init__(self, fileName:str):
        """
        @param fileName : a string representing the file path consisting of the binary code.
        """

        checkType([(fileName, str)])

        self.__memory = Memory(fileName=fileName)
        self.__registers = HoldRegisters()
        self.__control = Control()


    
    def __printAll(self):
        """
        Prints values of all the registers.
        """
        
        print("PC  :", self.__registers.PC())
        print("MAR :", self.__registers.MAR())
        print("MBR :", self.__registers.MBR())
        print("IBR :", self.__registers.IBR())
        print("IR  :", self.__registers.IR())
        print("AC  :", self.__registers.AC())
        print("MQ  :", self.__registers.MQ())

    def __fetch(self):
        """
        Starts the fetch cycle.
        The fetch cycle is characterized by
        MAR <-- PC
        MBR <-- MAR
        IBR <-- MBR[20:39]
        IR  <-- MBR[0:7]
        MAR <-- MBR[8:19]
        PC  <-- PC + 1
        """
        
        print("\nStart of Fetch Cycle : ")
        
        print("PC :", self.__registers.PC())
        
        #Going from PC to MAR
        print("Control signal generated : MAR <-- PC")
        self.__registers.MAR().write(self.__registers.PC().read())
        print("MAR :", self.__registers.MAR())
        
        #Going from MAR to Memory to MBR
        print(f"Control signal generated : Read from memory at location MAR : {self.__registers.MAR().read()}")
        value = self.__memory.load(self.__registers.MAR().read())
        print("Memory value:", value)
        print(f"Control signal generated : MBR <-- M[{self.__registers.MAR().read()}]")
        self.__registers.MBR().write(int("0b" + value, 2))
        print("MBR :", self.__registers.MBR())

        #Going from MBR to IBR
        print("Control signal generated : Right Instruction goes to IBR : IBR <-- MBR[20:39]")
        self.__registers.IBR().write(self.__registers.MBR().read(Positions.MBR_RIGHT_INSTRUCTION_START.value, Positions.MBR_RIGHT_INSTRUCTION_END.value))
        print("IBR :", self.__registers.IBR())

        #Going from MBR to IR
        print("Control signal generated : Left Opcode goes to IR : IR <-- MBR[0:7]")
        self.__registers.IR().write(self.__registers.MBR().read(Positions.MBR_LEFT_OPCODE_START.value, Positions.MBR_LEFT_OPCODE_END.value))
        print("IR :", self.__registers.IR())

        #Going from MBR to MAR
        print("Control signal generated : Left Address goes to MAR : MAR <-- MBR[8:19]")
        self.__registers.MAR().write(self.__registers.MBR().read(Positions.MBR_LEFT_ADDRESS_START.value, Positions.MBR_LEFT_ADDRESS_END.value))
        print("MAR :", self.__registers.MAR())

        #PC = PC + 1
        print("Control signal generated : PC <-- PC + 1")
        self.__registers.PC().inc()
        print("PC :", self.__registers.PC())

        print("Values of all registers after Fetch Cycle")
        self.__printAll()

        print("End of Fetch Cycle")
    
    def __decode(self):
        """
        Starts the decode cycle.
        The decode cycle is characterized by decoding the opcode.
        @return code : Returns the value of the decoded code.
        """

        print("\nStart of Decode Cycle : ")
        try:
            print(f"Control signal generated : Decoding {self.__registers.IR()}.")
            code = Opcode(str(self.__registers.IR()))
            print("Decoded Opcode :", code.name)
        except Exception:
            printErrorAndExit(f"No such opcode {self.__registers.IR()}.")

        print("Values of all registers after Decode Cycle")
        self.__printAll()

        print("End of Decode Cycle")

        return code

    def __execute(self, code:Opcode):
        """
        Starts the execute cycle.
        The execute cycle is characterized by executing the instruction given.
        @param code : The value of the decoded code
        @return status : returns the status specified by Enum Status.
        """

        checkType([(code, Opcode)])

        print("\nStart of Execute Cycle : ")

        status = self.__control.execute("left", code, self.__registers, self.__memory)
        
        print("Values of all registers after Execute Cycle")
        self.__printAll()

        if(status == Status.CLEAR_IBR):
            print("Clearing IBR")
            self.__registers.IBR().write(0)
        elif(status == Status.CONTINUE):
            self.__fetchRightIBR()
            ccode = self.__decodeRightIBR()
            status = self.__executeRightIBR(code)
        
        print("End of Execute Cycle")

        return status

    def __fetchRightIBR(self):
        """
        Starts the fetch cycle for fetching the right instruction from IBR.
        IR  <-- IBR[0:7]
        MAR <-- IBR[8:19]
        """

        print("\nStart of partial fetch cycle")

        #Going from IBR to IR
        print("Control signal generated : Right Opcode goes to IR : IR <-- IBR[0:7]")
        self.__registers.IR().write(self.__registers.IBR().read(Positions.IBR_RIGHT_OPCODE_START.value, Positions.IBR_RIGHT_OPCODE_END.value))
        print("IR :", self.__registers.IR())

        #Going from IBR to MAR
        print("Control signal generated : Right Address goes to MAR : MAR <-- IBR[8:19]")
        self.__registers.MAR().write(self.__registers.IBR().read(Positions.IBR_RIGHT_ADDRESS_START.value, Positions.IBR_RIGHT_ADDRESS_END.value))
        print("MAR :", self.__registers.MAR())

        print("Values of all registers after  Partial Fetch Cycle")
        self.__printAll()

        print("End of Partial Fetch Cycle")

    def __decodeRightIBR(self):
        """
        Starts the decode cycle for the right instruction.
        @return code : string representation of the decoded opcode.
        """
        
        print("\nStart of Partial Decode Cycle : ")
        try:
            print(f"Control signal generated : Decoding {self.__registers.IR()}.")
            code = Opcode(str(self.__registers.IR()))
            print("Decoded Opcode :", code.name)
        except Exception:
            printErrorAndExit(f"No such opcode {self.__registers.IR()}.")

        print("Values of all registers after Partial Decode Cycle")
        self.__printAll()

        print("End of Decode Cycle")

        return code

    def __executeRightIBR(self, code:Opcode):
        """
        Starts the execution cycle for the right instruction.
        @param code : the decoded right code
        @return status : returns the status specified by Enum Status.
        """

        checkType([(code, Opcode)])

        print("\nStart of Partial Execute Cycle : ")

        status = self.__control.execute("right", code, self.__registers, self.__memory)
        
        print("Values of all registers after Partial Execute Cycle")
        self.__printAll()

        print("End of Partial Execute Cycle")

        return status

    def run(self, PCStartValue:int):
        """
        Runs the processor.
        @param PCStartValue : the starting value of the PC
        """

        checkType([(PCStartValue, int)])
        
        status = Status.CONTINUE
        self.__registers.PC().write(PCStartValue)

        while(status == Status.CONTINUE):
            self.__fetch()
            code = self.__decode()
            status = self.__execute(code)


            input()

Processor("Assembly.obj").run(1)