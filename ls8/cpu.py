"""CPU functionality."""

import sys
SP = 7 #stack pointer

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # pass
        #initialize
        self.ram = [0] * 256 #bytes of memory (256)
        self.reg = [0] * 8 # amount of registers that store data (8)
        self.pc = 0 #the counter, sorta like a pointer
        

        self.reg[SP] = 0xF4

    def ram_read(self, MAR): #MAR is memory address register holds memory / position
        return self.ram[MAR]

    def ram_write(self, MAR, MDR): #MAR memory data register is data getting written into MAR LS8.spec file
        self.ram[MAR] = MDR

    def load(self):
        """Load a program into memory."""
        address = 0
        if len(sys.argv) != 2:
            print("usage: comp.py filename")
            sys.exit(1)

        try:
            with open(sys.argv[1]) as f:
                for line in f:
                    try:
                        line = line.split("#",1)[0]
                        line = int(line, 2)  # int() is base 10 by default, want it to start from line 2 because all zeros
                        self.ram[address] = line
                        address += 1
                    except ValueError:
                        pass

        except FileNotFoundError:
            print(f"Couldn't find file {sys.argv[1]}")
            sys.exit(1)


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
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b] #saving b into register a line 474 in ls8-spec

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
            0b10100010: 'MUL', # MUL R0,R1 (from mult.ls8 line 7)
            0b01000101: 'PUSH', # PUSH R0
            0b01000110: 'POP', # POP R0
            0b01010000: 'CALL', #CALL R1
            0b00010001: 'RET', # RET
            0b10100000: 'ADD', # ADD R0,R0
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

            elif instructions[i] == 'MUL':
                reg_a = self.ram[self.pc + 1]
                reg_b = self.ram[self.pc + 2]

                self.alu('MUL', reg_a, reg_b)
                self.pc += 3

            elif instructions[i] == 'PUSH':  # PUSH
            # decrement stack pointer
                self.reg[SP] -= 1

                self.reg[SP] &= 0xff  # keep R7 in the range 00-FF

                # get register value
                reg_num = self.ram[self.pc + 1]
                value = self.reg[reg_num]

          # Store in memory
                address_to_push_to = self.reg[SP]
                self.ram[address_to_push_to] = value

                self.pc += 2

            elif instructions[i] == 'POP':  # POP
          # Get value from RAM
                address_to_pop_from = self.reg[SP]
                value = self.ram[address_to_pop_from]

             # Store in the given register
                reg_num = self.ram[self.pc + 1]
                self.reg[reg_num] = value

                # Increment SP
                self.reg[SP] += 1

                self.pc += 2

            elif instructions[i] == 'CALL':
        # Get address of the next instruction
                return_addr = self.pc + 2

        # Push that on the stack
                self.reg[SP] -= 1
                address_to_push_to = self.reg[SP]
                self.ram[address_to_push_to] = return_addr

        # Set the PC to the subroutine address
                reg_num = self.ram[self.pc + 1]
                subroutine_addr = self.reg[reg_num]

                self.pc = subroutine_addr

            elif instructions[i] == 'RET':
        # Get return address from the top of the stack
                address_to_pop_from = self.reg[SP]
                return_addr = self.ram[address_to_pop_from]
                self.reg[SP] += 1

        # Set the PC to the return address
                self.pc = return_addr

            elif instructions[i] == 'ADD':
                reg_a = self.ram[self.pc + 1]
                reg_b = self.ram[self.pc + 2]
                self.alu('ADD', reg_a, reg_b)
                self.pc += 3
               


            else:
                print(f"Unknown instruction {i}")
                running = False








# new_cpu = CPU()
# new_cpu.load()
# new_cpu.run()


#ls8-spec and training kit
#ldi registers
#hlt alts cpu exists emulator

#ram read and write in TK


# python3 ls8.py examples/mult.ls8    this command is used in terminal and should return 72


#stack has a push and pop, take from stack.ls8? 

#bitwise operators

#python3 ls8.py examples/stack.ls8    day 3 command




#mult.ls8

# 10000010 # LDI R0,8 (Set the value of a register to an integer.)
# 00000000
# 00001000  (This is 8)
# 10000010 # LDI R1,9 (Set the value of a register to an integer.)
# 00000001
# 00001001    (This is 9)
# 10100010 # MUL R0,R1 (Multiply the values in two registers together and store the result in registerA.)
# 00000000
# 00000001
# 01000111 # PRN R0 (Print numeric value stored in the given register.)
# 00000000
# 00000001 # HLT (Halt the CPU (and exit the emulator).)






#stack.ls8

# 10000010 # LDI R0,1 (Set the value of a register to an integer.)
# 00000000      index 0
# 00000001 (1) #value stored at that index
# 10000010 # LDI R1,2 (Set the value of a register to an integer.)
# 00000001       index 1
# 00000010 (2)
# 01000101 # PUSH R0 (Push the value in the given register on the stack.)
# 00000000       index 0
# 01000101 # PUSH R1 (Push the value in the given register on the stack.)
# 00000001       index 1
# 10000010 # LDI R0,3 (Set the value of a register to an integer.)
# 00000000       index 0
# 00000011 (3)
# 01000110 # POP R0 (Pop the value at the top of the stack into the given register.)
# 00000000       index 0
# 01000111 # PRN R0 (Print numeric value stored in the given register.)
# 00000000       index 0
# 10000010 # LDI R0,4 (Set the value of a register to an integer.)
# 00000000       index 0
# 00000100 (4)
# 01000101 # PUSH R0 (Push the value in the given register on the stack.)
# 00000000       index 0
# 01000110 # POP R2 (Pop the value at the top of the stack into the given register.)
# 00000010       index 2
# 01000110 # POP R1 (Pop the value at the top of the stack into the given register.)
# 00000001       index 1
# 01000111 # PRN R2 (Print numeric value stored in the given register.)
# 00000010       index 2
# 01000111 # PRN R1 (Print numeric value stored in the given register.)
# 00000001       index 1
# 00000001 # HLT (Halt the CPU (and exit the emulator).)

