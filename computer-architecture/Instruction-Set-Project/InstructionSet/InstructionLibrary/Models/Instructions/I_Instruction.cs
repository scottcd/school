using InstructionLibrary.Interfaces;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace InstructionLibrary.Models.Instructions {
    public class I_Instruction :IInstruction{
        public Opcodes Opcode { get; set; }
        public int[] Instruction { get; set; }
        public Registers DestinationRegister { get; set; }
        public Registers SourceRegister1 { get; set; }
        public int Immediate { get; set; }
        public OpcodeType OpcodeType { get; set; }

        public I_Instruction(int[] instruction, Opcodes opcode, OpcodeType opcodeType) {
            Opcode = opcode;
            OpcodeType = opcodeType;
            DestinationRegister = (Registers)instruction[1];
            SourceRegister1 = (Registers)instruction[2];
            Immediate = instruction[3];
            Instruction = instruction;
        }
        public override string ToString() {
            return $"{Opcode}\t{DestinationRegister}\t{SourceRegister1}\t#{Immediate}";
        }
    }
}
