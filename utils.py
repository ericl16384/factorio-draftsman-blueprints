


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

# warnings.filterwarnings("error", category=draftsman.warning.OverlappingObjectsWarning)
warnings.filterwarnings("error", category=draftsman.warning.UnknownItemWarning)

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
        # self.ordered_belt_id_list = []

        self.grid = np.full((1000, 1000), -1)
        self.col = 0
        self.row = 0
        
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

        self.belt_lane_next_rows = []


        self.debug_working_bp_history = BlueprintBook()
    
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
    
    def add_bp(self, bp_name, modifying_function=None):
        # bottom-left align
        # intended to eventually be top-left align

        bp_index = self.blueprint_book_bp_names.index(bp_name)
        g = self.working_bp.groups.append(
            self.blueprint_book_groups[bp_index],
            copy=True,
            position=(self.col, -self.row)
        )

        if modifying_function != None:
            modifying_function(g)
    
    def offset_cursor(self, rows, cols):
        self.row += rows
        self.col += cols
        
        # self.add_debug_history()
    
    def add_debug_history(self):
        print("adding debug history", self.row, self.col)

        with warnings.catch_warnings():
            warnings.simplefilter("ignore", draftsman.warning.OverlappingObjectsWarning)

            debug_bp = Blueprint()
            for g in self.working_bp.groups:
                debug_bp.groups.append(g)
            debug_cursor = draftsman.entity.new_entity(
                "wooden-chest",
                position=(self.col+0.5, -self.row-0.5)
            )
            debug_bp.entities.append(debug_cursor)
            self.debug_working_bp_history.blueprints.append(debug_bp)

    def add_grid_component(self, name_id, row, col, modifying_function=None):     #, override_b_id=None):

        raise NotImplementedError

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

        if name_id == "belt up":
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

        for item, rate in reversed(inputs):
            def f(g):
                creative_sources = g.find_entities_filtered(name="creative-mod_item-source")
                for c in creative_sources:
                    for i in range(len(c.filters)):
                        c.filters[i].name = item
                #     print(c.filters)
                # print(recipe)
                # input()

            self.add_belt_lane(item, rate)
            self.belt_lane_next_rows[-1] += 2

            self.add_bp("creative start", f)
            self.offset_cursor(0, 1)
        # self.row += 1

        # self.row += max(len(inputs)-2, 0)
        # self.row += len(inputs)
        self.offset_cursor(len(inputs), -1)
    
    # def apply_outputs(self)

    def create_input_connector(self, requesting_belt_lanes):
        assert len(requesting_belt_lanes) > 0


        if len(requesting_belt_lanes) == 1:
            for item, rate in requesting_belt_lanes:

                self.grab_belt_lane(item)
                self.extract_items_from_bus(item, rate)
                
                if self.belt_lanes[-1][1] == 0:
                    self.drop_belt_lane()
                else:
                    self.add_bp("splitter")
                    self.offset_cursor(1, 1)
                
                self.add_debug_history()

                self.add_bp("belt right")
                self.offset_cursor(0, 1)
        
        elif len(requesting_belt_lanes) == 2:
            drop_history = []

            for item, rate in requesting_belt_lanes:

                self.grab_belt_lane(item)
                self.extract_items_from_bus(item, rate)
                
                drop_history.append(self.belt_lanes[-1][1] == 0)
                if drop_history[-1]:
                    self.drop_belt_lane()
                    self.offset_cursor(0, -1)
                else:
                    self.add_bp("splitter")
                    self.offset_cursor(1, 0)

                self.add_debug_history()


            # if drop_history[-2:] == [True, True]:
            #     self.add_bp("belt right")
            #     self.offset_cursor(0, 1)
            #     self.add_bp("belt up")
            #     self.offset_cursor(1, 1)
            #     self.add_debug_history()

            # if drop_history[-2:] == [False, False]:
            #     self.offset_cursor(0, 1)
            #     self.add_debug_history()
            
            # top wiggle
            # if drop_history[-2:] != [True, True]:
            self.offset_cursor(0, 1)
            self.add_bp("belt right")
            self.offset_cursor(0, 1)
            self.add_bp("belt down")
            self.offset_cursor(-1, 0)
            self.add_bp("belt right")
            self.add_debug_history()

            # bottom wiggle
            # if drop_history[0]:
            if not drop_history[1]:
            # if drop_history[-2:] != [False, True]:
                self.offset_cursor(-1, -1)
                self.add_bp("belt right")
                self.offset_cursor(0, 1)
                self.add_bp("belt up")
                self.offset_cursor(1, 0)
                self.add_debug_history()

            # if drop_history[-2:] == [False, False]:
            #     self.offset_cursor(-1, -1)
            #     self.add_bp("belt right")
            #     self.offset_cursor(0, 1)
            #     self.add_bp("belt up")
            #     self.offset_cursor(1, 1)
            #     self.add_debug_history()

            # if drop_history[-2:] == [False, True]:
            #     self.offset_cursor(0, 1)
            #     self.add_debug_history()
            
            self.offset_cursor(0, 1)

            self.add_bp("creative void")

        else:
            assert False


        ################################################
        # elements = 2
        # for _ in range(elements):
        #     self.add_bp("simple craft")
        #     self.offset_cursor(0, 6)
        # self.offset_cursor(6, -6*elements-1)
        # self.add_belt_lane("iron-gear-wheels", rate/2)

        # self.add_bp("belt up")
        # self.offset_cursor(1, 0)

        # self.add_debug_history()
        ################################################
    
    def apply_recipe(self, machine, recipe, throughput):

        self.add_debug_history()

        assert throughput > 0

        ingredient_ratios = ru.get_recipe_ingredient_ratios(recipe)
        ingredients = [i["name"] for i in draftsman_recipes.raw[recipe]["ingredients"]]

        time = ru.get_recipe_time(recipe)
        speed = draftsman.entity.new_entity(machine).prototype["crafting_speed"]
        output_amount = draftsman_recipes.raw[recipe]["results"][0]["amount"]
        multiplicity = int(np.ceil(throughput * time / speed / output_amount))

        output_offset = len(ingredients)-1

        grab_operations = []
        for ingredient in ingredients:

            grab_operations.append(self.grab_belt_lane(ingredient))

            ingredient_rate = throughput * ingredient_ratios[ingredient]
            self.extract_items_from_bus(ingredient, ingredient_rate)

            if self.belt_lanes[-1][1] == 0:
                self.drop_belt_lane()

            self.add_debug_history()

            self.offset_cursor(0, -1)
        self.offset_cursor(0, 1)
            

        def set_recipe(g):
            assembling_machines = g.find_entities_filtered(name=machine)
            for asm in assembling_machines:
                asm.recipe = recipe

        if len(ingredients) == 1:

            self.add_bp("one input connector")
            self.offset_cursor(0, 1)
            
            elements = int(np.ceil(multiplicity/2))
            for i in range(elements):
                assert machine in ("assembling-machine-1", "electric-furnace")
                if machine == "assembling-machine-1":
                    self.add_bp("simple craft", set_recipe)
                elif machine == "electric-furnace":
                    self.add_bp("smelting", set_recipe)
                self.offset_cursor(0, 6)
            self.offset_cursor(6, -6*elements-1)

        elif len(ingredients) == 2:

            self.offset_cursor(-2, 0)
            self.add_bp("two input connector")
            self.offset_cursor(1, 2)

            elements = int(np.ceil(multiplicity/2))
            for i in range(elements):
                self.add_bp("simple craft", set_recipe)
                self.offset_cursor(0, 6)
            self.offset_cursor(6, -6*elements-1)
        
        elif len(ingredients) == 3:

            self.offset_cursor(-4, 0)
            self.add_bp("three input connector")
            self.offset_cursor(2, 3)

            elements = int(np.ceil(multiplicity/2))
            for i in range(elements):
                self.add_bp("advanced craft", set_recipe)
                self.offset_cursor(0, 6)
            self.offset_cursor(7, -6*elements-1)

        else:
            assert False

        for i in range(output_offset):
            self.add_bp("left belt")
            self.offset_cursor(0, -1)
        self.add_bp("belt up")
        self.offset_cursor(1, 0)

        self.add_belt_lane(recipe, throughput)

    
    def show_image(self, block=True):
        assert False

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
    
    def add_belt_lane(self, item, rate):
        self.belt_lanes.append([item, rate])
        self.belt_lane_next_rows.append(self.row)
        # self.ordered_belt_id_list.append(item)

        print("add: ", item)
    
    def drop_belt_lane(self):
        "drops the most recent belt lane"

        item = self.belt_lanes.pop()
        self.belt_lane_next_rows.pop()

        print("drop:", item)

        return item
    
    def backtrack_build_belt_lane(self, start_row, start_col):
        raise AssertionError

        splitters = (
            self.blueprint_book_bp_names.index("priority splitter"),
            self.blueprint_book_bp_names.index("filter splitter"),
        )

        row = start_row-1
        col = start_col

        while True:

            if self.grid[row, col] == -1:
                self.add_grid_component("belt up", row, col)

            elif self.grid[row, col] in splitters:
                col += 1

                if self.grid[row, col] not in splitters:
                    break
            else:
                break

            row -= 1


            # assert row >= 0
            if row < 0:
                break


    def grab_belt_lane(self, item, belt_max_rate=7.5):
        #  0 index is oldest side
        # -1 index is newest side
            
        # print()
        # print([f"{x[0][0]} {x[1]}" for x in self.belt_lanes])


        operations = []
        grabbed = False

        # print("goal:", item)
        # print(json.dumps(self.belt_lanes, indent=2))

        for i in range(len(self.belt_lanes)-1):
            if grabbed:
                pass
            elif self.belt_lanes[i][0] == item:
                grabbed = True
            else:
                operations.append(None)
                continue

            a = self.belt_lanes[i]
            b = self.belt_lanes[i+1]

            if self.belt_lanes[i][0] == self.belt_lanes[i+1][0]:
                operations.append("splitter")

                total_rate = a[1] + b[1]
                a[1] = min(total_rate, belt_max_rate)
                b[1] = total_rate - a[1]

            else:
                operations.append("filter splitter")

                self.belt_lanes[i] = b
                self.belt_lanes[i+1] = a
                
        # operations.append("splitter")
        
        # print(json.dumps(operations, indent=2))
        # print(json.dumps(self.belt_lanes, indent=2))
        # input()
        
        # print([f"{x[0][0]} {x[1]}" for x in self.belt_lanes])

        # print(self.belt_lane_next_rows)

        self.offset_cursor(-len(self.belt_lanes)+2, -len(self.belt_lanes)+1)
        
        # self.add_debug_history()

        def f(g):
            for s in g.find_entities_filtered(type="splitter"):
                s.filter.name = item
        
        splitter_chain_has_started = False
        for j, op in enumerate(operations):

            if op != None:
                vertical_belt_length = self.row - self.belt_lane_next_rows[j]
                vertical_offset = 0

                if splitter_chain_has_started:
                    vertical_belt_length -= 1
                    vertical_offset -= 1
                splitter_chain_has_started = True

                if vertical_belt_length > 0:
                    self.offset_cursor(vertical_offset - vertical_belt_length, 0)
                    for _ in range(vertical_belt_length):
                        self.add_bp("belt up")
                        self.offset_cursor(1, 0)
                    if vertical_offset != 0:
                        self.offset_cursor(-vertical_offset, 0)
                        
                self.belt_lane_next_rows[j] = self.row+1

            if op == None:
                pass
                # self.add_bp("belt up")
            elif op == "splitter":
                self.add_bp(op)
            elif op == "priority splitter":
                self.add_bp(op)
            elif op == "merge splitter":
                self.add_bp(op)
            elif op == "filter splitter":
                self.add_bp(op, f)
            else:
                assert False
            self.offset_cursor(1, 1)

        # self.belt_lane_next_rows[-1] = self.row+1
        # self.add_bp("priority splitter")
        # self.offset_cursor(1, 1)
        
        # self.add_debug_history()

    def extract_items_from_bus(self, item, rate):

        remaining_rate = rate

        for i in range(len(self.belt_lanes)-1, -1, -1):
            x = self.belt_lanes[i]
            if x[0] == item:
                reduction = min(remaining_rate, x[1])
                remaining_rate -= reduction
                x[1] -= reduction
        
        print(f"{self.belt_lanes[-1][1]:25.20f} {self.belt_lanes[-1]}")

        #         print(f"{x[0]:20} {x[1]+reduction:5.2f} - {reduction:.2f} = {x[1]:5.2f}")
        #     else:
        #         print(f"{x[0]:20} {x[1]:5.2f}")
        
        # print(f"{'':18}-> {rate:5.2f}")
        
        # print()


