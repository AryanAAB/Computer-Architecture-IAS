from Utilities import *

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


class Assembler():

    def __init__(self, fileName):

        """
            This method readies the assembler.
        """

        checkType([(fileName,str)])
        if not (fileName.endswith(".asm")):
            printErrorAndExit("Invalid file type.")
        self.__fileName=fileName
        self.__IS=InstructionSet()
        
        self.__run()



    def __firstParse(self, lines):
        """
        This method readies the assembly code to be converted into machine code.
        It performs _define, _include, _var, _start.
        It also ensures the code has no syntactical errors to an extent.
        """
        return lines



    def __secondParse(self, lines):
        """
            This method blindly converts the results into machine code by string matching with the instruction set.
        """
    
        def addZeros(string, size):
            """
                This function takes the binary number and provides a padding of the required length.
            """
    
            while(len(string)<size):
                string="0"+string
            return string

        def addInstruct(s):
            """
                This function readies a 20 bit instruction in the form of machine code.
            """
            s=s.strip()+';'
            ls=s.split()
            if ls[0] in self.__IS.lst1:
                return str(self.__IS.lst1[ls[0]])+"0"*12
            else:
                for i in self.__IS.lst2:
                    if (ls[0]==i[0]):
                        for j in i[1].items():
                            if ls[1].startswith(j[0][0]) and ls[1].endswith(j[0][1]):
                                ls[1]=ls[1].strip(j[0][0])
                                ls[1]=ls[1].strip(j[0][1])
                                if ls[1].isdigit():
                                    return(j[1]+addZeros(bin(int(ls[1]))[2:],12))   
                else:
                    printErrorAndExit("Invalid Statements")

        def checkInstruct(lst):

            """
                This function prepares each memory location with the required instructions.
            """
        
            if len(lst)==1:
                return addInstruct(lst[0])+("0"*20) + "\n"
            if lst[0]=='':
                return ('0'*20)+addInstruct(lst[1]) + "\n"
            return addInstruct(lst[0]) + addInstruct(lst[1]) + "\n"

        z=('0'*40)+'\n'
        memory=[z for i in range(1000)]
        for i in lines:
            temp=i.strip().split(";")
            temp=temp[:-1]
            pos=int(temp[0].split()[0])-1
            temp[0]=(" ".join(temp[0].split()[1:]))
            if temp[0].isdigit():
                memory[pos]=(addZeros(bin(int(temp[0]))[2:], 40)+"\n")
            else:
                memory[pos]=checkInstruct(temp)
        return memory



    def __run(self):

        """
            This accesses the file and runs the assembler.
        """
        
        try:
            with open(f"{self.__fileName}", "r") as fileObject:
                self.__lines=fileObject.readlines()
        except:
            printErrorAndExit("Unable to use file.")

            
        onlyMemory=self.__firstParse(self.__lines)
        toDump=self.__secondParse(onlyMemory)

        
        while self.__fileName[-1]!=".":
            self.__fileName=self.__fileName[:-1]
        with open(f"{self.__fileName}obj", "w") as fileObject:
            fileObject.writelines(toDump)       


""""__main__"""
assembler=Assembler(input("Enter the file to be assembled:\n"))

