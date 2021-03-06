import itertools
from collections import defaultdict

def main():
    with open("inputs/day15.txt") as f:
        
        initial = [int(x) for x in f.readline().split(",")]
        max_value = 30000000

        index_table = defaultdict(list)
        for i,x in enumerate(initial):
            index_table[x].append(i)
        
        last_spoken = initial[-1]

        for i in range(len(initial), max_value):
            if i % 1000000 == 0:
                print(i)

            if len(index_table[last_spoken]) == 1:
                last_spoken = 0
            else:
                last_spoken = index_table[last_spoken][-1] - index_table[last_spoken][-2]
            index_table[last_spoken] = [ *index_table[last_spoken], i ][-2:]
        
        print(last_spoken)

if __name__ == "__main__":
    main()