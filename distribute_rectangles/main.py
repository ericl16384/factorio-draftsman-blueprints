# from pathfinding.core.grid import Grid
# from pathfinding.finder.bi_a_star import BiAStarFinder

import numpy as np

import belt_pathfinding




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

subassembly_entities = []
subassembly_entities.append(FactorioSubassemblyEntity(subassembly_prototypes["foo"], x=10, y=3))
subassembly_entities.append(FactorioSubassemblyEntity(subassembly_prototypes["foo"], x=30, y=7))



bitmap_size         = (20, 100)
occupancy_bitmap    = np.zeros(bitmap_size, dtype=int)
belt_bitmap         = np.zeros(bitmap_size, dtype=int)

for subassembly_entity in subassembly_entities:
    subassembly_entity.apply_to_occupany_bitmap(occupancy_bitmap)





requester = subassembly_entities[0]
provider = subassembly_entities[1]
start = (requester.x + requester.prototype.outputs[0][0], requester.y + requester.prototype.outputs[0][1])
end = (provider.x + provider.prototype.inputs[0][0], provider.y + provider.prototype.inputs[0][1])





# occupancy bitmap
print(f"+{'-'*bitmap_size[1]}+")
for y in range(bitmap_size[0]):
    print("|", end="")
    for x in range(bitmap_size[1]):
        if occupancy_bitmap[y, x]:
            print(occupancy_bitmap[y, x], end="")
        else:
            print(end=" ")
    print("|")
print(f"+{'-'*bitmap_size[1]}+")

# belt bitmap
print(f"+{'-'*bitmap_size[1]}+")
for y in range(bitmap_size[0]):
    print("|", end="")
    for x in range(bitmap_size[1]):
        if (belt_bitmap[y, x] & 0b1111):
            print((belt_bitmap[y, x] & 0b1111), end="")
        else:
            print(end=" ")
    print("|")
print(f"+{'-'*bitmap_size[1]}+")


