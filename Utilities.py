import sys
from enum import Enum

class InstructionSet():

    def __init__(self):
        """
        This is the valid instruction set
        """

        self.lst1={"LSH;":"00010100", "RHS;":"00010101", "NOP;":"00000000", "HALT;":"11111111"}

        self.lst2=[('LOAD',
       {('MQ', ';'): "00001010", ('MQ,M(', ');'): "00001001", ('M(', ');'): "00000001", ('-M(', ');'): "00000010", ('|M(', ')|;'): "00000011", ('-|M(', ')|;'): "00000100"}),
      ('JUMP',
       {('M(', ',0:19);'): "00001101", ('M(', ',20:39);'): "00001110"}),
      ('JUMP+',
       {('M(', ',0:19);'): "00001111", ('M(', ',20:39);'): "00010000"}),
      ('ADD',
       {('M(', ');'): "00000101", ('|M(', ')|;'): "00000111"}),
      ('SUB',
       {('M(', ');'): "00000110", ('|M(', ')|;'): "00001000"}),
      ('MUL',
       {('M(', ');'): "00001011"}),
      ('DIV',
       {('M(', ');'): "00001100"}),
      ('STOR',
       {('M(', ',8:19);'): "00010010", ('M(', ',28:39);'): "00010011", ('M(', ');'): "00100001"})]


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
