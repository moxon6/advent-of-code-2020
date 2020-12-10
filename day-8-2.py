class Computer:
    def __init__(self):
        self.accumulator = 0
        self.instruction_pointer = 0
        
        self.completed = False
        self.executed_instructions = set()

    def execute_program(self, program):
        while self.instruction_pointer != len(program):
            if self.instruction_pointer not in self.executed_instructions:
                self.executed_instructions.add(self.instruction_pointer)
                
                instruction = program[self.instruction_pointer]
                self.execute_instruction(*instruction)
            else:
                return False
        return True

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

def flip_instruction(program, index):
    new_program = program[:]
    op, arg = program[index]
    new_program[index] = ("nop", arg) if op == "jmp" else ("jmp", arg)
    return new_program
    
with open("inputs/day8.txt") as f:
    program = list(map(parse_instruction, f.readlines()))
    for index, (op, arg) in enumerate(program):
        if op in ["nop", "jmp"]:
            modified_program = flip_instruction(program, index)
            computer = Computer()
            if ( computer.execute_program(modified_program) ):
                print("Success")
                computer.print_summary()
