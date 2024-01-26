from enum import Enum
from Register import Register

class Positions(Enum):
    #Declaring constants that specify the first bit(inclusive)
    START                       =  0
    MBR_LEFT_OPCODE_START       =  0
    MBR_LEFT_ADDRESS_START      =  8
    MBR_RIGHT_OPCODE_START      = 20
    MBR_RIGHT_ADDRESS_START     = 28
    MBR_RIGHT_INSTRUCTION_START = 20
    IBR_RIGHT_OPCODE_START      =  0
    IBR_RIGHT_ADDRESS_START     =  8
    RIGHTMOST_BITS_START        = 28
    #Declaring constants that specify the last bit(exclusive)
    PC_END                      = 12
    MAR_END                     = 12
    MBR_LEFT_OPCODE_END         =  8
    MBR_LEFT_ADDRESS_END        = 20
    MBR_RIGHT_OPCODE_END        = 28
    MBR_RIGHT_ADDRESS_END       = 40
    MBR_RIGHT_INSTRUCTION_END   = 40
    IBR_RIGHT_OPCODE_END        =  8
    IBR_RIGHT_ADDRESS_END       = 20
    MBR_END                     = 40
    IBR_END                     = 20
    IR_END                      =  8
    AC_END                      = 40
    MQ_END                      = 40
    RIGHTMOST_BITS_END          = 40

class Status(Enum):
    #Declaring constants that specify status after execution
    CONTINUE                    = 0 # Continue means to continue processing the input
    EXIT                        = 1 # Exit means that we have reached HALT or end of PC has been reached
    JUMP_LEFT                   = 2 # JUMP_LEFT means that we want to jump left
    JUMP_RIGHT                  = 3 # JUMP_RIGHT means that we want to jump right
    
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
    
