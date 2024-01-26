_include "IMT2023029_InsertionSort.asm"
_include "IMT2023029_BinSearch.asm"

_start

    //Getting the input from the user
    20 INP M(80); LOAD -M(80);                    //Gets user input for array length
    21 STOR M(81); JUMP+ M(26,20:39);             //Stores the array length in temporary memory 81
    22 LOAD -M(81); ADD M(499); 
    23 STOR M(24,8:19); NOP;
    24 INP M(0); LOAD M(81);                      //Gets the user value and puts into the memory
    25 ADD M(503); STOR M(81);                    //Decreases temp memory by one and stores it there
    26 JUMP M(21,20:39); NOP;                     //Goes back to first instruction

    //Displaying output
    15 DISP M(999); HALT;

    //Pre-Defined values and important locations

    80 0;       //Array length to be filled by user
    81 0;       //Temporary memory location used by the program
    82 1;       //Stores the value i
    83 1;       //Stores the value j
    84 0;       //Stores the value currentValue

    499 100;    //Starting constant
    500 101;    //Start address
    501 0;      //End address to be filled by user
    503 1;      //constant 1
    1000 0;     //Stores the value to check (to be filled by user)
_end
