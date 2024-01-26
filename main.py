from Assembler import Assembler
from Processor import Processor

asmFile = "Assembly.asm"
executableFile = "Assembly.exe"
outputFile = "Output.txt"

Assembler(asmFile).run()
Processor(executableFile, outputFile).run(1, 999)
