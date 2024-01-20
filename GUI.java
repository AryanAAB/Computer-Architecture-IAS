/*
 * This class is for presenting the different instructions in a graphical user interface.
 * It shows the current stage (fetch, decode, execute, etc), the memory line that is being
 * read/written (if any), the operation that is being performed (if any), and the current 
 * values of the registers PC, MAR, MBR, IBR, IR, AC, and MQ. If the color of the registers
 * is red, then that means that those values were updated at that time. Otherwise, register
 * color would be blue. 
 * 
 * @author Aryan Bansal and Abhirath Adamane
 * @version 1.0
 * @date 20/01/24
 */

import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Dimension;
import java.awt.Font;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.font.FontRenderContext;
import java.awt.font.TextLayout;
import java.util.ArrayList;
import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.SwingConstants;

public class GUI extends JFrame
{
    public static final Font DEFAULT_FONT = new Font("Arial", Font.BOLD, 16); //Default font for all the texts in the GUI

    private static final Manager manager = new Manager();                               //Stores the JPanel object added to this frame. 

    /*
     * Creates a Frame with the tile IAS Machine. 
     * The size of the frame is 800 by 400 and is not resizable.
     */
    public GUI()
    {
        super("IAS Machine");

        this.setPreferredSize(new Dimension(800, 400));

        this.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        this.setResizable(false);

        this.add(manager);

        this.pack();
        this.setLocationRelativeTo(null);
    }

    /*
     * Runs the program
     * @param args : the in-line arguments.
     */
    public static void main(String [] args)
    {
        GUI gui = new GUI();
        manager.setStartingValues();

        gui.setVisible(true);
    }

    /*
     * @return Manager object
     */
    public static Manager getManager()
    {
        return manager;
    }
}

class Manager extends JPanel
{
    private Stage stage;    //Stores the stage or the JPanel that is on the North
    private Button button;  //Stores the button next or the JPanel that is on the South
    private Center center;  //Stores the main content or the JPanel that is in the Center
    private EAST east;      //Stores the components that are on the East

    public static final Color BACKGROUND_COLOR = Color.WHITE; //Background color

    /*
     * Creates a Manager class with White background. 
     * The layout of this JPanel is of BorderLayout.
     * It adds the current Stage to the North, Button to the South,
     * The contents of the center in the Center, and the contents 
     * that would go to the east. 
     */
    public Manager()
    {
        this.setBackground(BACKGROUND_COLOR);
        this.setLayout(new BorderLayout());
        
        this.stage = new Stage();
        this.button = new Button();
        this.center = new Center();
        this.east = new EAST();

        this.add(this.stage, BorderLayout.NORTH);
        this.add(this.button, BorderLayout.SOUTH);
        this.add(this.east, BorderLayout.EAST);
        this.add(this.center, BorderLayout.CENTER);
    }

    /*
     * Updates the current stage.
     * @param value : the new stage. 
     */
    public void updateStage(String value)
    {
        this.stage.updateStage(value);
    }

    /*
     * Updates the register values.
     * @param values : An arraylist consisting of the 7 values of the registers.
     */
    public void updateRegisters(ArrayList<String> values)
    {
        this.east.update(values);
    }

    /*
     * Updates the current operation.
     * @param value : The current operation. 
     */
    public void updateOperation(String value)
    {
        this.center.updateOperation(value);
    }

    /*
     * Updates memory to read.
     * @param value : The location and the value of the format "location value"
     */
    public void read(String value)
    {
        this.center.read(value);
    }

    /*
     * Updates memory to write.
     */
    public void write(String value)
    {
        this.center.write(value);
    }

    /*
     * Sets the initial values of the registers and the cycle. 
     */
    public void setStartingValues()
    {
        this.button.setStartingValues();
    }

    /*
     * Opens a pop up after which the program terminates. 
     * @param value : The message to show in the dialog.
     */
    public void popUp(String value)
    {
        JOptionPane.showMessageDialog(this, value, "Final Answer", JOptionPane.INFORMATION_MESSAGE);
        System.exit(1);
    }

    /*
     * Resets the value of operation, registers (to their current values), and the memory. 
     */
    public void reset()
    {
        this.updateOperation("None");
        this.center.reset();
        this.updateRegisters(null);
    }
}

class Button extends JButton implements ActionListener
{
    private OutputReader read;                                  //Stores a reader object which reads the output file.

    public static final String FILE_PATH = "Output.txt";        //File Path of the output file.

    public static final Color BACKGROUND_COLOR = Color.GREEN;   //Background color.

