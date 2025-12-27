
import numpy as np
import matplotlib.pyplot as plt

from draftsman.data import recipes as draftsman_recipes

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

ordered_recipes, required_inputs = ru.develop_recipe_path({
    # "automation-science-pack": 7.5,
    # "logistic-science-pack": 7.5,
    # # "chemical-science-pack": 7.5,
    # # "military-science-pack": 7.5,
    "electronic-circuit": 7.5,
}, [
    "assembling-machine-1"
])

print(ordered_recipes)

recipes = []
for recipe in required_inputs:
    recipes.append([
        recipe,
        []
    ])
for i in range(len(ordered_recipes)-1, -1, -1):
    recipe = ordered_recipes[i]
    recipes.append([
        recipe,
        [i["name"] for i in draftsman_recipes.raw[recipe]["ingredients"]]
    ])





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



