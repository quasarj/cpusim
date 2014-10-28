#!/usr/bin/env python3

"""
    Second very simple CPU simulator.

    The Plan:
    Memory is addressable by 4 bytes.
    Memory arranged into sets of 6 bytes.
    First byte is instruction, second is register, final 4 are memory/parameter.

    Four registers: A, B, C, D (or more, up to 256 I think)
    Plus an instruction register


"""
from __future__ import print_function

from binascii import hexlify

DEBUG=False
# DEBUG=True

def to_int(bytes):
    return int.from_bytes(bytes, byteorder='big')

def to_bytes(num):
    return num.to_bytes(4, 'big')

class Second(object):

    # utility stuff
    def reset(self):
        """Setup/reset the CPU"""

        self.pc = 0 # program counter
        self.ir = 0 # instruction register


        self.registers = [bytearray()] * 4

        # build opcode list for easier execution later
        self.opcodes = [self.HLT,  # 0 halt
                        self.STC,  # 1 store constant
                        self.STM,  # 2 store memory
                        self.JMP,  # 3 jump (no condition)
                        self.JPT,  # 4 jump if reg != 0 (is True)
                        self.JPF,  # 5 jump if reg == 0 (is False)
                        self.ADC,  # 6 add constant to reg
                        self.ADM,  # 7 add memory to constant
                        self.SBC,  # 8 subtract constant from reg
                        self.SBM,  # 9 subtract memory from reg
                        self.PTR,  # a print register to console
                        self.PTM,  # b print memory to console
                        self.PTS,  # c print string to console
                        
                        ]

    def load_memory(self, file):
        self.mem = bytearray(file.read()) 

    def print_registers(self):
        print("Registers:")
        print("A:", hexlify(self.registers[0]))
        print("B:", hexlify(self.registers[1]))
        print("C:", hexlify(self.registers[2]))
        print("D:", hexlify(self.registers[3]))
        print("\n")


    def run(self):
        self.ir = self.mem[self.pc]

        reg_param = self.mem[self.pc+1]
        otr_param = self.mem[self.pc+2:self.pc+6]

        if DEBUG:
            print("pc", self.pc)
            print("ir", self.ir, self.opcodes[self.ir].__name__)
            print("reg param", reg_param)
            print("other param", otr_param)
            print("\n")
            self.print_registers()

        self.pc += 6
        self.opcodes[self.ir](reg_param, otr_param)


    def execute(self):
        self.running = True

        print("Starting execution. Memory size = {}\n".format(len(self.mem)))

        while self.running:
            try:
                self.run()
            except IndexError:
                print("Attempted to read memory outside of range! Halting.")
                self.running = False

        print("[[[ Finished at PC = {} ]]]".format(self.pc))
        self.print_registers()

    # opcodes

    # Halt
    def HLT(self, reg, other):
        self.running = False

    # Store constant
    def STC(self, reg, other):
        self.registers[reg] = other

    # Store Memory
    def STM(self, reg, other):
        loc = to_int(other)
        self.registers[reg] = self.mem[loc:loc+4]

    def JMP(self, reg, other):
        self.pc = to_int(other)

    def JPT(self, reg, other):
        if to_int(self.registers[reg]) != 0:
            self.pc = to_int(other)

    def JPF(self, reg, other):
        if to_int(self.registers[reg]) == 0:
            self.pc = to_int(other)

    def ADC(self, reg, other):
        self.registers[reg] = to_bytes(to_int(self.registers[reg]) + to_int(other))

    def ADM(self, reg, other):
        loc = to_int(other)
        self.registers[reg] = to_bytes(to_int(self.registers[reg]) + 
                                       to_int(self.mem[loc:loc+4]))

    def SBC(self, reg, other):
        self.registers[reg] = to_bytes(to_int(self.registers[reg]) - to_int(other))

    def SBM(self, reg, other):
        loc = to_int(other)
        self.registers[reg] = to_bytes(to_int(self.registers[reg]) - 
                                       to_int(self.mem[loc:loc+4]))

    def PTR(self, reg, other):
        print("PTR:", to_int(self.registers[reg]))

    def PTM(self, reg, other):
        loc = to_int(other)
        val = self.mem[loc:loc+4]
        print("PTM: {} ({}) Loc: {}".format(to_int(val), 
                                            hexlify(val), 
                                            hexlify(other)))

    def PTS(self, reg, other):
        pass




second = Second()
second.reset()
with open("test.bin", "rb") as f:
    second.load_memory(f)

second.execute()
