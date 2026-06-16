from pathfinding.core.grid import Grid
from pathfinding.finder.bi_a_star import BiAStarFinder

import numpy as np




class FactorioSubassemblyPrototype:
    def __init__(self, width, height, inputs, outputs) -> None:
        self.width = width
        self.height = height
        self.inputs = inputs
        self.outputs = outputs

class FactorioSubassemblyEntity:
    def __init__(self, prototype, x, y) -> None:
        self.prototype = prototype
        self.x = x
        self.y = y
    
    def apply_to_canvas(self, collision_canvas):
        # Map x to columns and y to rows
        collision_canvas[self.y : self.y + self.prototype.height, self.x : self.x + self.prototype.width] = 0
        for proto_x, proto_y in self.prototype.outputs:
            collision_canvas[self.y + proto_y, self.x + proto_x] = 0
        for proto_x, proto_y in self.prototype.inputs:
            collision_canvas[self.y + proto_y, self.x + proto_x] = 0






subassembly_prototypes = {
    "foo": FactorioSubassemblyPrototype(6, 7, [[5, 6]], [[6, 0]])
}

subassembly_entities = []
subassembly_entities.append(FactorioSubassemblyEntity(subassembly_prototypes["foo"], x=10, y=3))
subassembly_entities.append(FactorioSubassemblyEntity(subassembly_prototypes["foo"], x=30, y=7))



canvas_size = (20, 100)
collision_canvas = np.ones(canvas_size, dtype=bool)
belt_canvas = np.zeros(canvas_size, dtype=int)

BELT_TO_NORTH   = 0b00000001
BELT_TO_EAST    = 0b00000010
BELT_TO_SOUTH   = 0b00000100
BELT_TO_WEST    = 0b00001000
BELT_FROM_NORTH = 0b00010000
BELT_FROM_EAST  = 0b00100000
BELT_FROM_SOUTH = 0b01000000
BELT_FROM_WEST  = 0b10000000


for subassembly_entity in subassembly_entities:
    subassembly_entity.apply_to_canvas(collision_canvas)



def find_belt_path(collision_canvas, start, end):
    return BiAStarFinder().find_path(grid.node(*start), grid.node(*end), Grid(collision_canvas))

def apply_belt_path(collision_canvas, belt_canvas, path):
    for i in range(len(path)-1):

        b = 0
        if path[i].y > path[i+1].y:
            b &= BELT_TO_NORTH
        if path[i].x < path[i+1].x:
            b &= BELT_TO_EAST
        if path[i].y < path[i+1].y:
            b &= BELT_TO_SOUTH
        if path[i].x > path[i+1].x:
            b &= BELT_TO_WEST
            
        assert belt_canvas[path[i].y, path[i].x] & 0b00001111 == 0
        belt_canvas[path[i].y, path[i].x]        &= b
        belt_canvas[path[i+1].y, path[i+1].x]    &= b<<4

        



# print(collision_canvas)

grid = Grid(matrix=collision_canvas)

# print(grid.grid_str())

requester = subassembly_entities[0]
provider = subassembly_entities[1]
start = grid.node(requester.x + requester.prototype.outputs[0][0], requester.y + requester.prototype.outputs[0][1])
end = grid.node(provider.x + provider.prototype.inputs[0][0], provider.y + provider.prototype.inputs[0][1])

# requester = subassembly_entities[1]
# provider = subassembly_entities[0]
# start = grid.node(requester.x + requester.prototype.outputs[0][0], requester.y + requester.prototype.outputs[0][1])
# end = grid.node(provider.x + provider.prototype.inputs[0][0], provider.y + provider.prototype.inputs[0][1])

# print(start, end)

finder = BiAStarFinder()

# Calculate the path and number of runs
path, runs = finder.find_path(start, end, grid)


print(Grid(matrix=belt_canvas).grid_str())

# Print the result
# print("Path found:", path)
print(grid.grid_str(path=path, start=start, end=end))

