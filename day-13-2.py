import itertools

# Iteratively merge rules
with open("inputs/day13.txt") as f:
    rules = [ (i, int(bus_id)) for (i, bus_id) in enumerate(f.readlines()[1].split(",")) if bus_id != "x" ]

    i = 0
    while len(rules) > 1:
        for ((offset1, mod1), (offset2, mod2)) in itertools.product(rules, rules):
            if offset1 < offset2:
                if (mod2 * i + (offset2 - offset1)) % mod1 == 0:
                    rules.remove((offset1, mod1))
                    rules.remove((offset2, mod2))
                    rules.append((offset2 + i * mod2, mod1 * mod2))
                    i = 0 # Start loop again after new rule add
                    break
        i += 1
    
    (offset, mod) = rules[0]
    print(f"Solution: {mod - offset}")
        