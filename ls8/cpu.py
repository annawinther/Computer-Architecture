"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # reg is 8 
        self.reg = [0] * 8
        # ram is 256
        self.ram = [0] * 256
        # add pc to 0
        self.pc = 0

        self.branchtable = {}
        self.branch_operations()

    ### Branch Operations ###
    def LDI(self, reg_a, data):
        self.reg[reg_a] = data
        self.pc += 3

    def PRN(self, a, b):
        print(self.reg[a])
        self.pc += 2
    ### AUL Operations ###
    # MUL is the resposibility of the ALU 
    # Here it calls the alu() function passing in operant_a and operand_b to get the work done
    def MUL(self, a, b):
        self.alu("MUL", a, b)
        self.pc += 3

    def load(self, program):
        """Load a program into memory."""

        address = 0
        for instruction in program:
            self.ram[address] = instruction
            address += 1

    def branch_operations(self):
        self.branchtable[0b10000010] = self.LDI
        self.branchtable[0b01000111] = self.PRN
        self.branchtable[0b10100010] = self.MUL

    def ram_read(self, adress):
        return self.ram[adress]

    def ram_write(self, value, address):
        self.ram[address] = value

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]

        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")
        # add MUL operation
        # Multiply the values in two registers together and store the result in registerA.
       

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
        # set running to be True
        running = True
        while running:
        # needs to read mem address stores in register PC and store in IR - local variable
            IR = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            # if IR = `HLT` (1)
            if IR == 0b00000001:
                # Halt the CPU (and exit the emulator).
                print("Halting operations")
                running = False
                break
            elif IR not in self.branchtable:
                print("Invalid Instruction")
                running = False
            # else if IR = 'PRN' (71)
            # elif IR == 0b01000111:
            #     # call self.prn on operand_a (the next item)
            #     self.prn(operand_a)
            #     # increment self.pc by 2
            #     self.pc += 2
            # # else if IR = 'LDI' (130)
            # elif IR == 0b10000010:
            #     # call self.ldi on both operand_a and operand_b
            #     self.ldi(operand_a, operand_b)
            #     # increment self.pc by 3
            #     self.pc += 3
            # else if IR == 'MUL' (162)
            # elif IR == 0b10100010:
            #     # MUL is the resposibility of the ALU 
            #     # Here it calls the alu() function passing in operant_a and operand_b to get the work done
                # self.alu("MUL", operand_a, operand_b)
                # self.pc += 3
            # otherwise
            else:
                # print an Invalid Instruction message amd set running to False to exit
                self.branchtable[IR](operand_a, operand_b)
