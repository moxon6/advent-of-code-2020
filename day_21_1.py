import re

def parse_line(line):
    ingredients, allergens = line.split(" (contains")
    ingredients = [x.strip() for x in ingredients.split(" ")]
    allergens = [x.strip() for x in allergens.strip(")").split(",")]
    return set(ingredients), set(allergens)

with open("inputs/day21.txt") as f:
    foods = [parse_line(line) for line in f.read().splitlines()]

    ingredients = set.union(*[i for (i,a) in foods])
    allergens = set.union(*[a for (i,a) in foods])
    
    # Map allergen -> ingredient[]
    possible_allergen_causes_map = {}

    for allergen in allergens:
        possible_causes = [ food_ingredients for (food_ingredients, food_allergens) in foods if allergen in food_allergens ]
        possible_causes = set.intersection(*possible_causes)

        possible_allergen_causes_map[allergen] = possible_causes

    possible_allergen_causes = set.union(*possible_allergen_causes_map.values())

    safe_ingredients = ingredients.difference(possible_allergen_causes)
    
    total_instances = sum(
        sum( ingredient in food[0] for food in foods )
        for ingredient in safe_ingredients
    )

    print(total_instances)
