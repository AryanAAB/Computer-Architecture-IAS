import sys
from enum import Enum

class InstructionSet():

    def __init__(self):
        """
        This is the valid instruction set
        """

        self.lst1={"LSH;":Opcode.LSH.value, "RSH;":Opcode.RSH.value, "NOP;":Opcode.NOP.value, "HALT;":Opcode.HALT.value}

        self.lst2=[('LOAD',
       {('MQ', ';'): Opcode.LOAD_MQ.value, ('MQ,M(', ');'): Opcode.LOAD_MQ_MX.value, ('M(', ');'): Opcode.LOAD_MX.value, ('-M(', ');'): Opcode.LOAD_NEG_MX.value, ('|M(', ')|;'): Opcode.LOAD_ABS_MX.value, ('-|M(', ')|;'): Opcode.LOAD_NEG_ABS_MX.value}),
      ('JUMP',
       {('M(', ',0:19);'): Opcode.JUMP_MX_0_19.value, ('M(', ',20:39);'): Opcode.JUMP_MX_20_39.value}),
      ('JUMP+',
       {('M(', ',0:19);'): Opcode.JUMP_PLUS_MX_0_19.value, ('M(', ',20:39);'): Opcode.JUMP_PLUS_MX_20_39.value}),
      ('ADD',
       {('M(', ');'): Opcode.ADD_MX.value, ('|M(', ')|;'): Opcode.ADD_ABS_MX.value}),
      ('SUB',
       {('M(', ');'): Opcode.SUB_MX.value, ('|M(', ')|;'): Opcode.SUB_ABS_MX.value}),
      ('MUL',
       {('M(', ');'): Opcode.MUL_MX.value}),
      ('DIV',
       {('M(', ');'): Opcode.DIV_MX.value}),
      ('STOR',
       {('M(', ',8:19);'): Opcode.STOR_MX_8_19.value, ('M(', ',28:39);'): Opcode.STOR_MX_28_39.value, ('M(', ');'): Opcode.STOR_MX.value})]


class Opcode(Enum):
    LOAD_MQ            = "00001010"    
    LOAD_MQ_MX         = "00001001"
    STOR_MX            = "00100001"
    LOAD_MX            = "00000001"
    LOAD_NEG_MX        = "00000010"
    LOAD_ABS_MX        = "00000011"
    LOAD_NEG_ABS_MX    = "00000100"
    JUMP_MX_0_19       = "00001101"
    JUMP_MX_20_39      = "00001110"
    JUMP_PLUS_MX_0_19  = "00001111"
    JUMP_PLUS_MX_20_39 = "00010000"
    ADD_MX             = "00000101"
    ADD_ABS_MX         = "00000111"
    SUB_MX             = "00000110"
    SUB_ABS_MX         = "00001000"
    MUL_MX             = "00001011"
    DIV_MX             = "00001100"
    LSH                = "00010100"
    RSH                = "00010101"
    STOR_MX_8_19       = "00010010"
    STOR_MX_28_39      = "00010011" 
    HALT               = "11111111"
    NOP                = "00000000"

def checkType(checkList:list):
    """
    checkList must be a list of the form
    [(arg1, type1), (arg2, type2), (arg3, type3), ..., (argN, typeN)]
    Returns true if all the types specified are correct and none of the
    arguments are None.
    Throws an Error and exits otherwise.
    """

    for arg in checkList:
        if(arg[0] == None or not isinstance(arg[0], arg[1])):
            printErrorAndExit(f"{arg[0]} is not of valid type {arg[1]}.")

    return True

def printErrorAndExit(message:str):
        """
        This function prints the error message specified by message and exits. 
        """

        print(message)
        sys.exit(1)
