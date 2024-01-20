import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;

public class OutputReader
{
	private BufferedReader in;

	public OutputReader(String file)
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