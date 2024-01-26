"""
This class is used for simulating the processor.

@author Aryan Bansal and Abhirath Adamane
@version 1.0
@data 13/01/24
"""

from IMT2023029_Control import Control
from IMT2023029_Memory import Memory
from IMT2023029_Utilities import *
from IMT2023029_ProcessorSupport import *

class Processor:
    """
    Defines the processor and runs the program.
    """

    def __init__(self, fileName:str, fh:str):
        """
        @param fileName : a string representing the file path consisting of the binary code.
        @param fh : a string representation of the file path consisting of the output file.
        """

        checkType([(fileName, str), (fh, str)])

        self.__memory = Memory(fileName=fileName)
        self.__registers = HoldRegisters()
        self.__control = Control(self.__registers, self.__memory, self.__writeRegisters, self.__writeMemory)
        
        try:
            self.__fh = open(fh, "w")
        except IOError:
            printErrorAndExit("No such file", fh)


    
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
        
    def __fetchFromMem(self):
        """
        Fetches data from memory. That is, it performs the operation MBR <-- MAR <-- PC.
        """
        
        print("PC :", self.__registers.PC())
        self.__writeRegisters("Printing Registers")

        #Going from PC to MAR
        print("Control signal generated : MAR <-- PC")
        self.__registers.MAR().write(self.__registers.PC().read())
        print("MAR :", self.__registers.MAR())
        self.__writeRegisters("MAR <-- PC")
        
        #Going from MAR to Memory to MBR
        print(f"Control signal generated : Read from memory at location MAR : {self.__registers.MAR().read()}")
        value = self.__memory.load(self.__registers.MAR().read())
        print("Memory value:", value)
        self.__writeMemory("Reading from memory", "R", self.__registers.MAR().read(), value)

        print(f"Control signal generated : MBR <-- M[{self.__registers.MAR().read()}]")
        self.__registers.MBR().write(int("0b" + value, 2))
        print("MBR :", self.__registers.MBR())
        self.__writeRegisters(f"MBR <-- M[{self.__registers.MAR().read()}]")

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
        self.__writeStage("FETCH")

        self.__fetchFromMem()

        #Going from MBR to IBR
        print("Control signal generated : Right Instruction goes to IBR : IBR <-- MBR[20:39]")
        self.__registers.IBR().write(self.__registers.MBR().read(Positions.MBR_RIGHT_INSTRUCTION_START.value, Positions.MBR_RIGHT_INSTRUCTION_END.value))
        print("IBR :", self.__registers.IBR())
        self.__writeRegisters("IBR <-- MBR[20:39]")

        #Going from MBR to IR
        print("Control signal generated : Left Opcode goes to IR : IR <-- MBR[0:7]")
        self.__registers.IR().write(self.__registers.MBR().read(Positions.MBR_LEFT_OPCODE_START.value, Positions.MBR_LEFT_OPCODE_END.value))
        print("IR :", self.__registers.IR())
        self.__writeRegisters("IR <-- MBR[0:7]")

        #Going from MBR to MAR
        print("Control signal generated : Left Address goes to MAR : MAR <-- MBR[8:19]")
        self.__registers.MAR().write(self.__registers.MBR().read(Positions.MBR_LEFT_ADDRESS_START.value, Positions.MBR_LEFT_ADDRESS_END.value))
        print("MAR :", self.__registers.MAR())
        self.__writeRegisters("MAR <-- MBR[8:19]")

        #PC = PC + 1
        print("Control signal generated : PC <-- PC + 1")
        self.__registers.PC().inc()
        print("PC :", self.__registers.PC())
        self.__writeRegisters("PC <-- PC + 1")

        print("Values of all registers after Fetch Cycle")
        self.__printAll()

        print("End of Fetch Cycle")
        self.__writeRegisters("End of Fetch Cycle")

    def __decode(self):
        """
        Starts the decode cycle.
        The decode cycle is characterized by decoding the opcode.
        @return code : Returns the value of the decoded code.
        """

        print("\nStart of Decode Cycle : ")
        self.__writeStage("DECODE")

        try:
            print(f"Control signal generated : Decoding {self.__registers.IR()}.")
            code = Opcode(str(self.__registers.IR()))
            print("Decoded Opcode :", code.name)
            self.__writeRegisters(f"Decoded Opcode : {code.name}")

        except Exception:
            printErrorAndExit(f"No such opcode {self.__registers.IR()}.")

        print("Values of all registers after Decode Cycle")
        self.__printAll()

        print("End of Decode Cycle")
        self.__writeRegisters("End of Decode Cycle")

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
        self.__writeStage("Execute")

        status = self.__control.execute("left", code)
        
        print("Values of all registers after Execute Cycle")
        self.__printAll()
        self.__writeRegisters("Printing")

        if(status == Status.JUMP_LEFT or status == Status.JUMP_RIGHT):
            self.__clearIBR()
        elif(status == Status.CONTINUE):
            self.__fetchRightIBR()
            code = self.__decodeRight()
            status = self.__executeRight(code)
        
        print("End of Execute Cycle")
        self.__writeRegisters("End of Execute Cycle")

        return status

    def __fetchRightIBR(self):
        """
        Starts the fetch cycle for fetching the right instruction from IBR.
        IR  <-- IBR[0:7]
        MAR <-- IBR[8:19]
        """

        print("\nStart of partial fetch cycle")
        self.__writeStage("Partial Fetch Cycle")

        #Going from IBR to IR
        print("Control signal generated : Right Opcode goes to IR : IR <-- IBR[0:7]")
        self.__registers.IR().write(self.__registers.IBR().read(Positions.IBR_RIGHT_OPCODE_START.value, Positions.IBR_RIGHT_OPCODE_END.value))
        print("IR :", self.__registers.IR())
        self.__writeRegisters("IR <-- IBR[0:7]")

        #Going from IBR to MAR
        print("Control signal generated : Right Address goes to MAR : MAR <-- IBR[8:19]")
        self.__registers.MAR().write(self.__registers.IBR().read(Positions.IBR_RIGHT_ADDRESS_START.value, Positions.IBR_RIGHT_ADDRESS_END.value))
        print("MAR :", self.__registers.MAR())
        self.__writeRegisters("MAR <-- IBR[8:19]")

        self.__clearIBR()
        print("Values of all registers after  Partial Fetch Cycle")
        self.__printAll()
        self.__writeRegisters("Printing")
        
        print("End of Partial Fetch Cycle")
        self.__writeRegisters("End of Partial Fetch Cycle")

    def __fetchRightMem(self):
        """
        Starts the fetch cycle but only for fetching the right memory.
        There is no IBR that is fetched.
        """

        print("\nStart of partial fetch cycle")
        self.__writeStage("Partial Fetch Cycle")

        self.__fetchFromMem()
        self.__clearIBR() #maybe a relic check and delete

        #Going from MBR to IR
        print("Control signal generated : Right Opcode goes to IR : IR <-- MBR[20:27]")
        self.__registers.IR().write(self.__registers.MBR().read(Positions.MBR_RIGHT_OPCODE_START.value, Positions.MBR_RIGHT_OPCODE_END.value))
        print("IR :", self.__registers.IR())
        self.__writeRegisters("IR <-- MBR[20:27]")

        #Going from MBR to MAR
        print("Control signal generated : Right Address goes to MAR : MAR <-- MBR[28:39]")
        self.__registers.MAR().write(self.__registers.MBR().read(Positions.MBR_RIGHT_ADDRESS_START.value, Positions.MBR_RIGHT_ADDRESS_END.value))
        print("MAR :", self.__registers.MAR())
        self.__writeRegisters("MAR <-- MBR[28:39]")

        #PC = PC + 1
        print("Control signal generated : PC <-- PC + 1")
        self.__registers.PC().inc()
        print("PC :", self.__registers.PC())
        self.__writeRegisters("PC <-- PC + 1")

        print("Values of all registers after Fetch Cycle")
        self.__printAll()

        print("End of Fetch Cycle")
        self.__writeRegisters("End of Fetch Cycle")

        print("\nEnd of partial fetch cycle")
        self.__writeRegisters("End of partial fetch cycle")

    def __clearIBR(self):
        """
        Clears the IBR and sets it to 0.
        """

        print("Clearing IBR")

        self.__registers.IBR().write(0)
        self.__writeRegisters("Clearing IBR")
        print("IBR : ", self.__registers.IBR())
        
    def __decodeRight(self):
        """
        Starts the decode cycle for the right instruction.
        @return code : string representation of the decoded opcode.
        """

        print("\nStart of Partial Decode Cycle : ")
        self.__writeStage("Partial Decode Cycle")

        try:
            print(f"Control signal generated : Decoding {self.__registers.IR()}.")
            code = Opcode(str(self.__registers.IR()))
            print("Decoded Opcode :", code.name)
            self.__writeRegisters(f"Decoded Opcode : {code.name}")

        except Exception:
            printErrorAndExit(f"No such opcode {self.__registers.IR()}.")

        print("Values of all registers after Partial Decode Cycle")
        self.__printAll()

        print("End of Partial Decode Cycle")
        self.__writeRegisters("End of Partial Decode Cycle")
        return code

    def __executeRight(self, code:Opcode):
        """
        Starts the execution cycle for the right instruction.
        @param code : the decoded right code
        @return status : returns the status specified by Enum Status.
        """

        checkType([(code, Opcode)])

        print("\nStart of Partial Execute Cycle : ")
        self.__writeStage("Partial Execute Cycle")

        status = self.__control.execute("right", code)
        
        print("Values of all registers after Partial Execute Cycle")
        self.__printAll()

        print("End of Partial Execute Cycle")
        self.__writeRegisters("End of Partial Execute Cycle")

        return status

    def run(self, PCStartValue:int, MemoryFinalValue:int):
        """
        Runs the processor.
        @param PCStartValue : the starting value of the PC
        """

        checkType([(PCStartValue, int), (MemoryFinalValue, int)])
        
        status = Status.CONTINUE
        self.__registers.PC().write(PCStartValue)

        self.__writeStage("NONE")
        self.__writeRegisters(None)

        while(status != Status.EXIT):
            if(status == Status.JUMP_RIGHT):
                self.__fetchRightMem()
                code = self.__decodeRight()
                status = self.__executeRight(code)

            else:
                self.__fetch()
                code = self.__decode()
                status = self.__execute(code)

            input()
        
        self.__fh.write("END" + "\n")
        self.__fh.write(self.__memory.load(MemoryFinalValue))

        self.__fh.close()
        
    def __writeStage(self, value:str):
        """
        Writes the current stage in the output file.
        @param value : the new stage.
        """
        
        self.__fh.write("STAGE: " + value + "\n")
    
    def __writeRegisters(self, value:str):
        """
        Writes the values of the registers to the output file.
        @param value : the operation performed if any.
        """
        if(value != None):
            self.__fh.write(value + "\n")

        self.__fh.write(str(self.__registers.PC().getVal()) + "\n")
        self.__fh.write(str(self.__registers.MAR().getVal()) + "\n")
        self.__fh.write(str(self.__registers.MBR().getVal()) + "\n")
        self.__fh.write(str(self.__registers.IBR().getVal()) + "\n")
        self.__fh.write(str(self.__registers.IR().getVal()) + "\n")
        self.__fh.write(str(self.__registers.AC().getVal()) + "\n")
        self.__fh.write(str(self.__registers.MQ().getVal()) + "\n")

    def __writeMemory(self, operation:str, rw:str, position:int, value:str):
        """
        Writes the memory values into the outputfile.
        @param operation : the operation performed
        @param rw : read or write
        @param position : the line number that was changed
        @param value : the read/written value of the memory.
        """
        
        self.__fh.write(operation + "\n")
        self.__fh.write(rw + "\n")
        self.__fh.write(str(position) + " ")
        self.__fh.write(str(int("0b" + value, 2)) + "\n")