    /*
     * Creates a Next Button. If you click on it, then the next step is executed. 
     * The background color of this button is Green.
     */
    public Button()
    {
        this.setBackground(BACKGROUND_COLOR);
        this.setFont(GUI.DEFAULT_FONT);
        this.setText("NEXT");

        read = new OutputReader("Output.txt");

        this.addActionListener(this);
    }

    /*
     * Sets the starting values of the GUI. 
     */
    public void setStartingValues()
    {
        ArrayList<String> list = read.getStartingInput();
        GUI.getManager().updateStage(list.remove(0));
        GUI.getManager().updateRegisters(list);
    }

    /*
     * Called when the button is clicked.
     * @param e : The Action Event Generated.
     */
    @Override
    public void actionPerformed(ActionEvent e) 
    {
        ArrayList<String> list = read.getNextValues();
        
        GUI.getManager().reset();

        //List is null impliex exit.
        if(list == null)
        {
            GUI.getManager().popUp(read.readEnding());
        }
        //Size is one implies that there is a state change.
        else if(list.size() == 1)
        {
            GUI.getManager().updateStage(list.remove(0));
            GUI.getManager().updateOperation("Changing stage");
        }
        else
        {
            GUI.getManager().updateOperation(list.remove(0));

            //Size is 1 after removal implies that this is a read instruction.
            if(list.size() == 1)
            {
                GUI.getManager().read(list.remove(0));
            }
            //Size is 2 after removal implies that this is a write instruction. 
            else if(list.size() == 2)
            {
                GUI.getManager().write(list.remove(0));
            }
            //Size is greater than 2 (assumed to be 7) implies that this is a normal register updation instruction.
            else
            {
                GUI.getManager().updateRegisters(list);
            }
        }
    }
}

class Stage extends JPanel
{
    private JLabel label;                                       //Label which stores the value of the stage

    public static final Color BACKGROUND_COLOR = Color.YELLOW; //Background color

    /*
     * Creates a stage object which stores the current stage that the processor is on.
     * The background color is Yellow.
     */
    public Stage()
    {
        this.setBackground(BACKGROUND_COLOR);
        this.label = new JLabel("Stage : ");
        this.label.setFont(GUI.DEFAULT_FONT);
        this.add(label);
    }

    /*
     * Changes the value of stage to that specified by str.
     * @param str : the new stage.
     */
    public void updateStage(String str)
    {
        this.label.setText(str);
    }
}

class Center extends JPanel
{
    private Memory memory;           //Stores the memory object
    private Operation operation;    //Stores the current operation object

    /*
     * Creates a center class object that manages everything in the center of the panel.
     * It uses another BorderLayout to put the memory field on the top and the operation 
     * field in the middle. 
     */
    public Center()
    {
        this.setLayout(new BorderLayout());

        this.memory = new Memory();
        this.operation = new Operation();

        this.add(this.memory, BorderLayout.NORTH);
        this.add(this.operation, BorderLayout.CENTER);
    }

    /*
     * Resets the memory.
     */
    public void reset()
    {
        this.memory.reset();
    }
    
    /*
     * Reads from memory.
     * @param value the memory read value "position value"
     */
    public void read(String value)
    {
        this.memory.read(value);
    }

    /*
     * Writes from memory.
     * @param value the memory write value "position value"
     */
    public void write(String value)
    {
        this.memory.write(value);
    }

    /*
     * Updates the operation that you are performing.
     * @param value the new operation.
     */
    public void updateOperation(String value)
    {
        this.operation.updateOperation(value);
    }
}

class Memory extends JPanel
{
    private JLabel label;                                                           //Stores the memory that is read/written.

    public static final String MESSAGE1 = "There is no memory being loaded.";       //Message when there is no memory being read/written.
    public static final String MESSAGE2 = "Memory is being read at location : ";    //Message when there is memory being read.
    public static final String MESSAGE3 = "Memory that is written at location : ";  //Message when there is memory being written.
    
    public static final Color BACKGROUND_COLOR = Color.CYAN;                        //Background color

    /*
     * Creates a memory object with background color as Cyan. 
     */
    public Memory()
    {
        this.setBackground(BACKGROUND_COLOR);

        String str = MESSAGE1;

        this.label = new JLabel(str);
        this.label.setFont(GUI.DEFAULT_FONT);
        this.add(label);
    }
    
    /*
     * Resets the memory object to print Message 1. 
     */
    public void reset()
    {
        this.label.setText(MESSAGE1);

    }

    /*
     * Reads value and prints Message 2.
     * @param value : must be of format "position value"
     */
    public void read(String value)
    {
        this.label.setText(MESSAGE2 + value.substring(0, value.indexOf(" ")) + " : " + value.substring(value.indexOf(" ") + 1));
    }

