fields = [
    "byr",
    "iyr",
    "eyr",
    "hgt",
    "hcl",
    "ecl",
    "pid",
    # "cid",
]

def parse_passport(passport_string):
    return dict(
        field.split(":") for field in passport_string
            .replace("\n", " ")
            .strip()
            .split(" ")
    )

with open("inputs/day4.txt") as f:
    valid_count = 0
    for passport in f.read().split("\n\n"):
        passport = parse_passport(passport)
        if all(field in passport for field in fields):
            valid_count += 1
    print(valid_count)