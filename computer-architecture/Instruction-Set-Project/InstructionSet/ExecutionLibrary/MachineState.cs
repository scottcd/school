using InstructionLibrary.Interfaces;
using InstructionLibrary.Models;
using System;
using System.Collections.Generic;

namespace ExecutionLibrary {
    public class MachineState {
        public Dictionary<Registers, int> MachineRegisters { get; set; }
        public byte[] memory;



        public IInstruction CurrentInstruction { get; set; }

        public MachineState() {
            MachineRegisters = new Dictionary<Registers, int>{
                {Registers.r0, 0 },
                {Registers.r1, 0 },
                {Registers.r2, 0 },
                {Registers.r3, 0 },
                {Registers.r4, 0 },
                {Registers.r5, 0 },
                {Registers.r6, 0 },
                {Registers.r7, 0 },
                {Registers.r8, 0 },
                {Registers.r9, 0 },
                {Registers.r10, 0 },
                {Registers.r11, 0 },
                {Registers.r12, 0 },
                {Registers.r13, 0 },
                {Registers.r14, 0 },
                {Registers.r15, 0 },
            }; 
            memory = new byte[1048576];
        }


        public override string ToString() {
            string output = "";

            foreach (var reg in MachineRegisters) {
                output += $"register: {reg.Key} value: {reg.Value}\n";
            }
            output += $"Current Instruction: {CurrentInstruction}";


            return output;
        }
    }

}
