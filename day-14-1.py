import re

matcher = re.compile("mem\[(?P<address>\d+)\] = (?P<value>.*)")
memory = {}

with open("inputs/day14.txt") as f:
    mask_1s = None
    mask_0s = None
    
    apply_bitmask = lambda value: (mask_1s | value) & mask_0s

    for instruction in f.readlines():
        if instruction.startswith("mask"):
            mask = instruction.split(" = ")[1]
            mask_1s = int( mask.replace("X", "0") , 2) # set 1's mask
            mask_0s = int ( mask.replace("X", "1"), 2) # set 0's mask
        else:
            instruction = { k: int(v) for k,v in matcher.match(instruction.strip()).groupdict().items() }

            memory[instruction["address"]] = apply_bitmask(instruction["value"])
    print(sum(memory.values()))