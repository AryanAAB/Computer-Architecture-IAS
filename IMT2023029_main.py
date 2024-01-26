from IMT2023029_Assembler import Assembler
from IMT2023029_Processor import Processor

asmFile = "IMT2023029_Assembly.asm"
executableFile = "IMT2023029_Assembly.exe"
outputFile = "IMT2023029_Output.txt"

Assembler(asmFile).run()
Processor(executableFile, outputFile).run(20, 999)
