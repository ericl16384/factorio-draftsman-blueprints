


import numpy as np
import matplotlib.pyplot as plt
import json


from draftsman.blueprintable import *
from draftsman.constants import Direction
from draftsman.entity import *
from draftsman.data import recipes as draftsman_recipes


import recipes as ru



import warnings
import draftsman.warning

warnings.filterwarnings("error", category=draftsman.warning.OverlappingObjectsWarning)
warnings.filterwarnings("ignore", category=draftsman.warning.UnknownKeywordWarning)

with open("reference_blueprint_book.txt") as f:
    BlueprintBook.from_string(f.read())





# def connect_all_power_poles(bp):

#     print()
#     print("start power connections")
#     bp.generate_power_connections()
#     print("end power connections")
#     print()

#     return

#     poles = bp.find_entities_filtered(type="electric-pole")

#     print()
#     print("TODO power connections")
#     print()
#     return

#     for i in range(len(poles)):
#         for j in range(i+1, len(poles)):
#             with warnings.catch_warnings(record=True) as captured_warnings:
#                 # warnings.simplefilter("always")  # Ensure all warnings are caught
                
#                 bp.add_power_connection(poles[i], poles[j])

#                 success = True
#                 assert len(captured_warnings) < 2
#                 for w in captured_warnings:
#                     assert w.category == draftsman.warning.ConnectionDistanceWarning
#                     success = False

#                     # print(f"Warning Category: {w.category.__name__}")
#                     # print(f"Message: {w.message}")




# class SubassemblyInstance

# class Subassembly:

#     def __init__(self, draftsman_bp_group):
#         self.size = (0, 0)
#         self.pos = (0, 0)

#         self.draftsman_bp_group = draftsman_bp_group

#         self.child_subassemblies = []
    
    # def create_instance(self):
    #     instance = self.__class__()

    #     instance.size = self.size

    #     return instance

# class ExtendableSubassembly(Subassembly):

#     def __init__(self, ):
#         super().__init__()

#         self.



