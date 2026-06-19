# from pathfinding.core.grid import Grid
# from pathfinding.finder.bi_a_star import BiAStarFinder

import numpy as np

import belt_pathfinding as bp




class FactorioSubassemblyPrototype:
    def __init__(self, width, height, inputs, outputs) -> None:
        self.width = width
        self.height = height
        self.inputs = inputs
        self.outputs = outputs

class FactorioSubassemblyEntity:

    # starts at 1 so that 0 can represent empty
    _entity_counter = 1

    def __init__(self, prototype, x, y) -> None:
        self.entity_id = FactorioSubassemblyEntity._entity_counter
        FactorioSubassemblyEntity._entity_counter += 1

        self.prototype = prototype
        self.x = x
        self.y = y
    
    def apply_to_occupany_bitmap(self, occupancy_bitmap):
        # Map x to columns and y to rows
        occupancy_bitmap[self.y : self.y + self.prototype.height, self.x : self.x + self.prototype.width] = self.entity_id
        # for proto_x, proto_y in self.prototype.outputs:
        #     occupancy_bitmap[self.y + proto_y, self.x + proto_x] = self.entity_id
        # for proto_x, proto_y in self.prototype.inputs:
        #     occupancy_bitmap[self.y + proto_y, self.x + proto_x] = self.entity_id






subassembly_prototypes = {
    "foo": FactorioSubassemblyPrototype(6, 7, [[5, 6]], [[6, 0]])
}

subassembly_entities = {}
def new_subassembly(subassembly_prototypes, prototype_id, x, y):
    entity = FactorioSubassemblyEntity(subassembly_prototypes[prototype_id], x, y)
    subassembly_entities[entity.entity_id] = entity



def create_belt_connection(start, end, occupancy_bitmap, belt_bitmap, starting_direction=None):
    obstacle_bitmap = occupancy_bitmap | belt_bitmap

    bitmap_overwrites = [(end, 0)]
    for (x, y), value in bitmap_overwrites:
        obstacle_bitmap[y, x] = value

    path = bp.astar(start, end, obstacle_bitmap, starting_direction)
    bp.apply_belt_path(belt_bitmap, path)
    print(path)

def connect_subassembly_entities(subassembly_entities, occupancy_bitmap, belt_bitmap, provider_id, requester_id, provider_output_index, requester_input_index):
    provider = subassembly_entities[provider_id]
    requester = subassembly_entities[requester_id]
    start = (provider.x + provider.prototype.outputs[provider_output_index][0], provider.y + provider.prototype.outputs[provider_output_index][1])
    end = (requester.x + requester.prototype.inputs[requester_input_index][0], requester.y + requester.prototype.inputs[requester_input_index][1])
    create_belt_connection(start, end, occupancy_bitmap, belt_bitmap, starting_direction=None)








new_subassembly(subassembly_prototypes, "foo", 20, 3)
new_subassembly(subassembly_prototypes, "foo", 60, 7)
# new_subassembly(subassembly_prototypes, "foo", 50, 5)



bitmap_shape         = (20, 100)
occupancy_bitmap    = np.zeros(bitmap_shape, dtype=int)
belt_bitmap         = np.zeros(bitmap_shape, dtype=int)

belt_bitmap[bitmap_shape[0]-1, :] = bp.BELT_TO_EAST
belt_bitmap[:, bitmap_shape[1]-1] = bp.BELT_TO_EAST

for subassembly_entity in subassembly_entities.values():
    subassembly_entity.apply_to_occupany_bitmap(occupancy_bitmap)








create_belt_connection((0, 0), (2, 2), occupancy_bitmap, belt_bitmap)

# create_belt_connection((26, 0), (100, 0), occupancy_bitmap, belt_bitmap)
# create_belt_connection((26, 1), (100, 1), occupancy_bitmap, belt_bitmap)
# create_belt_connection((26, 2), (100, 2), occupancy_bitmap, belt_bitmap)

connect_subassembly_entities(subassembly_entities, occupancy_bitmap, belt_bitmap, 1, 2, 0, 0)
connect_subassembly_entities(subassembly_entities, occupancy_bitmap, belt_bitmap, 2, 1, 0, 0)

create_belt_connection((30, 0), (30, 19), occupancy_bitmap, belt_bitmap)



# display
print(f"+{'-'*bitmap_shape[1]}+")
for y in range(bitmap_shape[0]):
    print("|", end="")
    for x in range(bitmap_shape[1]):
        occupancy = occupancy_bitmap[y, x]
        belt = belt_bitmap[y, x]
        if occupancy:
            if belt:
                print(end="▓") # conflict error
            else:
                print(end=str(occupancy))
        elif belt:
            if belt & (0b1111) << 4:
                print(end="X") # underground
            else:
                print(end="↑→↓←"[int(np.log2(belt))])
        else:
            print(end=" ")
    print("|")
print(f"+{'-'*bitmap_shape[1]}+")


