


class Cardiac(object):

    # utility stuff
    def reset(self):
        """Setup/reset the CPU"""

        self.pc = 0 # program counter

        self.acc = 0 # accumulator



        # build opcode list for easier execution later
        self.opcodes = [self.opcode_0,
                        self.opcode_1,
                        self.opcode_2,
                        self.opcode_3,
                        self.opcode_4,
                        self.opcode_5,
                        self.opcode_6,
                        self.opcode_7,
                        self.opcode_8,
                        self.opcode_9]


    def load_memory(self, memory):
        #TODO: This needs to be heavily expanded
        self.mem = memory


    def debug_dump(self):

        pc_mem = self.mem[self.pc]
        instruction = pc_mem/100
        data = pc_mem%100

        print "----- debug dump ----"
        print "acc: ", self.acc
        print "pc: ", self.pc
        print "memory at pc: ", pc_mem
        print "instruction: ", instruction
        print "data: ", data
        print

    def run(self):
        pc_mem = self.mem[self.pc]
        instruction = pc_mem/100
        data = pc_mem%100

        # self.debug_dump()

        self.pc += 1
        self.opcodes[instruction](data)


    def execute(self):
        self.running = True

        while self.running:
            self.run()

        print "[[[ Finished at PC = {} ]]]".format(self.pc)

    # opcodes

    # NOP 
    def opcode_0(self, data):
        pass

    # CLA
    def opcode_1(self, data):
        """Clear accululator and set from memory"""
        self.acc = self.mem[data]

    # ADD
    def opcode_2(self, data):
        """Add from memory to accumulator"""
        self.acc += self.mem[data]

    # TAC
    def opcode_3(self, data):
        """Jump if accumulator is < 0"""
        if self.acc < 0:
            self.pc = data

    # SFT
    def opcode_4(self, data):
        pass

    # OUT
    def opcode_5(self, data):
        print self.mem[data]

    # STO
    def opcode_6(self, data):
        pass

    # SUB
    def opcode_7(self, data):
        pass

    # JMP
    def opcode_8(self, data):
        pass

    # HLT
    def opcode_9(self, data):
        self.running = False

cardiac = Cardiac()
cardiac.reset()
cardiac.load_memory([120, 221, 520, 300, 0, 0, 0, 0, 0, 0,
                     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
                     15, 5, -1, 0, 0, 0, 0, 0, 0, 0, 
                     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
                     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
                     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
                     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
                     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
                     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
                     0, 0, 0, 0, 0, 0, 0, 0, 0, 900 ])

cardiac.execute()
