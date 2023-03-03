using InstructionLibrary.Interfaces;
using InstructionLibrary.Models;
using InstructionLibrary.Models.Instructions;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace ExecutionLibrary {
    public static class Executor {
        public static void SwitchSelect(IInstruction instruction, MachineState state) {
            switch (instruction.Opcode) {
                case Opcodes.add:
                    Add((R_Instruction)instruction, state);
                    break;
               case Opcodes.sub:
                    Sub((R_Instruction)instruction, state);
                    break;
               case Opcodes.and:
                    And((R_Instruction)instruction, state);
                        break;
               case Opcodes.or:
                    Or((R_Instruction)instruction, state);
                    break;
               case Opcodes.nor:
                    Nor((R_Instruction)instruction, state);
                    break;
               case Opcodes.lw:
                    Lw((I_Instruction)instruction, state);
                    break;
               case Opcodes.sw:
                    Sw((I_Instruction)instruction, state);
                    break;
               case Opcodes.beq:
                    Beq((I_Instruction)instruction, state);
                    break;
               case Opcodes.mul:
                    Mul((I_Instruction)instruction, state);
                    break;
               case Opcodes.addi:
                    Addi((I_Instruction)instruction, state);
                    break;
               case Opcodes.andi:
                    Andi((I_Instruction)instruction, state);
                    break;
               case Opcodes.ori:
                    Ori((I_Instruction)instruction, state);
                    break;
               case Opcodes.sll:
                    Sll((I_Instruction)instruction, state);
                    break;
               case Opcodes.srl:
                    Srl((I_Instruction)instruction, state);
                    break;
               case Opcodes.xor:
                    Xor((R_Instruction)instruction, state);
                    break;
                default:
                    //Add((R_Instruction)instruction, state);
                    break;
            }
        }

        private static void Xor(R_Instruction instruction, MachineState state)
        {
            int destRegister = (int)instruction.DestinationRegister;
            int sourceRegister1 = (int)instruction.SourceRegister1;
            int sourceRegister2 = (int)instruction.SourceRegister2;

            state.MachineRegisters[(Registers)destRegister] = state.MachineRegisters[(Registers)sourceRegister1]
                                                              ^ state.MachineRegisters[(Registers)sourceRegister2];
        }

        private static void Srl(I_Instruction instruction, MachineState state)
        {
            int destRegister = (int)instruction.DestinationRegister;
            int sourceRegister1 = (int)instruction.SourceRegister1;
            int sourceImmediate = (int)instruction.Immediate;

            state.MachineRegisters[(Registers)destRegister] = state.MachineRegisters[(Registers)sourceRegister1]
                                                              >> sourceImmediate;
        }

        private static void Sll(I_Instruction instruction, MachineState state)
        {
            int destRegister = (int)instruction.DestinationRegister;
            int sourceRegister1 = (int)instruction.SourceRegister1;
            int sourceImmediate = (int)instruction.Immediate;

            state.MachineRegisters[(Registers)destRegister] = state.MachineRegisters[(Registers)sourceRegister1]
                                                              << sourceImmediate;
        }

        private static void Ori(I_Instruction instruction, MachineState state)
        {
            int destRegister = (int)instruction.DestinationRegister;
            int sourceRegister1 = (int)instruction.SourceRegister1;
            int sourceImmediate = (int)instruction.Immediate;

            state.MachineRegisters[(Registers)destRegister] = state.MachineRegisters[(Registers)sourceRegister1]
                                                              | sourceImmediate;
        }

        private static void Andi(I_Instruction instruction, MachineState state)
        {
            int destRegister = (int)instruction.DestinationRegister;
            int sourceRegister1 = (int)instruction.SourceRegister1;
            int sourceImmediate = (int)instruction.Immediate;

            state.MachineRegisters[(Registers)destRegister] = state.MachineRegisters[(Registers)sourceRegister1]
                                                              & sourceImmediate;
        }

        private static void Addi(I_Instruction instruction, MachineState state)
        {
            int destRegister = (int)instruction.DestinationRegister;
            int sourceRegister1 = (int)instruction.SourceRegister1;
            int sourceImmediate = (int)instruction.Immediate;

            state.MachineRegisters[(Registers)destRegister] += state.MachineRegisters[(Registers)sourceRegister1]
                                                              + sourceImmediate;
        }

        private static void Mul(I_Instruction instruction, MachineState state)
        {
            int destRegister = (int)instruction.DestinationRegister;
            int sourceRegister1 = (int)instruction.SourceRegister1;
            int sourceImmediate = (int)instruction.Immediate;

            state.MachineRegisters[(Registers)destRegister] = state.MachineRegisters[(Registers)sourceRegister1]
                                                              * sourceImmediate;
        }
        public static void Add(R_Instruction instruction, MachineState state) {
            int destRegister = (int)instruction.DestinationRegister;
            int sourceRegister1 = (int)instruction.SourceRegister1;
            int sourceRegister2 = (int)instruction.SourceRegister2;

            state.MachineRegisters[(Registers)destRegister] =    state.MachineRegisters[(Registers)sourceRegister1]
                                                              +  state.MachineRegisters[(Registers)sourceRegister2];
        }

        public static void Sub(R_Instruction instruction, MachineState state)
        {
            int destRegister = (int)instruction.DestinationRegister;
            int sourceRegister1 = (int)instruction.SourceRegister1;
            int sourceRegister2 = (int)instruction.SourceRegister2;

            state.MachineRegisters[(Registers)destRegister] = state.MachineRegisters[(Registers)sourceRegister1]
                                                              - state.MachineRegisters[(Registers)sourceRegister2];
        }

        public static void And(R_Instruction instruction, MachineState state)
        {
            int destRegister = (int)instruction.DestinationRegister;
            int sourceRegister1 = (int)instruction.SourceRegister1;
            int sourceRegister2 = (int)instruction.SourceRegister2;

            state.MachineRegisters[(Registers)destRegister] = state.MachineRegisters[(Registers)sourceRegister1]
                                                              & state.MachineRegisters[(Registers)sourceRegister2];
        }

        public static void Or(R_Instruction instruction, MachineState state)
        {
            int destRegister = (int)instruction.DestinationRegister;
            int sourceRegister1 = (int)instruction.SourceRegister1;
            int sourceRegister2 = (int)instruction.SourceRegister2;

            state.MachineRegisters[(Registers)destRegister] = state.MachineRegisters[(Registers)sourceRegister1]
                                                              | state.MachineRegisters[(Registers)sourceRegister2];
        }

        //not fully done
        public static void Nor(R_Instruction instruction, MachineState state)
        {
            int destRegister = (int)instruction.DestinationRegister;
            int sourceRegister1 = (int)instruction.SourceRegister1;
            int sourceRegister2 = (int)instruction.SourceRegister2;

            
            state.MachineRegisters[(Registers)destRegister] = state.MachineRegisters[(Registers)sourceRegister1]
                                                              ^ state.MachineRegisters[(Registers)sourceRegister2];
            //state.MachineRegisters[(Registers)destRegister] = state.MachineRegisters[(Registers)destRegister]
        }

        
        public static void Lw(I_Instruction instruction, MachineState state)
        {
            int destRegister = (int)instruction.DestinationRegister;
            int sourceRegister1 = (int)instruction.SourceRegister1;
            int sourceImmediate = (int)instruction.Immediate;

            int memOffset = sourceRegister1 + sourceImmediate;

            int lWord = BitConverter.ToInt16(state.memory, memOffset);

            state.MachineRegisters[(Registers)destRegister] = lWord;
        }

        
        public static void Sw(I_Instruction instruction, MachineState state)
        {
            int destRegister = (int)instruction.DestinationRegister;
            int sourceRegister1 = (int)instruction.SourceRegister1;
            int sourceImmediate = (int)instruction.Immediate;

            int memOffset = sourceRegister1 + sourceImmediate;

            short var = (short)state.MachineRegisters[(Registers)destRegister];
            byte low = (byte)(var & 0x0f);  // Take just the lowest 8 bits.
            byte high = (byte)(var >> 8);

            state.memory[memOffset] = low;
            state.memory[memOffset+1] = high;

        }
        //not done
        public static void Beq(I_Instruction instruction, MachineState state)
        {
            int destRegister = (int)instruction.DestinationRegister;
            int sourceRegister1 = (int)instruction.SourceRegister1;
            int sourceImmediate = (int)instruction.Immediate;

            int memOffset = sourceRegister1 + sourceImmediate;


            //state.MachineRegisters[(Registers)destRegister] = mem.LoadMemory(memOffset);
        }
                                                             

    }
}
