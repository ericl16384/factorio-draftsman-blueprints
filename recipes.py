
import copy
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





def create_ordered_machine_steps(ordered_recipes, options, targets, current_rates, step_indices=None):
    if step_indices == None:
        step_indices = { recipe: len(option["steps"])-1 for recipe, option in options.items() }
    
    target_rates = {}
    for item, rate in targets.items():
        target_rate = targets[item] - current_rates[item]
        if target_rate > 0:
            target_rates[item] = target_rate


    best_recipe = None
    best_cost = np.inf

    for recipe in targets:
        if targets[recipe] <= current_rates[recipe]:
            continue

        ingredient_targets = {}
        for ing, ratio in options[recipe]["ingredient ratios"].items():
            ingredient_targets[ing] = targets[recipe]*ratio

        results = create_ordered_machine_steps(
            ordered_recipes, options, ingredient_targets,
            current_rates.copy(), step_indices.copy()
        )

        print(recipe)
        print(ingredient_targets)
        print(results)
        input()
    
    return current_rates, step_indices



    # while target_rates:




    
    # step_indices["iron-gear-wheel"] = -1

    print("create_ordered_machine_steps")
    # print(f"  {targets=}")
    # print(f"  {current_rates=}")
    print(f"  {step_indices=}")
    print(f"  {target_rates=}")

    ingredient_ratios = { recipe: 1 for recipe in target_rates }
    for recipe in ordered_recipes:
        # if recipe not in options:
        #     continue

        recipe_ratio = 1
        if recipe in ingredient_ratios:
            recipe_ratio = ingredient_ratios[recipe]
            del ingredient_ratios[recipe]
        else:
            continue

        if step_indices[recipe] < 0:
            continue

        for item, item_ratio in options[recipe]["ingredient ratios"].items():
            # if item not in options:
            #     continue

            # del ingredient_ratios[item]
            if item not in ingredient_ratios:
                ingredient_ratios[item] = 0
            ingredient_ratios[item] += item_ratio * recipe_ratio
    print(f"{ingredient_ratios=}")
    input()

    for recipe, rate in target_rates.items():
        print()
        create_ordered_machine_steps(
            ordered_recipes, options,
            ingredient_targets.copy(), current_rates.copy(), step_indices.copy()
        )
            # if ingredient_rate > current_rates[item]:
            #     create_ordered_machine_steps(ordered_recipes, options, {})

    input()


    
    
    return current_rates, step_indices
    

    # for recipe, rate in targets.items():

        



    ordered_steps = []

    

    while options:

    #     # calculate option costs

    #     # next_options = set(options.keys()).union(set(targets))

    #     # print(f"{next_options=}")
    #     # input()


    #             # rate_deficit = rate - current_rates[item]
    #             # for step in reversed(options[item]["steps"]):
    #             #     if rate_deficit <= 0:
    #             #         break
    #             #     rate_deficit -= step
    #             #     options[recipe]["prerequisites"][item] += 1

    #             # options[recipe]["total ratios"][item] = ratio
            
    #         # print(recipe)
    #         # print(options[recipe]["total ratios"])
    #         # input()
        
    #         # prerequisites
    #         # for item, rate in options[recipe]["ingredient draw"].items():

    #     break


            
                # # print()
                # # print(options[recipe]["total ratios"])
                # ingredient_ratio = options[recipe]["ingredient ratios"][prerequisite]
                # # del options[recipe]["ingredient ratios"][prerequisite]
                # for item, ratio in options[prerequisite]["total ratios"].items():
                #     # prerequisite_throughput = options[prerequisite]["steps"][-1]
                #     if item not in options[recipe]["total ratios"]:
                #         options[recipe]["total ratios"][item] = 0
                #     options[recipe]["total ratios"][item] += ingredient_ratio*ratio
            # input()
            
            # cost
            # print(f"{recipe=}")

            # for item, ratio in options[recipe]["prerequisites"].items():
            #     if ratio == 0:
            #         continue

            #     # target_rate = throughput*ratio
            #     # running_rate = current_rates[item]
            #     # if item in options:
            #     #     for rate in reversed(options[item]["steps"]):
            #     #         if running_rate >= target_rate:
            #     #             break
            #     #         running_rate += rate

            #     prev_belts = int(np.ceil(current_rates[item] / 7.5))
            #     next_belts = int(np.ceil(running_rate / 7.5))
            #     print(item, next_belts, prev_belts)
            #     print(f"          {target_rate} {running_rate}")
            #     # print(f"{ratio:5.2f} {item}")
            #     options[recipe]["belt cost"] += next_belts - prev_belts
            # cost = options[recipe]["belt cost"]
            # print(f"{cost=}")
            # print()
            
            # print(f'{options[recipe]["belt cost"]:3} {recipe:25}')
            # print()
            # print(json.dumps(options[recipe]["prerequisites"], indent=2))
            # print()
        # input()

        # if not next_options: break


        # print(json.dumps(next_options, indent=2))
        # input()


        # find lowest cost recipe

        while True:
            assert next_options

            recipe = None
            best_cost = np.inf
            for r in next_options:
                if options[r]["belt cost"] < best_cost:
                    best_cost = options[r]["belt cost"]
                    recipe = r
            assert recipe

            print(f"{options[r]["prerequisites"]}")

            if options[r]["prerequisites"]:
                next_options = set(options[r]["prerequisites"])
            else:
                break
            

        # apply recipe

        print("apply recipe:", recipe)
        input()

        throughput = options[recipe]["steps"].pop()

        for item, rate in options[recipe]["ingredient draw"].items():
            current_rates[item] -= rate
            assert current_rates[item] >= 0
        current_rates[recipe] += throughput

        ordered_steps.append((recipe, throughput))

        if not options[recipe]["steps"]:
            del options[recipe]
        
        for option in options.values():
            if recipe in option["prerequisites"]:
                option["prerequisites"][recipe] -= 1
                if option["prerequisites"][recipe] <= 0:
                    del option["prerequisites"][recipe]

        # print(current_rates)
        # input()
        


    # print(json.dumps(options, indent=2))
    # print(json.dumps(remaining_steps, indent=2))
    # print()

    return ordered_steps



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


    open_list = []
    closed_set = set()

    ordered_recipes = []
    required_inputs = set()

    open_list.extend(targets.keys())


    while len(open_list) > 0:

        current_recipe = open_list.pop()
        closed_set.add(current_recipe)

        # print(current_recipe)

        if current_recipe not in draftsman_recipes.raw:
            # print(" ", "-- no recipe --")
            # print()
            required_inputs.add(current_recipe)
            continue

        elif current_recipe not in machine_recipes:
            # print(" ", "-- recipe not allowed --")
            # print()
            required_inputs.add(current_recipe)
            continue

        if current_recipe in ordered_recipes:
            ordered_recipes.remove(current_recipe)
        ordered_recipes.append(current_recipe)

        assert len(draftsman_recipes.raw[current_recipe]["results"]) == 1
        assert draftsman_recipes.raw[current_recipe]["results"][0]["name"] == current_recipe

        for ingredient in draftsman_recipes.raw[current_recipe]["ingredients"]:
            name = ingredient["name"]

            # if name not in closed_set:
            open_list.append(name)

            # print(" ", name)
        # print()
    

    return ordered_recipes, sorted(required_inputs)







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

        full_belts, remainder = divmod(throughputs[r], throughput_constraint)
        if remainder > 0:
            lanes.append((r, remainder))
        for _ in range(int(full_belts)):
            lanes.append((r, throughput_constraint))

        # remaining_throughput = throughputs[r]
        # while remaining_throughput > throughput_constraint:
        #     remaining_throughput -= throughput_constraint 

        #     lanes.append((r, throughput_constraint))
        # lanes.append((r, remaining_throughput))

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
    
    # def evaluate_rate(self, rate):
    #     rates = { self.name: rate }

    #     for ing in self.ingredients:
    #         ing.evaluate_rate(self, )


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

    
