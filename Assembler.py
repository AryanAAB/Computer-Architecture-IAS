"""
This class is the Assembler which converts the text given by the user
into binary instructions which the IAS machine can understand. 

@author Abhirath Adamane and Aryan Bansal
@version 1.0
@date 13/01/24
"""

from Utilities import *

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


    def __firstParse(self, lines):
        """
        This method readies the assembly code to be converted into machine code.
        It performs |_define|, _include, |_var|, _start.
        It also ensures the code has no syntactical errors to an extent.
        """
        
        def start(lines):
            k=len(lines)
            i=0
            while(i<k):
                s=lines[i]
                s=s.strip()
                s=s.split("//")[0]         
                if s=='':
                    k=k-1
                    lines.pop(i)
                    continue
                if s=='_end':
                    return lines[:i]
                lines[i]=s
                i+=1
            return lines

        
        included=[]
        for j in range(len(lines)):
            
            i=lines[j].strip().split("//")[0]
            
            if i.startswith("_include"):
                i=i.strip()
                i=i.lstrip("_include")
                i=i.strip()
                i=i.strip('"')
                a1=Assembler(i)
                included.append(a1.run(1))

            if i=="_start":
                included.append(start(lines[j+1:]))
                
                ans=[]
                for k in included:
                    ans=ans+k
                return ans

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
                                num=ls[1][len(j[0][0]):(-len(j[0][1]))]
                                if num.isdigit():
                                    return(j[1]+addZeros(bin(int(num))[2:],12))
                                else:
                                    return(j[1]+"0"*12)
                else:
                    print(s)
                    printErrorAndExit("Invalid Statements")

        def checkInstruct(lst):

            """
                This function prepares each memory location with the required instructions.
            """
            
            if len(lst)==1:
                return addInstruct(lst[0])+("0"*20) + "\n"
            if lst[0]=='':
                if lst[1]=='':
                    return '0'*40
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
            elif temp[0][1::].isdigit() and (temp[0][0]=="-" or temp[0][0]=="+"):
                stringNum=(addZeros(bin(int(temp[0][1::]))[2:], 39)+"\n")
                if temp[0][0]=="-":
                    memory[pos] = "1" + stringNum
                else:
                    memory[pos] = "0" + stringNum
            else:
                memory[pos]=checkInstruct(temp)
                
        return memory
        

    def run(self, val=0 ):

        """
            This accesses the file and runs the assembler.
        """
        
        try:
            with open(f"{self.__fileName}", "r") as fileObject:
                self.__lines=fileObject.readlines()
        except:
            printErrorAndExit("Unable to use file.")

            
        onlyMemory=self.__firstParse(self.__lines)

        if val:
            return onlyMemory
        
        toDump=self.__secondParse(onlyMemory)
        
        while self.__fileName[-1]!=".":
            self.__fileName=self.__fileName[:-1]
        with open(f"{self.__fileName}exe", "w") as fileObject:
            fileObject.writelines(toDump)
        return toDump

if __name__ == "__main__":
    assembler=Assembler(input("Enter the file to be assembled:\n"))
    assembler.run()









