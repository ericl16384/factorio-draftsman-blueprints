import json
import numpy as np

from draftsman.data import recipes as draftsman_recipes
import draftsman.entity





# # print(json.dumps(draftsman_recipes.raw["iron-plate"], indent=4))

# print(json.dumps(list(draftsman_recipes.categories["crafting"]), indent=4))

# print(json.dumps(draftsman_recipes.raw["electronic-circuit"], indent=4))








# print(json.dumps(draftsman_recipes.for_machine["assembling-machine-1"], indent=2))

# import sys
# sys.exit()




# allowed_machines = [
#     "assembling-machine-1"
# ]

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

# desired_open_quantity_targets = {
#     # "iron-gear-wheel": 7.5,

#     # "automation-science-pack": 7.5,
#     "logistic-science-pack": 7.5,
#     # "chemical-science-pack": 7.5,
#     # "military-science-pack": 7.5,
#     # "production-science-pack": 7.5,
#     # "utility-science-pack": 7.5,
#     # "space-science-pack": 7.5,
# }




def create_custom_recipe(recipe_name, ingredients, output_amount=1):
    raw_recipe = {
        "ingredients": [],
        "name": recipe_name,
        "results": [
            {
                "name": recipe_name,
                "amount": output_amount,
                "type": "item"
            }
        ],
        "type": "recipe"
    }
    for name, amount in ingredients.items():
        raw_recipe["ingredients"].append(
            {
                "name": name,
                "amount": amount,
                "type": "item"
            }
        )
    return raw_recipe

def validate_raw_recipe(raw_recipe, recipe_name):
    assert raw_recipe["name"] == recipe_name
    assert len(raw_recipe["results"]) == 1
    assert raw_recipe["results"][0]["name"] == recipe_name
    assert raw_recipe["results"][0]["type"] == "item"
    assert raw_recipe["type"] == "recipe"
    





def get_recipe_time(recipe_name):
    recipe = draftsman_recipes.raw[recipe_name]
    if "energy_required" in recipe:
        return recipe["energy_required"]
    else:
        return 0.5

def get_recipe_ingredient_ratios(recipe_name):
    recipe = draftsman_recipes.raw[recipe_name]
    ingredient_ratios = {}

    assert len(recipe["results"]) == 1
    output_amount = recipe["results"][0]["amount"]
    for ingredient in recipe["ingredients"]:
        input_name = ingredient["name"]
        input_amount = ingredient["amount"]

        ingredient_ratios[input_name] = input_amount / output_amount
    
    return ingredient_ratios



def develop_machine_recipes(allowed_machines):

    machine_recipes = {}

    for machine in allowed_machines:
        for category in draftsman.entity.new_entity(machine).prototype["crafting_categories"]:
            for recipe in draftsman_recipes.categories[category]:
                if recipe not in machine_recipes:
                    machine_recipes[recipe] = []
                machine_recipes[recipe].append(machine)
        # for recipe in draftsman_recipes.for_machine[machine]:
        #     machine_recipes.add((recipe, machine))
    
    return machine_recipes

def develop_recipe_path(targets, machine_recipes):
    # assert allowed_machines == ["assembling-machine-1"]


    open_set = set()
    closed_set = set()

    ordered_recipes = []
    required_inputs = set()

    open_set.update(targets.keys())


    while open_set:

        current_recipe = open_set.pop()
        closed_set.add(current_recipe)

        # print(current_recipe)

        if current_recipe not in draftsman_recipes.raw:
            # print(" ", "-- no recipe --")
            # print()
            required_inputs.add(current_recipe)
            continue

        if current_recipe not in machine_recipes:
            # print(" ", "-- recipe not allowed --")
            # print()
            required_inputs.add(current_recipe)
            continue

        try:
            ordered_recipes.remove(current_recipe)
        except ValueError:
            pass
        ordered_recipes.append(current_recipe)

        assert len(draftsman_recipes.raw[current_recipe]["results"]) == 1
        assert draftsman_recipes.raw[current_recipe]["results"][0]["name"] == current_recipe

        for ingredient in draftsman_recipes.raw[current_recipe]["ingredients"]:
            name = ingredient["name"]

            # if name not in closed_set:
            open_set.add(name)

            # print(" ", name)
        # print()
    

    return ordered_recipes, required_inputs







        # if current_recipe not in open_quantity_targets:
        #     open_quantity_targets[current_recipe] = 0
        # open_quantity_targets[current_recipe] += 100 # TODO



    # open_quantity_targets = dict()
    # closed_quantity_targets = dict()
    # open_quantity_targets.update(desired_open_quantity_targets)


