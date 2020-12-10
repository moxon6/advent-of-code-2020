import re

matcher = re.compile("(?P<quantity>\d+) (?P<color>.*) bags?")

contents = {
}

def process_line(line):
    bag, bag_contents = line.split(" bags contain ")
    parsed_contents = [process_bag_item(x.strip()) for x in bag_contents.replace(".", "").split(",")]
    if None not in parsed_contents:
        contents[bag] = parsed_contents
    else:
        contents[bag] = []

def process_bag_item(bag_item):
    if bag_item == "no other bags":
        return None
    else:
        try:
            return matcher.match(bag_item).groupdict()
        except:
            print(bag_item)
            raise
    
def can_contain_gold(color):
    if color == "shiny gold":
        return True
    else:
        return any(map(
            lambda x: can_contain_gold(x["color"]), 
            contents[color]
        ))

with open("inputs/day7.txt") as f:
    for line in f.readlines():
        process_line(line)

    total = sum( 1 for color in contents if can_contain_gold(color) and color != "shiny gold" )
    print(total)