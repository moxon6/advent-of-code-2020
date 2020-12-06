

examples = [
    "BFFFBBFRRR",
    "FFFBBBFRRR",
    "BBFFBBFRLL"
]

def get_seat_id(boarding_pass):
    return int("".join(
        map(lambda x: "1" if (x == "B" or x == "R") else "0", boarding_pass) 
    ), 2)

## day-5-1
with open("inputs/day5.txt") as f:
    highest_boarding_pass = max(f.read().splitlines(), key=get_seat_id)    
    print(list(highest_boarding_pass), get_seat_id(highest_boarding_pass))

## day-5-2

with open("inputs/day5.txt") as f:
    seat_id_set = set(map(get_seat_id, f.read().splitlines()))
    for seat_id in seat_id_set:
        if (seat_id + 1) not in seat_id_set and (seat_id +2) in seat_id_set:
            print(f"Mising seat:  {seat_id +1}")
            break
