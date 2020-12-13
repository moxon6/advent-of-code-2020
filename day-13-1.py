import math

with open("inputs/day13.txt") as f:
    timestamp = int( f.readline() )
    buses = [int(bus_id) for bus_id in f.readline().split(",") if bus_id != "x"]
    nextbus = lambda bus_id: bus_id * math.ceil(timestamp / bus_id)
    earliest_bus = min(buses, key=nextbus)
    waiting_time = nextbus(earliest_bus) - timestamp
    print( waiting_time * earliest_bus )
