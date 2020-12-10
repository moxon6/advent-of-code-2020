with open("inputs/day10.txt") as f:
    adaptors = list(map(int, f.readlines()))
    adaptors = [ 0, *sorted(adaptors), max(adaptors) + 3]
    
    adaptors_set = set(adaptors)

    sequences_ending_with = {
        0: 1
    }
    
    for adaptor in adaptors:
        for dx in [1,2,3]:
            if (adaptor - dx) in sequences_ending_with:
                sequences_ending_with.setdefault(adaptor, 0)
                sequences_ending_with[adaptor] += sequences_ending_with[adaptor - dx]
    print(sequences_ending_with)