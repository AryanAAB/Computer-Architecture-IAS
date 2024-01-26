from IMT2023513_Assembler import Assembler
from IMT2023513_Processor import Processor

asmFile = "IMT2023513_Assembly.asm"
executableFile = "IMT2023513_Assembly.exe"
outputFile = "Output.txt"

Assembler(asmFile).run()
Processor(executableFile, outputFile).run(20, 999)