    /*
     * Writes value and prints Message 3.
     * @param value : must be of format "position value"
     */
    public void write(String value)
    {
        this.label.setText(MESSAGE3 + value.substring(0, value.indexOf(" ")) + " : " + value.substring(value.indexOf(" ") + 1));
    }
}

class Operation extends JPanel
{
    private JLabel label;                                       //Stores the current operation

    public static final Color BACKGROUND_COLOR = Color.ORANGE;  //Stores the Background Color

    /*
     * Creates an operation object that is of color Orange.
     */
    public Operation()
    {
        this.setBackground(BACKGROUND_COLOR);

        this.label = new JLabel("Operation : None");
        this.label.setFont(GUI.DEFAULT_FONT);
        this.add(label);
    }

    /*
     * Updates operation to the new operation given.
     * @param value : the new operation.
     */
    public void updateOperation(String value)
    {
        String str = this.label.getText();

        this.label.setText(str.substring(0, str.indexOf(": ") + 2) + value);
    }
}

class EAST extends JPanel
{
    private EASTCenter center;                                  //Stores the values of the registers.

    public static final Color BACKGROUND_COLOR = Color.MAGENTA; //Background color.

    /*
     * Creates the elements that are going to be placed in the east. 
     */
    public EAST()
    {
        this.setBackground(BACKGROUND_COLOR);

        JLabel label = new JLabel("REGISTERS", SwingConstants.CENTER);
        label.setFont(GUI.DEFAULT_FONT);
        
        this.setLayout(new BorderLayout());
        this.add(label, BorderLayout.NORTH);

        this.center = new EASTCenter();
        this.add(center, BorderLayout.CENTER);
    }

    /*
     * Updates the value of the registers given by the ArrayList.
     * The list must be of length 7. The first one is PC, MAR,
     * MBR, IBR, IR, AC, and MQ.
     * @param values : the list of numbers.
     */
    public void update(ArrayList<String> values)
    {
        center.updateRegisters(values);
    }
}

class EASTCenter extends JPanel
{
    private String [] labels;                                                                               //Stores the labels
    private boolean [] changed;                                                                             //Stores if the registers were changed or not.
    public static final String [] values = {"PC: ", "MAR: ", "MBR: ", "IBR: ", "IR: ", "AC: ", "MQ: "};     //Stores the constants (the registers used)
    
    public static final Color BACKGROUND_COLOR = Color.WHITE;                                               //The background color
    public static final Color CHANGED_COLOR = Color.RED;                                                    //If register was changed
    public static final Color NORMAL_COLOR = Color.BLUE;                                                    //If register was not changed

    /*
     * Creates the EastCenter object which stores the register values.
     */
    public EASTCenter()
    {
        labels = new String[7];
        changed = new boolean[7];

        for(int i = 0; i < 7; i++)
        {
            labels[i] = values[i];
        }

        this.setPreferredSize(new Dimension(300, 100));
        this.setBackground(BACKGROUND_COLOR);
    }

    /*
     * Draws all the components onto the screen.
     * @param g : Graphics object.
     */
    @Override
    protected void paintComponent(Graphics g)
    {
        super.paintComponent(g);

        g.setFont(GUI.DEFAULT_FONT);
        
        Graphics2D g2d = (Graphics2D) g; //Castes g to a 2DGraphics object and uses it to draw the registers perfectly.
        FontRenderContext frc = g2d.getFontRenderContext();
        
        int y = 20;
        int x = 20;
        for(int i = 0; i < 7; i++)
        {
            if(!this.changed[i])
                g.setColor(NORMAL_COLOR);
            else
                g.setColor(CHANGED_COLOR);

            TextLayout layout = new TextLayout(labels[i], GUI.DEFAULT_FONT, frc);   //used for drawing the object.
            layout.draw(g2d, x, y);
            y += 20;
        }
    }

    /*
     * Changes the register values based on the the list of registers given. The length is assumed to bbe of 7.
     * If a null list is given, then the red color of the registers is reset.
     * @param registers the values of the registers or null if you want to reset the values. 
     */
    public void updateRegisters(ArrayList<String> registers)
    {
        if(registers == null)
        {
            for(int i = 0; i < changed.length; i++)
            {
                changed[i] = false;
            }
        }
        else
        {
            for(int i = 0; i < registers.size(); i++)
            {
                String value = labels[i].substring(0, labels[i].indexOf(": ") + 2) + registers.get(i);
                
                if(labels[i].equals(value))
                    changed[i] = false;
                else
                {
                    changed[i] = true;
                    labels[i] = value;
                }
            }
        }
        repaint();
    }
}