def develop_recipe_throughputs(targets, ordered_recipes, required_inputs, machine_recipes):
    throughputs = {}
    for x in ordered_recipes:
        throughputs[x] = 0
    for x in required_inputs:
        throughputs[x] = 0

    for recipe in ordered_recipes:

        if recipe in targets:
            throughputs[recipe] += float(targets[recipe])
        
        target_amount = throughputs[recipe]
        
        raw_recipe = draftsman_recipes.raw[recipe]

        assert len(raw_recipe["results"]) == 1
        output_amount = raw_recipe["results"][0]["amount"]
        
        for ingredient in raw_recipe["ingredients"]:
            name = ingredient["name"]
            input_amount = ingredient["amount"]
            throughputs[name] += target_amount * input_amount / output_amount

        # print(recipe)
        # print(json.dumps(throughputs, indent=2))
    
    return throughputs

def subdivide_ordered_recipes(ordered_recipes, throughputs):

    constraint_ratios = []

    # assemblies = []
    for recipe in ordered_recipes:
        ingredient_ratios = get_recipe_ingredient_ratios(recipe)

        input_constraint = max(ingredient_ratios.values())
        output_constraint = 1 #/ min(ingredient_ratios.values())
        max_constraint = max(input_constraint, output_constraint)

        constraint_ratios.append(max_constraint)

        # assembly_max_throughput = belt_max_throughput / max_constraint

        # print(ingredient_ratios)
        # print(input_constraint)
        # print(output_constraint)
        # print(assembly_max_throughput)
        # input()

    #     remaining_throughput = throughputs[recipe]
    #     while remaining_throughput > assembly_max_throughput:
    #         remaining_throughput -= assembly_max_throughput 

    #         assemblies.append((recipe, assembly_max_throughput))
    #     assemblies.append((recipe, remaining_throughput))
    
    # return assemblies

    return subdivide_ordered_lanes(ordered_recipes, throughputs, constraint_ratios)

def subdivide_ordered_lanes(ordered_lanes, throughputs, constraint_ratios=None):
    belt_max_throughput = 7.5

    ordered_throughput_constraints = [belt_max_throughput for _ in ordered_lanes]
    if constraint_ratios != None:
        for i, constraint in enumerate(constraint_ratios):
            ordered_throughput_constraints[i] = ordered_throughput_constraints[i] / constraint

    lanes = []

    for i, r in enumerate(ordered_lanes):
        throughput_constraint = ordered_throughput_constraints[i]

        remaining_throughput = throughputs[r]
        while remaining_throughput > throughput_constraint:
            remaining_throughput -= throughput_constraint 

            lanes.append((r, throughput_constraint))
        lanes.append((r, remaining_throughput))

    return lanes



class RecipeAnalysis:

    # def __new__(cls, recipe_name, _context=None, *args, **kwargs):
    #     if _context:
    #         if recipe_name in _context:
    #             return _context[recipe_name]
    #         else:
    #             instance = super(RecipeAnalysis, cls).__new__(cls)
    #             _context[recipe_name] = instance
    #             return instance
    #     else:
    #         return super(RecipeAnalysis, cls).__new__(cls)

    def __init__(self, recipe_name, allowed_recipes=None, custom_recipes=None, _context=None):

        self.name = recipe_name

        self.context = _context
        if self.context == None:
            self.context = {}
        assert recipe_name not in self.context
        self.context[recipe_name] = self
            

        self.local_incredient_ratio = 0
        self.total_ingredient_ratio = 0
        # self.output_per_second = None

        self.ingredients = {}


        self.raw_recipe = None
        if custom_recipes and self.name in custom_recipes:
            self.raw_recipe = custom_recipes[self.name]
        elif allowed_recipes and self.name not in allowed_recipes:
            pass
        elif self.name in draftsman_recipes.raw:
            self.raw_recipe = draftsman_recipes.raw[self.name]

        if self.raw_recipe:

            validate_raw_recipe(self.raw_recipe, self.name)

            output_amount = self.raw_recipe["results"][0]["amount"]

            for ing in self.raw_recipe["ingredients"]:

                ingredient_name = ing["name"]
                ingredient_amount = ing["amount"]
                ingredient_ratio = ingredient_amount / output_amount

                if ingredient_name not in self.context:
                    RecipeAnalysis(
                        ingredient_name,
                        allowed_recipes=allowed_recipes,
                        custom_recipes=custom_recipes,
                        # _current_depth=self.depth+1,
                        _context=self.context
                    )

                sub_recipe_analysis = self.context[ingredient_name]
                self.ingredients[ingredient_name] = sub_recipe_analysis

                self.local_incredient_ratio += ingredient_ratio

                self.total_ingredient_ratio += ingredient_ratio * sub_recipe_analysis.total_ingredient_ratio

                # ingredient_per_second = output_per_second * ingredient_ratio

                # result = recursive_recipe_analysis(ingredient, ingredient_per_second, depth=depth+1)

        #         sub_tree = result[0]
        #         sub_flattened_per_second = result[1]
                
        #         tree.append(sub_tree)

        #         for k, v in sub_flattened_per_second.items():
        #             if k not in flattened_per_second:
        #                 flattened_per_second[k] = 0
        #             flattened_per_second[k] += v
                
        #         tree[0]["total_ingredient_ratio"] += ingredient_ratio * sub_tree[0]["total_ingredient_ratio"]
        
        # else:
        #     tree[0]["total_ingredient_ratio"] = 1.0

        # self.flattened_inputs_per_second = {
        #     name: output_per_second,
        # }

        if len(self.ingredients) == 0:
            self.total_ingredient_ratio = 1
        
        if self.ingredients:
            # member = ". "*self.depth + self.name
            member = self.name
            print(f'RA {member:25} {self.local_incredient_ratio:5.1f} {self.total_ingredient_ratio:5.1f}')
            # print(self.context)


