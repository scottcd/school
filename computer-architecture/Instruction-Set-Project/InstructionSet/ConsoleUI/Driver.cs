using System;
using System.Collections.Generic;
using InstructionLibrary;
using InstructionLibrary.Models.Instructions;
using InstructionLibrary.Interfaces;
using ExecutionLibrary;
using InstructionLibrary.Models;


namespace ConsoleUI {
    public class Driver {
        public static void Main(string[] args) {
            
            MachineState state = new MachineState();


            Console.WriteLine("Input (AS BINARY STREAM):\n\n");

            List<IInstruction> instructions = GetInstructions();

            foreach (var instruction in instructions) {
                state.CurrentInstruction = instruction;
                Executor.SwitchSelect(instruction, state);
                Console.WriteLine(instruction);
            }
            Console.WriteLine(state);
        }


        public static List<IInstruction> GetInstructions() {
            string hexString = Console.ReadLine();

            //var instructionValues = Decoder.ParseToInt(hexString);
            return Decoder.DecodeHex(instructionValues);
        }
    }
}