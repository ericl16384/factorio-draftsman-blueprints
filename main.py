
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
    "automation-science-pack": 1,
    "logistic-science-pack": 1,
    # "chemical-science-pack": 1,
    # "military-science-pack": 1,

    # "electronic-circuit": 2.5,
    # "iron-gear-wheel": 15,
    
    # "iron-gear-wheel": 15,
    # "copper-cable": 7.5,

    # "advanced-circuit": 7.5,

    # "inserter": 7.5
}
vbs.update_rate_targets(targets)

allowed_machines = [
    "assembling-machine-1",
    # "electric-furnace",
]
vbs.update_allowed_machines(allowed_machines)



###################################################################################################################
# machine_recipes = ru.develop_machine_recipes(allowed_machines)

ordered_recipes, required_inputs = ru.develop_recipe_path(targets, vbs.machine_recipes)

recipe_throughputs = ru.develop_recipe_throughputs(targets, ordered_recipes, required_inputs, vbs.machine_recipes)

# print(json.dumps(list(ru.RecipeAnalysis("logistic-science-pack", vbs.machine_recipes).context.keys()), indent=2))
# print(json.dumps(recipe_throughputs, indent=2))

subdivided_ordered_recipes = ru.subdivide_ordered_recipes(ordered_recipes, recipe_throughputs)

subdivided_ordered_inputs = ru.subdivide_ordered_lanes(required_inputs, recipe_throughputs)
###################################################################################################################
current_rates = {}
options = {}

for item in required_inputs:
    current_rates[item] = 0

for recipe, rate in recipe_throughputs.items():
    if recipe in required_inputs:
        continue

    current_rates[recipe] = 0

    options[recipe] = {
        "ingredient ratios": ru.get_recipe_ingredient_ratios(recipe),
        "steps": [],
    }

for recipe, rate in subdivided_ordered_recipes:
    options[recipe]["steps"].append(rate)
for item, rate in subdivided_ordered_inputs:
    current_rates[item] += rate

# for recipe in reversed(ordered_recipes):

#     # if not options[recipe]["steps"]:
#     #     continue
#     # next_options.add(recipe)
#     if recipe not in options:
#         continue

#     throughput = options[recipe]["steps"][-1]

#     options[recipe]["ingredient draw"] = {}
#     # options[recipe]["raw ratios"] = {}
#     # options[recipe]["total ratios"] = {}

#     # options[recipe]["prerequisites"] = set()
#     # options[recipe]["belt cost"] = 0
    
#     # ingredient draw
#     for item, ratio in options[recipe]["ingredient ratios"].items():
#         # if current_rates[item] < draw:
#         #     next_options.remove(recipe)
#         #     break
#         rate = throughput*ratio
#         options[recipe]["ingredient draw"][item] = rate

#         # if item not in options:
#         #     # if item not in options[recipe]["raw ratios"]:
#         #     #     options[recipe]["raw ratios"][item] = 0
#         #     # options[recipe]["raw ratios"][item] += ratio
#         #     continue

#         # for ing, ing_rate in options[item]["raw ratios"].items():
#         #     if ing not in options[recipe]["raw ratios"]:
#         #         options[recipe]["raw ratios"][ing] = 0
#         #     options[recipe]["raw ratios"][ing] += ing_rate*ratio

#         # options[recipe]["prerequisites"].add(item)
            
#         # print()
#         # print({recipe: throughput})
#         # # print(options[recipe]["prerequisites"])
#         # print(options[recipe]["ingredient draw"])
#         # # print(options[recipe]["raw ratios"])

#         # for prerequisite in options[recipe]["prerequisites"]:
#         #     if prerequisite in next_options:
#         #         next_options.remove(prerequisite)


# print(f"{ordered_recipes=}")
# print(f"{json.dumps(options,indent=2)}")
# print()

ordered_machine_steps = ru.create_ordered_machine_steps(ordered_recipes, options, targets, current_rates)
input()

assert len(ordered_machine_steps) == len(subdivided_ordered_recipes)
###################################################################################################################



recipes = []
# for recipe, throughput in reversed(subdivided_ordered_recipes):
for recipe, throughput in ordered_machine_steps:

    machine = vbs.machine_recipes[recipe][0]

    recipes.append((machine, recipe, throughput))

for machine, recipe, throughput in reversed(recipes):
    print(f"{machine:20}  {recipe:25}  {throughput:5.2f}")
print()


# vbs.deferred_apply_input("asdfghjkl", 1234)

#############################################
vbs.apply_inputs(subdivided_ordered_inputs)

for recipe in recipes:
    vbs.apply_recipe(*recipe)
#############################################
# utils.test_input_connector_creation(vbs, 6)
#############################################




# for target in reversed(targets):
#     vbs.grab_belt_lane(target)
# for i in range(len(targets)):
#     vbs.backtrack_build_belt_lane(vbs.grid_current_row, vbs.grid_current_col-1-i)


for x in vbs.belt_lanes:
    print(f"{x[1]:20.15f} {x[0]}")
print()

vbs.apply_outputs()


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



