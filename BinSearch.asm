PROGRAM FOR BINARY SEARCH

By Abhirath Adamane and Aryan V Bansal

********

!!! This assumes that the inputed array is already sorted

_start

	1 LOAD M(500); SUB M(501);		// Lines 1 and 2 represents 						
	2 JUMP++ M(14,0:19); ARSH; 		//while(*low <= *high){}

	3 ADD M(501); STOR M(502);		// Lines 2 and 3 represents
						// *mid = *high + (*low - *high)//2
	4 STOR M(5,28:39); NOP;  
	5 ;LOAD M();		// L4 fills M() // Lines 4 and 5 dereferrence mid like:
						//AC = *mid
	
	// Lines 6 to 13 is about shrinking the gap between low and high

	6 SUB M(1000); JUMP+ M(9,0:19); 
	7 LOAD M(502); INC;		// Lines 7 and 8 are for *low = *mid + 1 
	8 STOR M(500); JUMP M(1,0:19);

	9 DEC; JUMP+ M(12,0:19);		// !! **** maybe wrong JUMP+ M(11)
	10 LOAD M(502); STOR M(999);		// Lines 10 and 11 are if *mid is the required number
	11 JUMP M(15,0:19);

	12 LOAD M(502); DEC;		// Lines 12 and 13 are for *high = *mid - 1
	13 STOR M(501); JUMP M(1,0:19);
	
	14 LOAD M(16); STOR M(999);		// Here we store the answer into M(999)

_end

!!! The End result is stored at location 999

********
