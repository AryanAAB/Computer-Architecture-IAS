_start
    80 0;       //Array length to be filled by user
    81 0;       //Temporary memory location used by the program
    82 1;       //Stores the value i
    83 1;       //Stores the value j
    84 0;       //Stores the value currentValue

    499 100;    //Starting constant
    500 101;    //Start address
    502 0;      //End address to be filled by user
    503 1;      //constant 1
    1000 0;     //Stores the value to check (to be filled by user)

    //Getting the input from the user
    20 INP M(80); LOAD -M(80);                    //Gets user input for array length
    21 STOR M(81); JUMP+ M(26,20:39);             //Stores the array length in temporary memory 81
    22 LOAD -M(81); ADD M(499); 
    23 STOR M(24,8:19); NOP;
    24 INP M(0); LOAD M(81);                      //Gets the user value and puts into the memory
    25 ADD M(503); STOR M(81);                    //Decreases temp memory by one and stores it there
    26 JUMP M(21,20:39); NOP;                     //Goes back to first instruction

    //Sorts the array
    27 LOAD M(82); SUB M(80);                     //For loop condition
    28 JUMP+ M(47,0:19); LOAD M(82);              //If condition is false, exit
    29 STOR M(83); ADD M(500);                    //Sets the value of j = i
    30 STOR M(31,8:19); NOP;
    31 LOAD M(0); STOR M(84);                     //Sets the currentValue
    32 LOAD -M(83); JUMP+ M(42,0:19);             //First condition of whilee loop
    33 LOAD M(83); SUB M(503);
    34 ADD M(500); STOR M(35,8:19);
    35 LOAD -M(0); ADD M(84);
    36 JUMP+ M(42,0:19); LOAD M(83);              //Second condition of while loop ends and body starts
    37 ADD M(500); STOR M(39,28:39);
    38 SUB M(503); STOR M(39,8:19);
    39 LOAD M(0); STOR M(0);
    40 LOAD M(83); SUB M(503);
    41 STOR M(83); JUMP M(32,0:19);                //While loop ends here
    42 LOAD M(83); ADD M(500);
    43 STOR M(44,8:19); LOAD M(84);
    44 STOR M(0); LOAD M(82);
    45 ADD M(503); STOR M(82);
    46 JUMP M(27,0:19); NOP;                       //For loop ends here

    //Sets the ending value for binary search
    47 LOAD M(80); ADD M(499);
    48 STOR M(502); NOP;

    //Sets the value that the user wants to find
    49 INP M(1000); JUMP M(1,0:19);
_end