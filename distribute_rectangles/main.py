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
    
    def apply_to_canvas(self, canvas):
        # Map x to columns and y to rows
        canvas[self.y : self.y + self.prototype.height, self.x : self.x + self.prototype.width] = 0
        for proto_x, proto_y in self.prototype.outputs:
            canvas[self.y + proto_y, self.x + proto_x] = 0
        for proto_x, proto_y in self.prototype.inputs:
            canvas[self.y + proto_y, self.x + proto_x] = 0






subassembly_prototypes = {
    "foo": FactorioSubassemblyPrototype(6, 7, [[5, 6]], [[6, 0]])
}

subassembly_entities = []
subassembly_entities.append(FactorioSubassemblyEntity(subassembly_prototypes["foo"], x=10, y=10))
subassembly_entities.append(FactorioSubassemblyEntity(subassembly_prototypes["foo"], x=30, y=15))




canvas = np.ones((40, 100), dtype=bool)

for subassembly_entity in subassembly_entities:
    subassembly_entity.apply_to_canvas(canvas)



for i in range(1):
    # print(canvas)

    grid = Grid(matrix=canvas)

    # print(grid.grid_str())

    start = grid.node(0, 0)
    end = grid.node(8, 8)

    # print(start, end)

    finder = BiAStarFinder()

    # Calculate the path and number of runs
    path, runs = finder.find_path(start, end, grid)

    # Print the result
    # print("Path found:", path)
    print(grid.grid_str(path=path, start=start, end=end))

