using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace InstructionLibrary.Models {
    public enum Registers {
        r0  = 0x0,
        r1  = 0x1,
        r2  = 0x2,
        r3  = 0x3,
        r4  = 0x4,
        r5  = 0x5,
        r6  = 0x6,
        r7  = 0x7,
        r8  = 0x8,
        r9  = 0x9,
        r10 = 0xA,
        r11 = 0xB,
        r12 = 0xC,
        r13 = 0xD,
        r14 = 0xE,
        r15 = 0xF
    }
    public enum RegisterType {
        Hardwired_Zero,
        Temporary,
        Save,
        Global_Pointer,
        Stack_Pointer,
        Frame_Pointer,
        Return_Address,
        Function_Args
    }
    public static class RegisterTypes {
        public static RegisterType GetType(this Registers register) {
            switch (register) {
                case Registers.r0:
                    return RegisterType.Hardwired_Zero;
                case Registers.r1:
                    return RegisterType.Temporary;
                case Registers.r2:
                    return RegisterType.Temporary;
                case Registers.r3:
                    return RegisterType.Temporary;
                case Registers.r4:
                    return RegisterType.Temporary;
                case Registers.r11:
                    return RegisterType.Global_Pointer;
                case Registers.r12:
                    return RegisterType.Stack_Pointer;
                case Registers.r13:
                    return RegisterType.Frame_Pointer;
                case Registers.r14:
                    return RegisterType.Return_Address;
                case Registers.r15:
                    return RegisterType.Function_Args;
                default:
                    return RegisterType.Save;
            }
        }
    }
}
