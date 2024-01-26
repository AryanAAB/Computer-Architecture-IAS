/*
 * This class is for reading from a text file so as to interactively show what is happening in the processor.
 * The text file must have the following elements in the starting
 * 
 * "STAGE: " Stage Name
 * PC value
 * MAR value
 * MBR value
 * IBR value
 * IR value
 * AC value
 * MQ value
 * 
 * Followed by any one of the following in any order repeated any number of times
 * 
 * 1) Operation and changing registers
 * Operation
 * PC value
 * MAR value
 * MBR value
 * IBR value
 * IR value
 * AC value
 * MQ value
 * 
 * 2) Changing the stage
 * "STAGE: " Stage Name
 * 
 * 3) Reading from memory
 * Operation
 * "R"
 * Position Value
 * 
 * 4) Writing to memory
 * Operation 
 * "W"
 * position Value
 * 
 * In the end the following keywords must be there.
 * 
 * "END"
 * Final value to be printed.
 * 
 * @author Aryan Bansal and Abhirath Adamane
 * @version 1.0
 * @date 20/01/24
 */

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;

public class IMT2023029_OutputReader
{
	private BufferedReader in;	//BufferedReader object for reading from file

	/*
	 * Creates a BufferedReader specified by the file path given in the file.
	 * @param file : the file path.
	 */
	public IMT2023029_OutputReader(String file)
	{
		try
		{
			this.in = new BufferedReader(new FileReader(new File(file)));
		}
		catch(IOException e)
		{
			System.err.println("No Such file " + file);
			e.printStackTrace();
			System.exit(1);
		}
	}
	
	/*
	 * Returns the starting input.
	 * Consists of an array starting with the stage followed by the rest of the elements.
	 * @return ArrayList<String> the list of elements.
	 */
	public ArrayList<String> getStartingInput()
	{
		ArrayList<String> list = new ArrayList<>();

		try
		{
			for(int i = 0; i < 8; i++)
				list.add(in.readLine());
		}
		catch(IOException e)
		{
			System.err.println("No more lines");
			e.printStackTrace();
			System.exit(1);
		}

		return list;
	}

	/*
	 * Returns the next value.
	 * 1) If there is a stage change, then length of list is 1.
	 * 2) If the program is to end, then null list is returned.
	 * 3) If the program wants to read from memory, then operation and "position value" are returned (size 2).
	 * 4) If the program wants to write to memory, then opertion, null, and "position value" are returned (size 3).
	 * 5) Otherwise if the program wants to change the registers,  then list of lenght 8 is returned consisting of
	 *    opcodes and the final values of the registers.
	 * 
	 * @return ArrayList<String> the list following the format given above.
	 */
	public ArrayList<String> getNextValues()
	{
		ArrayList<String> list = new ArrayList<>();

		try
		{
			String next = in.readLine();
			if(next.startsWith("STAGE: "))
			{
				list.add(next);
				return list;
			}
			else if(next.startsWith("END"))
			{
				return null;
			}

			list.add(next);
			next = in.readLine();

			if(next.startsWith("R"))
			{
				list.add(in.readLine());
				return list;
			}
			else if(next.startsWith("W"))
			{
				list.add(in.readLine());
				list.add(null);
				return list;
			}
			else
			{
				list.add(next);

				for(int i = 0; i < 6; i++)
				{
					list.add(in.readLine());
				}
			}
		}
		catch(IOException e)
		{
			System.err.println("No more lines");
			e.printStackTrace();
			System.exit(1);
		}
		return list;
	}

	/*
	 * Is for reading the last two entries "END" and final value.
	 * After this, the bufferedreader is closed.
	 */
	public String readEnding()
	{
		String value = null;
		try
		{
			value = in.readLine();
			in.close();
		}
		catch(IOException e)
		{
			System.err.println("No more lines");
			e.printStackTrace();
			System.exit(1);
		}

		return value;
	}
}
