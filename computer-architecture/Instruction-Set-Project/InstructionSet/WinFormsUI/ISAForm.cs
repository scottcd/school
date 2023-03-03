using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using InstructionLibrary;
using InstructionLibrary.Interfaces;
using InstructionLibrary.Models;
using InstructionLibrary.Models.Instructions;


namespace WinFormsUI {
    public partial class ISAForm : Form {
        protected MachineState state;

        private int currentInstruction = 0;
        protected List<IInstruction> instructions;

        private List<int> lint = new List<int>();

    

        public ISAForm() {
            InitializeComponent();
            //inputBox.Text = "1A EE 4A A1 2A AA A3 5F 1A EE 4A A1 2A AA A3 5F 1A EE 4A A1 2A AA A3 5F 00";

            CompileButton.Enabled = false;
            CompileButton.FlatStyle = FlatStyle.System;
            stateBox.Text = $"{state}";

            
        }

        //simple event to prevent step through if the code hasn't been compiled
        private void inputBox_TextChanged(object sender, EventArgs e)
        {
            NextButton.Enabled = false;
            NextButton.FlatStyle = FlatStyle.System;
        }//end inputBox_TextChanged(object, EventArgs)

        private void CompileButton_Click(object sender, EventArgs e) {
            state = new MachineState();
            if(inputBox.Text.Length != 0)
            {

                //var instructionValues = InstructionLibrary.Decoder.ParseToInt(inputBox.Text);

                instructions = InstructionLibrary.Decoder.DecodeHex(lint.ToArray());
                string output = "";
                int i = 0;
                foreach (var instruction in instructions) {
                    output += i.ToString("X4") + "\t";
                    state.CurrentInstruction = instruction;
                    //ExecuteInstruction.SwitchSelect(instruction, state);
                    output += $"{instruction}\n";
                    i += 4;
                }

                outputBox.Text = output;
                stateBox.Text = $"{state}";
                NextButton.Enabled = true;
                RunButton.Enabled = true;

                RunButton.FlatStyle = FlatStyle.Popup;
                NextButton.FlatStyle = FlatStyle.Popup;
                currentInstruction = 0;                
            }

        }

        //event that executes the next step of the compiled code
        //gets the current instruction from the instructions list then
        //updates the form accordingly.
        private void RunButton_Click(object sender, EventArgs e) {
            state = new MachineState();
            foreach (var instruction in instructions) {
                state.CurrentInstruction = instruction;
                Executor.SwitchSelect(instruction, state);
                currentInstruction = state.MachineRegisters[(Registers)11] / 4;
            }

            stateBox.Text = $"{state} \nResults: {state.MachineRegisters[(Registers)15]}";

            //disable the NextButton and reset currentInstruction
            NextButton.Enabled = false;
            NextButton.FlatStyle = FlatStyle.System;
            currentInstruction = 0;
        }//end RunButton_Click(object, EventArgs)

        //event that executes the next step of the compiled code
        //gets the current instruction from the instructions list then
        //updates the form accordingly.
        private void NextButton_Click(object sender, EventArgs e)
        {
            state.CurrentInstruction = instructions[currentInstruction];
            Executor.SwitchSelect(instructions[currentInstruction], state);
            stateBox.Text = $"{state}";
            currentInstruction = state.MachineRegisters[(Registers)11] / 4;

            //prevents step through if the end
            //of the instructions list has been reached.
            if (currentInstruction >= instructions.Count) 
            {
                NextButton.Enabled = false;
                NextButton.FlatStyle = FlatStyle.System;
            }//end if()
        }//end NextButton_Click(object, EventArgs)

        private void LoadFileButton_Click(object sender, EventArgs e)
        {
            if (this.openFileDialog1.ShowDialog() == DialogResult.OK)
            {

                lint.Clear();
                inputBox.Text = "";

                var fileStream = this.openFileDialog1.OpenFile();

                int[] parsedHex;

                BinaryReader binReader = new BinaryReader(fileStream);

                int i = 0;
                int instruct = 0;

                while (true)
                {
                    byte newByte = binReader.ReadByte();
                    byte lowerNibble = (byte)(newByte & 0x0f);  // Take just the lowest 8 bits.
                    byte higherNible = (byte)(newByte >> 4);

                    lint.Add((int)higherNible);

                    inputBox.Text += higherNible.ToString("X");

                    if (i == instruct)
                    {
                        if (higherNible == 0)
                        {
                            lint.Add((int)lowerNibble);
                            inputBox.Text += lowerNibble.ToString("X") + " ";
                            break;
                        }
                        instruct += 4;

                    }

                    i++;
                    lint.Add((int)lowerNibble);

                    inputBox.Text += lowerNibble.ToString("X") + " ";
                    i++;

                }

                
            }
            RunButton.Enabled = false;
            RunButton.FlatStyle = FlatStyle.System;
            NextButton.Enabled = false;
            NextButton.FlatStyle = FlatStyle.System;
            CompileButton.Enabled = true;
            CompileButton.FlatStyle = FlatStyle.Popup;
        }

        private void SaveFileButton_Click(object sender, EventArgs e)
        {
            if (this.saveFileDialog1.ShowDialog() == DialogResult.OK)
            {
                File.WriteAllText(this.saveFileDialog1.FileName, inputBox.Text);
            }
        }

    }
}
