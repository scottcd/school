using InstructionLibrary.Interfaces;
using InstructionLibrary.Models.Instructions;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace InstructionLibrary.Models.Instructions {
    public class H_Instruction : IInstruction {
        public Opcodes Opcode { get; set; }
        public OpcodeType OpcodeType { get; set; }
        public int[] Instruction { get; set; }

        public H_Instruction(int[] instruction, Opcodes opcode, OpcodeType opcodeType) {
            Opcode = opcode;
            OpcodeType = opcodeType;
            Instruction = instruction;
        }

        public override string ToString() {
            return $"{Opcode}";
        }
    }
}
