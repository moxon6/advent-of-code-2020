import re
from operator import xor
pattern = re.compile('(\d*)-(\d*) (.): (.*)')

def get_solution():
    with open("inputs/day2.txt") as f:
        return sum( 1 for x in f.readlines() if valid_password(x) )

def valid_password(line):
    low, high, char, password = pattern.match(line).groups()
    return xor( 
        password[int(low) - 1] == char,
        password[int(high) - 1] == char
    )

if __name__ == "__main__":
    print(get_solution())