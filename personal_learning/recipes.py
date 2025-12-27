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

# targets = [
#     # "electronic-circuit",

#     "automation-science-pack",
#     "logistic-science-pack",
#     # "chemical-science-pack",
#     # "military-science-pack",
#     # "production-science-pack",
#     # "utility-science-pack",
#     # "space-science-pack",
# ]

desired_open_quantity_targets = {
    "automation-science-pack": 7.5,
    "logistic-science-pack": 7.5,
    # "chemical-science-pack": 7.5,
    # "military-science-pack": 7.5,
    # "production-science-pack": 7.5,
    # "utility-science-pack": 7.5,
    # "space-science-pack": 7.5,
}




allowed_recipes = set()

open_set = set()
closed_set = set()

# ordered_recipes

for machine in allowed_machines:
    allowed_recipes.update(recipes.for_machine[machine])

open_set.update(desired_open_quantity_targets.keys())


while open_set:

    current_recipe = open_set.pop()
    closed_set.add(current_recipe)

    print(current_recipe)

    if current_recipe not in recipes.raw:
        print(" ", "-- no recipe --")
        print()
        continue

    if current_recipe not in allowed_recipes:
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

    assert len(recipes.raw[current_recipe]["results"]) == 1
    assert recipes.raw[current_recipe]["results"][0]["name"] == current_recipe

    for ingredient in recipes.raw[current_recipe]["ingredients"]:
        name = ingredient["name"]

        # if name not in closed_set:
        open_set.add(name)

        print(" ", name)
    
    print()







    # if current_recipe not in open_quantity_targets:
    #     open_quantity_targets[current_recipe] = 0
    # open_quantity_targets[current_recipe] += 100 # TODO



# open_quantity_targets = dict()
# closed_quantity_targets = dict()
# open_quantity_targets.update(desired_open_quantity_targets)







print("open_set =", json.dumps(list(open_set), indent=2))
print("closed_set =", json.dumps(list(closed_set), indent=2))
# print("open_quantity_targets =", json.dumps(dict(open_quantity_targets), indent=2))
print()

    
