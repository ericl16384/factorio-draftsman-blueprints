import json
from draftsman.data import recipes

# # print(json.dumps(recipes.raw["iron-plate"], indent=4))

# print(json.dumps(list(recipes.categories["crafting"]), indent=4))

# print(json.dumps(recipes.raw["electronic-circuit"], indent=4))








# print(json.dumps(recipes.for_machine["assembling-machine-1"], indent=2))

# import sys
# sys.exit()




allowed_machines = [
    "assembling-machine-1"
]

targets = [
    # "electronic-circuit",

    "automation-science-pack",
    "logistic-science-pack",
    # "chemical-science-pack",
    # "military-science-pack",
    # "production-science-pack",
    # "utility-science-pack",
    # "space-science-pack",
]

open_set = set(targets)
closed_set = set()

unresolved_set = set()


allowed_recipes = set()
for machine in allowed_machines:
    allowed_recipes.update(recipes.for_machine[machine])


while open_set:

    current_recipe = open_set.pop()

    print(current_recipe)

    if current_recipe not in recipes.raw:
        unresolved_set.add(current_recipe)
        print(" ", "-- no recipe --")
        print()
        continue

    if current_recipe not in allowed_recipes:
        unresolved_set.add(current_recipe)
        print(" ", "-- recipe not allowed --")
        print()
        continue

    # if not "category" in recipes.raw[current_recipe]:
    #     print(json.dumps(recipes.raw[current_recipe], indent=2))
    #     input()
        
    # category = recipes.raw[current_recipe]["category"]
    # print(" ", " ", "[", category, "]")

    # if category not in allowed_categories:
    #     unresolved_set.add(current_recipe)
    #     print(" ", f"-- category not allowed --")
    #     print()
    #     continue
    
    closed_set.add(current_recipe)

    assert len(recipes.raw[current_recipe]["results"]) == 1
    assert recipes.raw[current_recipe]["results"][0]["name"] == current_recipe

    for ingredient in recipes.raw[current_recipe]["ingredients"]:
        name = ingredient["name"]
        if name not in closed_set:
            open_set.add(name)

        print(" ", name)
    
    print()



print("open_set =", json.dumps(list(open_set), indent=2))
print("closed_set =", json.dumps(list(closed_set), indent=2))
print("unresolved_set =", json.dumps(list(unresolved_set), indent=2))
print()

    
