PROGRAM FOR INSERTION SORT

By Aryan Bansal and Abhirath Adamane

********
!!! This assumes that the values that the user inputs are valid.

_start

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
    48 STOR M(501); NOP;

    //Sets the value that the user wants to find
    49 INP M(1000); JUMP M(1,0:19);
_end
