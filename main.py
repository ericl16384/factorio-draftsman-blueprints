
import json
import numpy as np
import matplotlib.pyplot as plt

from draftsman.data import recipes as draftsman_recipes
# from draftsman import prototypes as draftsman_prototypes
import draftsman

import utils
import recipes as ru




vbs = utils.VisualBeltSystem("reference_blueprint_book.txt")


targets = {
    # "automation-science-pack": 1,
    # "logistic-science-pack": 1,
    # "chemical-science-pack": 1,
    # "military-science-pack": 1,

    # "electronic-circuit": 7.5,
    # "iron-gear-wheel": 15,
    
    # "iron-gear-wheel": 15,
    # "copper-cable": 7.5,

    "advanced-circuit": 0.01,
}
vbs.update_rate_targets(targets)

allowed_machines = [
    "assembling-machine-1",
    # "electric-furnace",
]
vbs.update_allowed_machines(allowed_machines)


# machine_recipes = ru.develop_machine_recipes(allowed_machines)

ordered_recipes, required_inputs = ru.develop_recipe_path(targets, vbs.machine_recipes)

recipe_throughputs = ru.develop_recipe_throughputs(targets, ordered_recipes, required_inputs, vbs.machine_recipes)

# print(json.dumps(list(ru.RecipeAnalysis("logistic-science-pack", vbs.machine_recipes).context.keys()), indent=2))
# print(json.dumps(recipe_throughputs, indent=2))

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

    machine = vbs.machine_recipes[recipe][0]

    # time = ru.get_recipe_time(recipe)

    # assert len(allowed_machines) == 1
    # speed = draftsman.entity.new_entity(machine).prototype["crafting_speed"]
    # print(speed)
    
    # output_amount = draftsman_recipes.raw[recipe]["results"][0]["amount"]

    # multiplicity = int(np.ceil(throughput * time / speed / output_amount))
    # multiplicity = 1 # debug
    recipes.append((machine, recipe, throughput))

    print(f"{machine:20}  {recipe:20}  {throughput:5.2f}")
print()




############################################
# vbs.apply_inputs(subdivided_ordered_inputs)

# for recipe in recipes:
#     vbs.apply_recipe(*recipe)
############################################


utils.test_input_connector_creation(vbs, 6)


# for target in reversed(targets):
#     vbs.grab_belt_lane(target)
# for i in range(len(targets)):
#     vbs.backtrack_build_belt_lane(vbs.grid_current_row, vbs.grid_current_col-1-i)





# s = vbs.export_bp().to_string()

vbs.add_debug_history()

print(f"exporting debug history ({len(vbs.debug_working_bp_history.blueprints)})")
vbs.debug_working_bp_history.active_index = len(vbs.debug_working_bp_history.blueprints)-1
s = vbs.debug_working_bp_history.to_string()



# print(s)
with open("output.txt", "w") as f:
    print(s, file=f)
print()
print("exported to output.txt")


if __name__ == "__main__":
    # vbs.show_image()
    print()
    print("waiting for ENTER...")
    print()
    input()



