"""
This class is used for reading the memory stored in a text file.
The text file must contain 1000 lines that are each of length 40.
The file must contain binary 1's and 0's.

@author Aryan Bansal and Abhirath Adamane
@version 1.0
@data 13/01/24
"""

from Utilities import *

class Memory:
    def __init__(self, fileName:str):
        """
        @param fileName : a string representing the file path consisting of the binary code.
        """

        checkType([(fileName, str)])
        
        self.__memory = self.__openFile(fileName)
    
    def __openFile(self, fileName):
        """
        Opens the file specified by fileName and reads the content available.
        @param fileName : a string representing the file path consisting of the binary code.
        @return a list specifying the contents of the file.
        """

        memory = []

        try:
            with open(fileName, 'r') as fh:
                memory = fh.readlines()
        except IOError:
            printErrorAndExit(f"The file path {fileName} does not exist.")
        
        if(len(memory) != 1000):
            printErrorAndExit("The memory length is not 1000.")
        
        memory = [i.strip() for i in memory]

        for i in memory:
            if(len(i) != 40):
                printErrorAndExit(f"Line {i} is not of length 40.")

        return memory
    
    def load(self, lineNumber: int):
        """
        Reads the memory specified by the lineNumber.
        @param lineNumber : The lineNumber to read. LineNumber must be between 1 and 1000. 
        @return a string that contains the contents of that lineNumber.
        """
        
        checkType([(lineNumber, int)])

        if(lineNumber <= 0 or lineNumber > 1000):
            printErrorAndExit(f"Cannot access lineNumber {lineNumber}.")

        return self.__memory[lineNumber - 1]

    def dump(self, lineNumber: int,  memory : str, start = 0, finish = 40):
        """
        Writes memory into the line specified by lineNumber.
        @param lineNumber : The lineNumber to write to. LineNumber must be between 1 and 1000.
        @param memory : The new content of the memory. Memory must be of length 40.
        """

        checkType([(lineNumber, int), (memory, str)])

        if(lineNumber <= 0 or lineNumber > 1000):
            printErrorAndExit(f"Cannot access lineNumber {lineNumber}.")
        elif(len(memory) != finish - start):
            printErrorAndExit(f"{memory} is of insufficient length. Must be of length 40.")
        
        self.__memory[lineNumber - 1] = self.__memory[lineNumber - 1][0:start] + memory + self.__memory[lineNumber - 1][finish:]