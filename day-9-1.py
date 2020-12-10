def composed_of(digit, digits):
    return any( digit - x in digits for x in digits)

preamble = 25

with open("inputs/day9.txt") as f:
    digits = list(map(int, f.readlines()))
    for i, digit in enumerate(digits):
        if i > preamble and not composed_of(digit, digits[i-preamble:i]):
            print(digit)