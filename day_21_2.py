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
    
    canonical_mapping = {}


    while len(canonical_mapping) < len(allergens):

        for (allergen, possible_allergen_causes) in possible_allergen_causes_map.items():
            if len(possible_allergen_causes) == 1:
                allergenic_ingredient = list(possible_allergen_causes)[0]
                canonical_mapping[allergen] = allergenic_ingredient

                del possible_allergen_causes_map[allergen]
                for ingredients in possible_allergen_causes_map.values():
                    if allergenic_ingredient in ingredients:
                        ingredients.remove(allergenic_ingredient)
                break

    sorted_by_allergen = sorted(canonical_mapping.items(), key=lambda x: x[0])
    
    result = ",".join([ ingredient for (allergen, ingredient) in sorted_by_allergen ])
    print(result)
