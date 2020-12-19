import itertools
from collections import defaultdict


with open("inputs/day15.txt") as f:
    
    initial = [int(x) for x in f.readline().split(",")]
    max_value = 2020

    index_table = defaultdict(list)
    for i,x in enumerate(initial):
        index_table[x].append(i)
    
    last_spoken = initial[-1]

    for i in range(len(initial), max_value):
        if (i % 100000 == 0):
            print(i)
        if len(index_table[last_spoken]) == 1:
            last_spoken = 0
        else:
            last_spoken = index_table[last_spoken][-1] - index_table[last_spoken][-2]
        index_table[last_spoken].append(i)
    
    print(last_spoken)