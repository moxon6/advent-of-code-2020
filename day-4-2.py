import re

colors = [
    "amb",
    "blu",
    "brn",
    "gry",
    "grn",
    "hzl",
    "oth",
]

fields = {
    "byr": lambda x: 1920 <= int(x) <= 2002,
    "iyr": lambda x: 2010 <= int(x) <= 2020,
    "eyr": lambda x: 2020 <= int(x) <= 2030,
    "hgt": lambda x: 150 <= int(x[:-2]) <= 193 if (x[-2:] == "cm") else 59 <= int(x[:-2]) <= 76,
    "hcl": lambda x: bool( re.match("^#[A-Za-z0-9]{6}$", x) ),
    "ecl": lambda x: x in colors,
    "pid": lambda x: bool( re.match("^[0-9]{9}$", x) ),
    # "cid": lambda x: True,
}

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
        if all(field in passport and validate(passport[field]) for (field, validate) in fields.items()):
            valid_count += 1
    print(valid_count)