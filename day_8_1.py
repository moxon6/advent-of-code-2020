class Computer:
    def __init__(self):
        self.accumulator = 0
        self.instruction_pointer = 0
        
        self.completed = False
        self.executed_instructions = set()

    def execute_program(self, program):
        while True:
            if self.instruction_pointer not in self.executed_instructions:
                self.executed_instructions.add(self.instruction_pointer)
                
                instruction = program[self.instruction_pointer]
                self.execute_instruction(*instruction)
            else:
                print("Avoided second execution of instruction")
                self.print_summary()
                break

    def execute_instruction(self, op, arg):
        if op == "nop":
            self.instruction_pointer += 1
        if op == "acc":
            self.accumulator += arg
            self.instruction_pointer += 1
        if op == "jmp":
            self.instruction_pointer += arg
    
    def print_summary(self):
        print("Accumulator: ", self.accumulator, " Instruction pointer ", self.instruction_pointer)

def parse_instruction(instruction):
    op, arg = instruction.split(" ")
    return op, int(arg)

computer = Computer()
with open("inputs/day8.txt") as f:
    program = list(map(parse_instruction, f.readlines()))
    computer.execute_program(program)
