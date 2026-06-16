from pathfinding.core.grid import Grid
from pathfinding.finder.bi_a_star import BiAStarFinder

import numpy as np




class FactorioSubassembly:
    def __init__(self, width, height, inputs, outputs) -> None:
        self.width = width
        self.height = height
        self.inputs = inputs
        self.outputs = outputs
    
    def apply_to_canvas(self, canvas, x, y):
        # Map x to columns and y to rows
        canvas[y : y + self.height, x : x + self.width] = 0
        for x, y in self.outputs:
            canvas[y, x] = 0
        for x, y in self.inputs:
            canvas[y, x] = 0


subassemblies = {
    "foo": FactorioSubassembly(6, 7, [[5, 6]], [[6, 0]])
}



# Format: [x, y, width, height]
rectangles = [
    [1, 1, 3, 2],  # Rect 1: Starts at (1,1), width 3, height 2
    [5, 4, 4, 5],  # Rect 2: Starts at (5,4), width 4, height 5
]




canvas = np.ones((40, 100), dtype=bool)


for x, y, width, height in rectangles:
    # Map x to columns and y to rows
    canvas[y : y + height, x : x + width] = 0







canvas[0, 9] = 0
canvas[1, 8] = 0

canvas[0, 0] = 0
canvas[9, 9] = 0

# print(canvas)

grid = Grid(matrix=canvas)

# print(grid.grid_str())

start = grid.node(0, 0)
end = grid.node(9, 9)

# print(start, end)

finder = BiAStarFinder()

# Calculate the path and number of runs
path, runs = finder.find_path(start, end, grid)

# Print the result
# print("Path found:", path)
print(grid.grid_str(path=path, start=start, end=end))

