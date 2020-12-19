def get_solution():
    with open("inputs/day1.txt") as f:
        numbers = set( map(int, f.readlines() ) )
        for x in numbers:
            for y in numbers:
                remainder = 2020 - ( x + y )
                if remainder in numbers:
                    return x * y * remainder

if __name__ == "__main__":
    print(get_solution())
    