using System;
using System.Runtime.InteropServices;

namespace MemoryLibrary
{
    public class MemoryAccess
    {


        private byte[] memory;
        private int startPtr = 0;
        private int currentPtr;


        public MemoryAccess()
        {
            memory = new byte[1048576];
            currentPtr = startPtr;


        }



        public void StoreMemory(int address, byte[] value)
        {
            currentPtr = address;
            value.CopyTo(memory, currentPtr);

        }

        public byte[] LoadMemory(int address)
        {
            currentPtr = address;
            byte[] temp = new byte[2];

            for(int i = 0; i < 2; i++)
            {
                temp[i] = memory[currentPtr];
                currentPtr++;
            }

            return temp;
        }


    }
}
