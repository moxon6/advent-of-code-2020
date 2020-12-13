import math
import itertools

with open("inputs/day13.txt") as f:
    f.readline()
    buses = dict( (i, int(bus_id)) for (i, bus_id) in enumerate(f.readline().split(",")) if bus_id != "x" )
    buses_origin = { k:v for (k,v) in buses.items() }

    i = 0
    while True:
        for ((offset1, mod1), (offset2, mod2)) in itertools.product(buses.items(), buses.items()):
            if offset1 < offset2:
                if (mod2 * i + (offset2 - offset1)) % mod1 == 0:
                    del buses[offset1]
                    del buses[offset2]
                    if (offset2 + i * mod2) in buses:
                        raise Exception("Overwriting")
                    buses[offset2 + i * mod2] = mod1 * mod2
                    print(f"Combining rules {(offset1, mod1)} and {(offset2, mod2)} with i={i}")
                    print(f"t + {offset2 + i * mod2} mod {mod1 * mod2} == 0")
                    break
        i += 1
        if len(buses) == 1:
            break
    
    (offset, mod) = list(buses.items())[0]

    print(buses_origin)
    for j in itertools.count(start=1):
        solution = mod * j - offset
        for (offset, mod) in buses_origin.items():
            if not (solution + offset) % mod == 0:
                print(f"Solution {solution} rejected, rule {(offset, mod)} failed")
                raise SystemExit
            
        else:
            print(f"Solution {solution} accepted")
            raise SystemExit
        print(solution, solution > 100000000000000)
        