from functools import lru_cache

with open("inputs/day10.txt") as f:
    adaptors = list(map(int, f.readlines()))
    adaptors = [ 0, *sorted(adaptors), max(adaptors) + 3]

    @lru_cache(maxsize=None)
    def get_sequences_ending_with(x):        
        if x == 0:
            return 1
        return sum(
            get_sequences_ending_with(x - dx) for dx in [1,2,3] 
                if x-dx in adaptors
        )

    print(get_sequences_ending_with( max(adaptors) ))