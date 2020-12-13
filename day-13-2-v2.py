with open("inputs/day13.txt") as f:
    rules = [ (i, int(bus_id)) for (i, bus_id) in enumerate(f.readlines()[1].split(",")) if bus_id != "x" ]
    t, jump_size = rules[0]
    for (offset, mod) in rules[1:]:
        while (t + offset) % mod != 0:
            t += jump_size
        jump_size *= mod
    print(t)