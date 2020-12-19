with open("inputs/day10.txt") as f:
    adaptors = list(map(int, f.readlines()))
    adaptors = [ 0, *sorted(adaptors), max(adaptors) + 3]
    
    differences = {
        1: 0,
        2: 0,
        3: 0
    }

    for (i, adaptor) in enumerate(adaptors):
        if i == 0:
            continue

        dj = adaptor - adaptors[i-1]
        differences[dj] += 1

    print(differences[1] * differences[3])

