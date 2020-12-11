with open("inputs/day10.txt") as f:
    adaptors = list(map(int, f.readlines()))
    adaptors = [ 0, *sorted(adaptors), max(adaptors) + 3]
    
    adaptors_set = set(adaptors)

    memo_table = {
        0: 1
    }

    def get_sequences_ending_with(x):
        if x in memo_table:
            return memo_table[x]

        sequences = 0

        for dx in [1,2,3]:
            if x - dx in adaptors_set:
                sequences += get_sequences_ending_with(x - dx)
        memo_table[x] = sequences
        return sequences

    print(get_sequences_ending_with( max(adaptors) ))