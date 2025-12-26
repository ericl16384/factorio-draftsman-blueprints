
import numpy as np
import matplotlib.pyplot as plt

import utils





# belt_lane_inputs = [
#     "iron-plate",
#     "copper-plate",
#     "steel-plate",
# ]

recipes = [
    ("iron-plate", ()),
    ("copper-plate", ()),

    ("iron-gear-wheel", ("iron-plate",)),
    ("copper-cable", ("copper-plate",)),
    ("electronic-circuit", ("iron-plate", "copper-cable",)),

    ("transport-belt", ("iron-plate", "iron-gear-wheel",)),
    ("inserter", ("iron-plate", "iron-gear-wheel", "electronic-circuit",)),

    ("automation-science-pack", ("iron-gear-wheel", "copper-plate",)),
    ("logistic-science-pack", ("transport-belt", "inserter",)),


    # # ("iron-plate", ()),
    # # ("iron-gear-wheel", ()),
    # # ("electronic-circuit", ()),

    # # ("inserter", ("iron-plate", "iron-gear-wheel", "electronic-circuit",)),

]

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