# class RecipeBlock:

#     def __init__(self, recipe, target_rate, machine_type):
#         self.recipe = recipe
#         self.target_rate = target_rate
#         self.machine_type = machine_type

#         self.machine_count = None

class CraftingSystem:

    def __init__(self, rate_targets, allowed_machines):
        self.rate_targets = rate_targets

        self.allowed_recipes = develop_machine_recipes(allowed_machines)

        self.recipe_context = {}
        for recipe in rate_targets:
            RecipeAnalysis(recipe, self.allowed_recipes, _context=self.recipe_context)

        # self.thr fghj



if __name__ == "__main__":

    targets = {
        "automation-science-pack": 1,
        "logistic-science-pack": 1,
        # "chemical-science-pack": 1,
        # "military-science-pack": 1,
        # "production-science-pack": 1,
        # "utility-science-pack": 1,
        # "space-science-pack": 1,
    }


    allowed_machines = [
        "assembling-machine-1",
        # "electric-furnace",
    ]

    # machine_recipes = develop_machine_recipes(allowed_machines)

    cs = CraftingSystem(targets, allowed_machines)
        
    # print(list(cs.recipe_context.keys()))
    input()


    custom_recipe_name = "[science]"
    custom_recipe = create_custom_recipe(custom_recipe_name, targets)
    # result = recursive_recipe_analysis(custom_recipe_name, 1, allowed_recipes=machine_recipes, custom_recipe=custom_recipe)
    # print(json.dumps(result, indent=2))
    print(f'{"-- recipe --":^32} {"local":5} {"total":5}')
    RecipeAnalysis(custom_recipe_name, machine_recipes, {custom_recipe_name: custom_recipe})
    input()


    ordered_recipes, required_inputs = develop_recipe_path(targets, machine_recipes)

    throughputs = develop_recipe_throughputs(targets, ordered_recipes, required_inputs, machine_recipes)

    subdivided_ordered_recipes = subdivide_ordered_recipes(ordered_recipes, throughputs)

    print(json.dumps(throughputs, indent=2))
    print(json.dumps(subdivided_ordered_recipes, indent=2))


    # print(json.dumps(draftsman_recipes.raw["copper-cable"], indent=2))

    # print(json.dumps(draftsman_recipes.raw["advanced-circuit"], indent=2))

    # print(draftsman.entity.new_entity("assembling-machine-1").prototype["crafting_speed"])
    # print(draftsman.entity.new_entity("assembling-machine-2").prototype["crafting_speed"])
    # print(draftsman.entity.new_entity("assembling-machine-3").prototype["crafting_speed"])







# print("open_set =", json.dumps(list(open_set), indent=2))
# print("closed_set =", json.dumps(list(closed_set), indent=2))
# # print("open_quantity_targets =", json.dumps(dict(open_quantity_targets), indent=2))
# print("ordered_recipes =", json.dumps(list(ordered_recipes), indent=2))
# print("required_inputs =", json.dumps(list(required_inputs), indent=2))
# print()

    