class VisualBeltSystem:

    def __init__(self, reference_blueprint_book_file) -> None:
        self.belt_lanes = []
        self.ordered_belt_id_list = []

        self.grid = np.full((1000, 1000), -1)
        self.grid_current_col = 0
        self.grid_current_row = 0
        
        with open(reference_blueprint_book_file) as f:
            self.reference_blueprint_book = BlueprintBook.from_string(f.read())

        self.blueprint_book_bp_names = []

        self.blueprint_book_groups = []
        
        for b in self.reference_blueprint_book.blueprints:
            self.blueprint_book_bp_names.append(b.label)

            g = Group()
            g.entities = b.entities
            g.extra_keys = b.extra_keys
            g.groups = b.groups
            g.parameters = b.parameters
            # # g.schedules = b.schedules
            # # g.stock_connections = b.stock_connections
            g.tiles = b.tiles
            # # # g.wires = b.wires
            bounding_box = g.get_world_bounding_box()
            g.translate(
                -np.floor(bounding_box.world_top_left[0]),
                -np.ceil(bounding_box.world_bot_right[1])
            )
            self.blueprint_book_groups.append(g)


        self.working_bp = Blueprint()


        self.total_rate_targets = {}
        self.remaining_rate_targets = {}

        self.allowed_machines = []
        self.machine_recipes = {}
    
    def update_rate_targets(self, rate_targets):
        assert len(self.total_rate_targets) == 0
        assert len(self.remaining_rate_targets) == 0
        # for rt in rate_targets:
        #     assert rt not in self.total_rate_targets
        #     assert rt not in self.remaining_rate_targets

        self.total_rate_targets.update(rate_targets)
        self.remaining_rate_targets.update(rate_targets)
    
    def update_allowed_machines(self, machines):
        assert len(self.allowed_machines) == 0
        assert len(self.machine_recipes) == 0

        self.allowed_machines = []
        self.allowed_machines.extend(machines)

        self.machine_recipes = ru.develop_machine_recipes(self.allowed_machines)

    
    def export_bp(self, autoconnect_all_power=True):
        # final_bp = Blueprint.from_string(self.working_bp.to_string())

        if autoconnect_all_power:
            # final_bp.generate_power_connections()
            self.working_bp.generate_power_connections()
        
        # return final_bp
        return self.working_bp
    
    def add_bp(self, bp_index, row, col, modifying_function=None):
        # bottom-left align
        # intended to eventually be top-left align

        # g = Group()
        # g.entities = self.reference_blueprint_book.blueprints[bp_index].entities
        
        # bounding_box = g.get_world_bounding_box()
        # min_corner = np.floor(bounding_box.world_top_left)
        # max_corner = np.ceil(bounding_box.world_bot_right)
        # for entity in g.entities:
        #     entity.position -= (min_corner[0], max_corner[1])
        
        # if modifying_function != None:
        #     modifying_function(g)

        # self.working_bp.groups.append(g, position=(col, -row))

        g = self.working_bp.groups.append(self.blueprint_book_groups[bp_index], copy=True, position=(col, -row))
        
        if modifying_function != None:
            modifying_function(g)

    def add_grid_component(self, name_id, row, col, modifying_function=None):     #, override_b_id=None):
        b_id = self.blueprint_book_bp_names.index(name_id)

        assert row >= 0
        assert col >= 0

        # if override_b_id != None:
        #     b_id = override_b_id

        # print(b_id)
        
        # self.working_bp.groups.append(self.bp_groups[b_id], position=(col, -row))

        # print(name_id)
        self.add_bp(b_id, row, col, modifying_function)

        # fb = Subassembly()

        if name_id == "belt":
            # fb.size = (1, 1)

            self.grid[row, col] = b_id

        elif name_id == "one input connector":
            # fb.size = (1, 1)

            self.grid[row, col] = b_id
            self.grid[row, col+1] = b_id
            self.grid[row+1, col+1] = b_id
            self.grid[row+7, col+1] = b_id

        elif name_id == "two input connector":
            # fb.size = (1, 1)

            self.grid[row, col] = b_id
            self.grid[row, col+1] = b_id
            self.grid[row+1, col+1] = b_id
            self.grid[row+1, col+2] = b_id
            self.grid[row+2, col] = b_id
            self.grid[row+2, col+1] = b_id
            self.grid[row+2, col+2] = b_id
            self.grid[row+3, col+1] = b_id
            self.grid[row+3, col+2] = b_id
            self.grid[row+8, col+1] = b_id
            self.grid[row+8, col+2] = b_id

        elif name_id == "three input connector":
            # fb.size = (1, 1)

            # self.add_grid_component("two input connector", row+2, col, b_id)
            self.grid[row, col] = b_id
            self.grid[row, col+1] = b_id
            self.grid[row+1, col+1] = b_id
            self.grid[row+1, col+2] = b_id
            self.grid[row+2, col+2] = b_id
            self.grid[row+2, col+3] = b_id
            self.grid[row+3, col+3] = b_id
            self.grid[row+4, col+3] = b_id
            self.grid[row+10, col+3] = b_id
            
            self.grid[row+2, col] = b_id
            self.grid[row+2, col+1] = b_id
            self.grid[row+2+1, col+1] = b_id
            self.grid[row+2+1, col+2] = b_id
            self.grid[row+2+2, col] = b_id
            self.grid[row+2+2, col+1] = b_id
            self.grid[row+2+2, col+2] = b_id
            self.grid[row+2+3, col+1] = b_id
            self.grid[row+2+3, col+2] = b_id
            self.grid[row+2+8, col+1] = b_id
            self.grid[row+2+8, col+2] = b_id

        elif name_id == "simple craft":
            # fb.size = (6, 7)

            for x in range(6):
                for y in range(7):
                    if y in [1, 5] and x in [0, 3, 5]:
                        continue
                    self.grid[row+y, col+x] = b_id

        elif name_id == "advanced craft":
            # fb.size = (6, 8)

            for x in range(6):
                for y in range(8):
                    if y == 2 and x == 5: continue
                    if y == 6 and x in [0, 3, 5]: continue
                    self.grid[row+y, col+x] = b_id

        elif name_id == "priority splitter":
            # fb.size = (2, 1)

            self.grid[row, col] = b_id
            self.grid[row, col+1] = b_id

        elif name_id == "filter splitter":
            # fb.size = (2, 1)

            self.grid[row, col] = b_id
            self.grid[row, col+1] = b_id

        elif name_id == "creative start":
            self.grid[row, col] = b_id

        elif name_id == "smelting":
            # fb.size = (6, 7)

            for x in range(6):
                for y in range(7):
                    if y in [1, 5] and x in [0, 3, 5]:
                        continue
                    self.grid[row+y, col+x] = b_id

        else:
            assert False
    
    def apply_inputs(self, inputs):
        assert len(self.belt_lanes) == 0

        for item in inputs:
            def f(g):
                creative_sources = g.find_entities_filtered(name="creative-mod_item-source")
                for c in creative_sources:
                    for i in range(len(c.filters)):
                        c.filters[i].name = item
                #     print(c.filters)
                # print(recipe)
                # input()

            self.add_grid_component("creative start", self.grid_current_row, self.grid_current_col, f)
            self.add_belt_lane(item)
            self.grid_current_col += 1
        self.grid_current_row += 1

        self.grid_current_row += max(len(inputs)-2, 0)
    
    # def apply_outputs(self)
    
    def apply_recipe(self, machine, recipe, multiplicity):

        assert multiplicity > 0

        if multiplicity == 0:
            ingredients = []
        else:
            ingredients = [i["name"] for i in draftsman_recipes.raw[recipe]["ingredients"]]

        # print("recipe:", recipe)
        grabbed = 0
        for g, ingredient in enumerate(ingredients):
            if self.grab_belt_lane(ingredient):
                grabbed += 1
        if grabbed:
            self.grid_current_row += 1
        self.grid_current_row -= grabbed*2

        

        def set_recipe(g):
            assembling_machines = g.find_entities_filtered(name=machine)
            for asm in assembling_machines:
                asm.recipe = recipe


        if len(ingredients) == 0:
        
            def f(g):
                # print(g.entities[0])
                creative_sources = g.find_entities_filtered(name="creative-mod_item-source")
                for c in creative_sources:
                    for i in range(len(c.filters)):
                        c.filters[i].name = recipe
                #     print(c.filters)
                # print(recipe)
                # input()

            self.add_grid_component("creative start", self.grid_current_row, self.grid_current_col, f)
            self.grid_current_row += 1
            self.grid_current_col += 1

        elif len(ingredients) == 1:

            self.add_grid_component("one input connector", self.grid_current_row, self.grid_current_col-1)
            self.grid_current_row += 1
            
            for i in range(int(np.ceil(multiplicity/2))):
                assert machine in ("assembling-machine-1", "electric-furnace")
                if machine == "assembling-machine-1":
                    self.add_grid_component("simple craft", self.grid_current_row, self.grid_current_col+1+i*6, set_recipe)
                elif machine == "electric-furnace":
                    self.add_grid_component("smelting", self.grid_current_row, self.grid_current_col+1+i*6, set_recipe)
            self.grid_current_row += 7
            self.grid_current_col += 1

        elif len(ingredients) == 2:

            self.add_grid_component("two input connector", self.grid_current_row, self.grid_current_col-1)
            self.grid_current_row += 2

            for i in range(int(np.ceil(multiplicity/2))):
                self.add_grid_component("simple craft", self.grid_current_row, self.grid_current_col+2+i*6, set_recipe)
            self.grid_current_row += 7
            self.grid_current_col += 1
        
        elif len(ingredients) == 3:

            self.add_grid_component("three input connector", self.grid_current_row, self.grid_current_col-1)
            self.grid_current_row += 3

            for i in range(int(np.ceil(multiplicity/2))):
                self.add_grid_component("advanced craft", self.grid_current_row, self.grid_current_col+3+i*6, set_recipe)
            self.grid_current_row += 8
            self.grid_current_col += 1

        else:
            assert False
        
        self.add_belt_lane(recipe)

        # self.show_image()

        # print(self.belt_lanes)

        # # # for i, item in enumerate(self.belt_lanes):
        # # #     self.grid[self.grid_current_row+i, self.grid_current_col] = self.ordered_belt_id_list.index(item)
        # # # self.grid_current_col += 1
        # # # print(self.belt_lanes)

        # self.grid_current_col += 1
    
    def show_image(self, block=True):
        plt.imshow(self.get_image())
        plt.axis("off")
        plt.gca().invert_yaxis()
        plt.show(block=block)

    def get_image(self):
        color_list = [
            (255, 0, 0),
            (0, 255, 0),
            (0, 0, 255),
            (255, 255, 0),
            (0, 255, 255),
            (255, 0, 255),
            (255, 165, 0),
            (128, 0, 128),
            (127, 255, 0),
            (0, 191, 255),
            (255, 20, 147),
            (255, 215, 0),
            (138, 43, 226),
            (0, 128, 128),
            (255, 127, 80),
            (0, 255, 127),
            (0, 0, 0),
        ]

        image = np.zeros((self.grid.shape[0], self.grid.shape[1], 3), dtype=int)
        # image = np.zeros((len(self.belt_lanes)+2, self.grid_current_col+1, 3))
        max_row = 0
        max_col = 0
        for row in range(image.shape[0]):
            for col in range(image.shape[1]):
                i = self.grid[row, col]
                image[row, col] = color_list[i]
                if i > -1:
                    max_row = max(max_row, row)
                    max_col = max(max_col, col)
        image = image[:max_row+1, :max_col+1]
            
        return image
    
    def add_belt_lane(self, item):
        self.belt_lanes.append(item)
        self.ordered_belt_id_list.append(item)

        # print(item)
    
    def backtrack_build_belt_lane(self, start_row, start_col):
        splitters = (
            self.blueprint_book_bp_names.index("priority splitter"),
            self.blueprint_book_bp_names.index("filter splitter"),
        )

        row = start_row-1
        col = start_col

        while True:
            # self.show_image()

            if self.grid[row, col] == -1:
                self.add_grid_component("belt", row, col)

            elif self.grid[row, col] in splitters:
                col += 1

                if self.grid[row, col] not in splitters:
                    break
            else:
                break

            row -= 1

            # self.show_image()

            assert row >= 0


    def grab_belt_lane(self, item):
        #  0 index is oldest side
        # -1 index is newest side

        first_index = np.inf
        last_index = -np.inf
        success = False
        for i in range(len(self.belt_lanes)):
            if self.belt_lanes[i] == item:
                first_index = min(first_index, i)
                last_index = max(last_index, i)
                success = True
        assert success, f"ingredient {item} not found in belt_lanes"

        shift = len(self.belt_lanes)-1 - first_index #grab
        if shift == 0:
            # print("00 shift:", item)
            return False
        # print(f"{shift:2} shift:", item)

        def f(g):
            for s in g.find_entities_filtered(type="splitter"):
                s.filter.name = item
                # print(s.filter)
                # input()
        
        row = self.grid_current_row+1-shift
        col = self.grid_current_col-1-shift
        
        self.backtrack_build_belt_lane(row, col)

        # print(json.dumps(self.belt_lanes, indent=2))
        # print("shift", shift, "for", item)

        # print(row, col)

        for i in range(shift):
            # row = self.grid_current_row+-i
            # col = self.grid_current_col-2  -i

            # row += 1
            # col += 1

            # print(self.belt_lanes[-(i+2)])
            # print(self.belt_lanes[-(i+1)])
            # print()

            # print()
            # print(json.dumps(self.belt_lanes, indent=2))
            # print(first_index+i, first_index+i+1)
            # print(self.belt_lanes[first_index+i], self.belt_lanes[first_index+i+1])

            if self.belt_lanes[first_index+i] == self.belt_lanes[first_index+i+1]:
                self.add_grid_component("priority splitter", row+i, col+i)
                self.backtrack_build_belt_lane(row+i, col+i+1)

                # print("priority splitter")

            else:
                self.add_grid_component("filter splitter", row+i, col+i, f)
                a = self.belt_lanes[first_index+i]
                b = self.belt_lanes[first_index+i+1]
                self.belt_lanes[first_index+i+1] = a
                self.belt_lanes[first_index+i] = b
                # self.belt_lanes[first_index+i:first_index+i+2] = self.belt_lanes[first_index+i+2:first_index+i:-1]
                
                # print("filter splitter")

            # self.show_image()
        
        # self.belt_lanes[last_index:] = self.belt_lanes[last_index+1:] + [self.belt_lanes[last_index]]

        self.grid_current_row += 2

        # print(json.dumps(self.belt_lanes, indent=2))

        return True
    


