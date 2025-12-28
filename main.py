
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

    # "electronic-circuit": 4,
    # "iron-gear-wheel": 10
    
    "iron-gear-wheel": 15,
    # "copper-cable": 7.5,
}

allowed_machines = [
    "assembling-machine-1"
]

ordered_recipes, required_inputs = ru.develop_recipe_path(
    targets, allowed_machines)

recipe_throughputs = ru.develop_recipe_throughputs(
    targets, ordered_recipes, required_inputs
)

subdivided_ordered_recipes = ru.subdivide_ordered_recipes(ordered_recipes, recipe_throughputs)

subdivided_ordered_inputs = ru.subdivide_ordered_lanes(required_inputs, recipe_throughputs)


# print(ordered_recipes)

recipes = []
# for recipe in required_inputs:
#     # recipes.append([
#     #     recipe,
#     #     []
#     # ])
#     recipes.append((recipe, 0))
for i in range(len(subdivided_ordered_recipes)-1, -1, -1):
    recipe, throughput = subdivided_ordered_recipes[i]

    time = ru.get_recipe_time(recipe)

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






# vbs.apply_inputs([x[0] for x in subdivided_ordered_inputs])

# for recipe in recipes:
#     vbs.apply_recipe(recipe)

# # for target in targets:
# #     vbs.grab_belt_lane(target)
# vbs.grab_belt_lane("iron-gear-wheel")
# vbs.grab_belt_lane("iron-gear-wheel")





vbs.apply_inputs(["iron-plate", "iron-plate", "copper-plate", "copper-plate",])

vbs.grab_belt_lane("iron-plate")
# vbs.grab_belt_lane("iron-plate")





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