# reg = [4, 1, 4]
# stack = []

# 2
# 4
# 1


# call.ls8

#0000 = 0
#0001 = 1
#0010 = 2
#0100 = 4
#1000 = 8
#1001 = 9
#0101 = 5


# 10000010 # LDI R1,MULT2PRINT
# 00000001  (index1, second spot)
# 00011000
# 10000010 # LDI R0,10
# 00000000   (index 0, first spot)
# 00001010
# 01010000 # CALL R1
# 00000001   (index 1, second spot)
# 10000010 # LDI R0,15
# 00000000
# 00001111
# 01010000 # CALL R1
# 00000001
# 10000010 # LDI R0,18
# 00000000
# 00010010
# 01010000 # CALL R1
# 00000001
# 10000010 # LDI R0,30
# 00000000
# 00011110
# 01010000 # CALL R1
# 00000001
# 00000001 # HLT
# # MULT2PRINT (address 24):
# 10100000 # ADD R0,R0
# 00000000
# 00000000
# 01000111 # PRN R0
# 00000000
# 00010001 # RET



#day 4 command python3 ls8.py examples/call.ls8



# 10000010 # LDI R0,10  (Set the value of a register to an integer.)
# 00000000 (index 0, spot 1)
# 00001010. (10)
# 10000010 # LDI R1,20 (Set the value of a register to an integer.)
# 00000001 (index 1, spot 2)
# 00010100 (20)
# 10000010 # LDI R2,TEST1 (Set the value of a register to an integer.)
# 00000010 (index 2, spot 3)
# 00010011 (19)
# 10100111 # CMP R0,R1 (Compare the values in two registers.)
# 00000000 (index 0, spot 1)
# 00000001 (1)
# 01010101 # JEQ R2 (If `equal` flag is set (true), jump to the address stored in the given register.)
# 00000010 (index 2, spot 3)
# 10000010 # LDI R3,1 (Set the value of a register to an integer.)
# 00000011 (index 3, spot 4)
# 00000001 (1)
# 01000111 # PRN R3 (Print numeric value stored in the given register.)
# 00000011 (index 3, spot 4)
# # TEST1 (address 19):
# 10000010 # LDI R2,TEST2 (Set the value of a register to an integer.)
# 00000010 (index 2, spot 3)
# 00100000 (32)
# 10100111 # CMP R0,R1 (Compare the values in two registers.)
# 00000000 (index 0, spot 1)
# 00000001 (1)
# 01010110 # JNE R2 (If `E` flag is clear (false, 0), jump to the address stored in the given register)
# 00000010 (index 2, spot 3)
# 10000010 # LDI R3,2 (Set the value of a register to an integer.)
# 00000011 (index 3, spot 4)
# 00000010 (2)
# 01000111 # PRN R3 (Print numeric value stored in the given register.)
# 00000011 (index 3, spot 4)
# # TEST2 (address 32):
# 10000010 # LDI R1,10 (Set the value of a register to an integer.)
# 00000001 (index 1, spot 2)
# 00001010 (10)
# 10000010 # LDI R2,TEST3 (Set the value of a register to an integer.)
# 00000010 (index 2, spot 3)
# 00110000 (48)
# 10100111 # CMP R0,R1 (Compare the values in two registers.)
# 00000000 (index 0, spot 1)
# 00000001 (1)
# 01010101 # JEQ R2 (If `equal` flag is set (true), jump to the address stored in the given register.)
# 00000010 (index 2, spot 3)
# 10000010 # LDI R3,3 (Set the value of a register to an integer.)
# 00000011 (index 3, spot 4)
# 00000011 (3)
# 01000111 # PRN R3 (Print numeric value stored in the given register.)
# 00000011 (index 3, spot 4)
# # TEST3 (address 48):
# 10000010 # LDI R2,TEST4 (Set the value of a register to an integer.)
# 00000010 (index 2, spot 3)
# 00111101 (61)
# 10100111 # CMP R0,R1 (Compare the values in two registers.)
# 00000000 (index 0, spot 1)
# 00000001 (1)
# 01010110 # JNE R2 (If `E` flag is clear (false, 0), jump to the address stored in the given register)
# 00000010 (index 2, spot 3)
# 10000010 # LDI R3,4 (Set the value of a register to an integer.)
# 00000011 (index 3, spot 4)
# 00000100 (4)
# 01000111 # PRN R3 (Print numeric value stored in the given register.)
# 00000011 (index 3, spot 4)
# # TEST4 (address 61):
# 10000010 # LDI R3,5 (Set the value of a register to an integer.)
# 00000011 (index 3, spot 4)
# 00000101 (5)
# 01000111 # PRN R3 (Print numeric value stored in the given register.)
# 00000011 (index 3, spot 4)
# 10000010 # LDI R2,TEST5 (Set the value of a register to an integer.)
# 00000010 (index 2, spot 3)
# 01001001 (73)
# 01010100 # JMP R2 (Jump to the address stored in the given register.)
# 00000010 (index 2, spot 3)
# 01000111 # PRN R3 (Print numeric value stored in the given register.)
# 00000011 (index 3, spot 4)
# # TEST5 (address 73):
# 00000001 # HLT (Halt the CPU (and exit the emulator).)
