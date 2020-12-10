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

def get_total_bags(color):
    return sum( int(item["quantity"]) * ( 1 + get_total_bags(item["color"])) for item in contents[color] ) # + 1 for the parent bag

with open("inputs/day7.txt") as f:
    for line in f.readlines():
        process_line(line)

    
    print(get_total_bags("shiny gold"))