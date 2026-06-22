"""

AI generated via prompt:


use w9-pathfinding (python) to make an example where we path through a grid



two caveats:

- the cost between grid cells depends on the direction of travel

- the graph needs to be generated dynamically (not all at once, since it's an infinite space) according to external bitmaps representing grid data 




"""



import numpy as np

class InfiniteBitmapWorld:
    """Simulates an infinite world split into bitmap chunks/tiles."""
    def __init__(self, chunk_size=16):
        self.chunk_size = chunk_size
        self.loaded_chunks = {}

    def _generate_chunk(self, chunk_x, chunk_y):
        # In a real app, load an image file here. 
        # Here we mock it: 0 is open space, 1 is a wall obstacle.
        # Let's create a repeating pattern or random noise
        rng = np.random.default_rng(seed=(chunk_x ^ chunk_y))
        # 15% chance of obstacles
        return rng.choice([0, 1], size=(self.chunk_size, self.chunk_size), p=[0.85, 0.15])

    def get_cell_value(self, x, y):
        # Find which chunk this global coordinate belongs to
        chunk_x = x // self.chunk_size
        chunk_y = y // self.chunk_size
        
        # Local relative coordinate within the chunk
        local_x = x % self.chunk_size
        local_y = y % self.chunk_size
        
        chunk_key = (chunk_x, chunk_y)
        if chunk_key not in self.loaded_chunks:
            self.loaded_chunks[chunk_key] = self._generate_chunk(chunk_x, chunk_y)
            
        return self.loaded_chunks[chunk_key][local_y, local_x]
    


from w9_pathfinding.envs import Graph
from w9_pathfinding.pf import AStar  # or Dijkstra

def calculate_directional_cost(from_pos, to_pos):
    """
    Caveat 1: Cost depends on the direction of travel.
    Example Rule: Traveling East/North is easy (cost 1.0),
    Traveling West/South is uphill/harder (cost 2.5).
    """
    dx = to_pos[0] - from_pos[0]
    dy = to_pos[1] - from_pos[1]
    
    if dx > 0: return 1.0   # Moving East
    if dx < 0: return 2.5   # Moving West
    if dy > 0: return 1.0   # Moving North
    if dy < 0: return 2.5   # Moving South
    return 1.0

def generate_local_graph(world, start, goal, padding=10):
    """
    Caveat 2: Graph generated dynamically according to external bitmaps.
    Only instantiates the bounding box region needed between start and goal.
    """
    graph = Graph()
    
    # Define bounding box for the path request
    min_x = min(start[0], goal[0]) - padding
    max_x = max(start[0], goal[0]) + padding
    min_y = min(start[1], goal[1]) - padding
    max_y = max(start[1], goal[1]) + padding
    
    # Step 1: Add traversable nodes dynamically based on bitmap
    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            # Check bitmap: if it's 0 (passable), add node to graph
            if world.get_cell_value(x, y) == 0:
                graph.add_node((x, y))
                
    # Step 2: Establish directed edges with asymmetric directional weights
    # 4-connected grid neighbors (can extend to 8-connected if required)
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    
    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            current = (x, y)
            if not graph.has_node(current):
                continue
                
            for dx, dy in directions:
                neighbor = (x + dx, y + dy)
                if graph.has_node(neighbor):
                    # Calculate cost purely based on direction vector
                    weight = calculate_directional_cost(current, neighbor)
                    # Add directed edge (from -> to)
                    graph.add_edge(current, neighbor, weight=weight)
                    
    return graph



def main():
    # Instantiate our endless map generator
    world = InfiniteBitmapWorld(chunk_size=16)
    
    # Pick a start and goal deep inside the coordinate space
    start_pos = (5, 5)
    goal_pos = (25, 22)
    
    print(f"Generating dynamic graph from bitmaps for {start_pos} -> {goal_pos}...")
    local_graph = generate_local_graph(world, start_pos, goal_pos, padding=5)
    
    # Ensure start and goal aren't spawned inside walls
    if not local_graph.has_node(start_pos) or not local_graph.has_node(goal_pos):
        print("Oops! Start or Goal landed on an unpassable bitmap obstacle. Retrying...")
        return

    # Initialize the pathfinder with our custom-built Graph environment
    finder = AStar(local_graph)
    
    print("Computing optimal path...")
    path = finder.find_path(start_pos, goal_pos)
    
    if path:
        print(f"\nSuccess! Path found with {len(path)} steps.")
        print("Path coordinates:")
        print(path)
    else:
        print("\nNo path could be found between those locations given the obstacles.")

if __name__ == "__main__":
    main()