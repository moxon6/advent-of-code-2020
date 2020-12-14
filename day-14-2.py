import re
from utils import powerset

matcher = re.compile("mem\[(?P<address>\d+)\] = (?P<value>.*)")
memory = {}

def generate_addresses(mask):
    for mask_subset in powerset([i for i, x in enumerate(reversed(mask)) if x == "X"]):
        yield sum( 2**i for i in mask_subset)

with open("inputs/day14.txt") as f:
    mask_out_xs = None
    mask_over_1s = None
    apply_bitmask = lambda address: (address & mask_out_xs) | mask_over_1s

    for instruction in f.readlines():
        if instruction.startswith("mask"):
            mask = instruction.split(" = ")[1]

            mask_out_xs = int( mask.replace("0", "1").replace("X", "0"), 2) # remove all X's
            mask_over_1s = int( mask.replace("X", "0"), 2) # apply 1's on top
        else:

            instruction = matcher.match(instruction.strip()).groupdict()
            address = int( instruction["address"] )
            value = int( instruction["value"] )
            
            for offset in generate_addresses(mask.strip()):
                memory[apply_bitmask(address) + offset ] = value
    print(sum(memory.values()))