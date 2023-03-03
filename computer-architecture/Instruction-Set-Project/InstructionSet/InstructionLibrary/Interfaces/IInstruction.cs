using InstructionLibrary.Models;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace InstructionLibrary.Interfaces {
    public interface IInstruction {
        public Opcodes Opcode { get; set; }
        public int[] Instruction { get; set; }
        public OpcodeType OpcodeType { get; set; }
    }
}
