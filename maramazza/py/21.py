from collections import Counter


def getpuzzleInput():
    foods = list()
    with open("./../data/21.txt") as input_txt:
        for line in input_txt:
            line = line.strip()
            parts = line.split(" (contains ")
            ingredients = parts[0].strip().split(" ")
            allergens = parts[1].strip().replace(")", "").split(", ")
            foods.append([ingredients, allergens])

    return foods


def solvePart1(foods):
    ingr_with_allergen = {}
    ingr_counter = Counter()
    for food in foods:
        for ingredient in food[0]:
            ingr_counter[ingredient] += 1
        ingredients = set(food[0])
        for allergen in food[1]:
            if allergen in ingr_with_allergen:
                ingr_with_allergen[allergen].intersection_update(ingredients)
            else:
                ingr_with_allergen[allergen] = ingredients.copy()

    bad_ingredients = set()
    for ingredients in ingr_with_allergen.values():
        bad_ingredients = bad_ingredients.union(ingredients)

    ans = 0
    for ingredient, count in ingr_counter.items():
        if ingredient not in bad_ingredients:
            ans += count
    return ans


def solvePart2(foods):
    ingr_with_allergen = {}
    for food in foods:
        ingredients = set(food[0])
        for allergen in food[1]:
            if allergen in ingr_with_allergen:
                ingr_with_allergen[allergen].intersection_update(ingredients)
            else:
                ingr_with_allergen[allergen] = ingredients.copy()

    final_allergens = {}
    changed = True
    while changed:
        changed = False
        new_allergen_ingredients = {}
        for allergen, ingredients in ingr_with_allergen.items():
            for ingredient in final_allergens.values():
                if ingredient in ingredients:
                    ingredients.remove(ingredient)
            if len(ingredients) == 1:
                final_allergens[allergen] = ingredients.pop()
                changed = True
            else:
                new_allergen_ingredients[allergen] = ingredients
        ingr_with_allergen = new_allergen_ingredients

    ans = []
    for allergen in sorted(final_allergens.keys()):
        ans.append(final_allergens[allergen])
    return ','.join(ans)


if __name__ == "__main__":
    foods = getpuzzleInput()

    answer1 = solvePart1(foods)
    print(f"Res Part 1: {answer1}")

    answer2 = solvePart2(foods)
    print(f"Res Part 2: {answer2}")
