"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # pass
        #initialize
        self.ram = [0] * 256 #bytes of memory (256)
        self.reg = [0] * 8 # amount of registers that store data (8)
        self.pc = 0 #the counter, sorta like a pointer

    def ram_read(self, MAR): #MAR is memory address register holds memory / position
        return self.ram[MAR]

    def ram_write(self, MAR, MDR): #MAR memory data register is data getting written into MAR LS8.spec file
        self.ram[MAR] = MDR

    def load(self):
        """Load a program into memory."""

        # address = 0

        # # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        # pass

        running = True

        instructions = {
            0b10000010: 'LDI', # LDI R0,8
            0b01000111: 'PRN', # PRN R0
            0b00000001: 'HLT', # HLT
        }

        while running:
            i = self.ram[self.pc] #grabbing the index from ram(memory)from comp.py notepad
            
            if instructions[i] == 'LDI':
                reg_num = self.ram[self.pc + 1] #set up register
                value = self.ram[self.pc + 2] #what does this mean from guided project??
                self.reg[reg_num] = value #save value to register
                #value = 8 from the counter pc getting to that index
                self.pc +=3

            elif instructions[i] == 'PRN':
                #print register
                reg_num = self.ram[self.pc + 1]
                print(self.reg[reg_num])

                self.pc +=2

            elif instructions[i] == 'HLT':
                #this is the halt
                running = False

            else:
                print(f"Unknown instruction {i}")








new_cpu = CPU()
new_cpu.load()
new_cpu.run()


#ls8-spec and training kit
#ldi registers
#hlt alts cpu exists emulator

#ram read and write in TK

