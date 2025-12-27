
import numpy as np
import matplotlib.pyplot as plt

from draftsman.data import recipes as draftsman_recipes
# from draftsman import prototypes as draftsman_prototypes
import draftsman

import utils
import recipes as ru




# belt_lane_inputs = [
#     "iron-plate",
#     "copper-plate",
#     "steel-plate",
# ]

# recipes = [
#     ("iron-plate", ()),
#     ("copper-plate", ()),

#     ("iron-gear-wheel", ("iron-plate",)),
#     ("copper-cable", ("copper-plate",)),
#     ("electronic-circuit", ("iron-plate", "copper-cable",)),

#     ("transport-belt", ("iron-plate", "iron-gear-wheel",)),
#     ("inserter", ("iron-plate", "iron-gear-wheel", "electronic-circuit",)),

#     ("automation-science-pack", ("iron-gear-wheel", "copper-plate",)),
#     ("logistic-science-pack", ("transport-belt", "inserter",)),


#     # # ("iron-plate", ()),
#     # # ("iron-gear-wheel", ()),
#     # # ("electronic-circuit", ()),

#     # # ("inserter", ("iron-plate", "iron-gear-wheel", "electronic-circuit",)),

# ]

targets = {
    # "automation-science-pack": 7.5,
    # "logistic-science-pack": 7.5,
    # # "chemical-science-pack": 7.5,
    # # "military-science-pack": 7.5,
    "electronic-circuit": 10,
}

allowed_machines = [
    "assembling-machine-1"
]

ordered_recipes, required_inputs = ru.develop_recipe_path(
    targets, allowed_machines)

recipe_throughputs = ru.develop_recipe_throughputs(
    targets, ordered_recipes, required_inputs
)

print(ordered_recipes)

recipes = []
for recipe in required_inputs:
    # recipes.append([
    #     recipe,
    #     []
    # ])
    recipes.append((recipe, 0))
for i in range(len(ordered_recipes)-1, -1, -1):
    recipe = ordered_recipes[i]
    # recipes.append([
    #     recipe,
    #     [i["name"] for i in draftsman_recipes.raw[recipe]["ingredients"]]
    # ])
    throughput = recipe_throughputs[recipe]

    time = utils.get_recipe_time(recipe)

    assert len(allowed_machines) == 1
    speed = draftsman.entity.new_entity(allowed_machines[0]).prototype["crafting_speed"]
    # print(speed)
    
    output_amount = draftsman_recipes.raw[recipe]["results"][0]["amount"]

    multiplicity = int(np.ceil(throughput * time / speed / output_amount))
    # multiplicity = 1 # debug
    recipes.append((recipe, multiplicity))

    print(recipe, throughput, multiplicity)





vbs = utils.VisualBeltSystem("reference_blueprint_book.txt")
# for item in belt_lane_inputs:
#     vbs.add_belt_lane(item)

grid_colors = np.zeros((100, 100, 3))
grid_current_pos = np.array((1, 1))




# belt_lanes = grab_belt_lane(belt_lanes, "copper-plate")
# print(belt_lanes)
# belt_lanes = grab_belt_lane(belt_lanes, "steel-plate")
# print(belt_lanes)
# belt_lanes = grab_belt_lane(belt_lanes, "steel-plate")
# print(belt_lanes)

# print(vbs.belt_lanes)

# for output, ingredients in recipes:
#     for ingredient in ingredients:
#         # print("grab", ingredient)
#         vbs.grab_belt_lane(ingredient)
#         # print(belt_lanes)
#     vbs.add_belt_lane(output)
#     # print(vbs.belt_lanes)

for recipe in recipes:
    vbs.apply_recipe(recipe)

# print()
# for pair in enumerate(vbs.ordered_belt_id_list):
#     print(pair)
# print(vbs.ordered_belt_id_list)




s = vbs.export_bp().to_string()
# print(s)
with open("output.txt", "w") as f:
    print(s, file=f)
print("exported to output.txt")

vbs.show_image()



