import math
import numpy as np


import pygame
import random






class PositionalGraphNode:
    def __init__(self, x:float, y:float) -> None:
        self.x = x
        self.y = y
        # self.parent = None
        # self.f = 0.0
        # self.g = 0.0
        # self.h = 0.0
        self.connections = set()

class GraphLink:
    def __init__(self) -> None:
        self.link_name = None

        self.valid = True

    __links = {}
    
    @classmethod
    def get_registered_link(cls, a, b):
        if id(a) < id(b):
            link_name = (a, b,)
        else:
            link_name = (b, a,)

        if link_name not in cls.__links:
            link = GraphLink()
            link.link_name = link_name
            cls.__links[link_name] = link

        return cls.__links[link_name]


def new_link(a, b):
    if id(a) < id(b):
        return (a, b,)
    else:
        return (b, a,)

def get_graph_links(graph_nodes):
    links = set()
    for a in graph_nodes:
        for b in a.connections:
            assert a in b.connections
            links.add(new_link(a, b,))
    return links



# def get_line_intersect(p1, p2, p3, p4):
#     """ 
#     Credit google search

#     Finds the intersection of two lines defined by points:
#     Line 1: (p1, p2)
#     Line 2: (p3, p4)
#     """
#     # Create vectors
#     r = np.subtract(p2, p1)
#     s = np.subtract(p4, p3)
    
#     # Check if lines are parallel (denominator is zero)
#     denom = np.cross(r, s)
#     print(denom)
#     print(np.linalg.det((r, s)))
#     assert denom == np.linalg.det((r, s))
#     input()
#     if denom == 0:
#         return None  # Parallel lines
    
#     # Solve for t in: p1 + t*r = p3 + u*s
#     # Using the formula: t = (q - p) x s / (r x s)
#     t = np.cross(np.subtract(p3, p1), s) / denom
    
#     # Calculate intersection point
#     return np.add(p1, np.multiply(t, r))

def raycast_ab(a:PositionalGraphNode, b:PositionalGraphNode, colliding_edges, tolerance=1e-10):
    ray_vec = np.subtract((b.x, b.y), (a.x, a.y))

    intersections = set()
    
    for edge in colliding_edges:
        edge_vec = np.subtract((edge[1].x, edge[1].y), (edge[0].x, edge[0].y))
        
        denom = np.linalg.det((ray_vec, edge_vec))
        if abs(denom) < tolerance: continue

        t = np.cross(np.subtract((edge[0].x, edge[0].y), (a.x, a.y)), edge_vec) / denom
        # print(t)

        if t > tolerance and t < 1-tolerance:
            intersections.add(tuple(np.add((a.x, a.y), np.multiply(ray_vec, t))))

            # print(t)

    return intersections


obstacles = [
    # CENTERED #
    # x, y, w, h
    # (3.5, 3.5, 3.0, 3.0),
    # (5.0, 8.0, 2.0, 2.0),
]
# get_obstacle_bounding_box = lambda xywh_centered: return

for x in range(10):
    for y in range(10):
        if random.random() < 0.9: continue

        obstacles.append((x+0.5, y+0.5, 0.8, 0.8))


routing_graph_nodes = set()

colliding_edges = set()

routing_links = set()
blocked_links = set()


# row col map (following factorio's y is down and x is right)
# traverse_map = np.zeros((16, 16), int)

# This brute force would be better as obstacles making their own traverse map and ORing it
for obstacle in obstacles:
    (x, y, w, h) = obstacle
    
    x_min = math.floor(x - w/2)
    y_min = math.floor(y - h/2)

    x_max = math.ceil(x + w/2)
    y_max = math.ceil(y + h/2)

    a = PositionalGraphNode(x_min, y_min)
    b = PositionalGraphNode(x_min, y_max)
    c = PositionalGraphNode(x_max, y_min)
    d = PositionalGraphNode(x_max, y_max)

    a.connections.add(b)
    b.connections.add(a)
    colliding_edges.add(new_link(a, b))

    a.connections.add(c)
    c.connections.add(a)
    colliding_edges.add(new_link(a, c))

    d.connections.add(b)
    b.connections.add(d)
    colliding_edges.add(new_link(d, b))

    d.connections.add(c)
    c.connections.add(d)
    colliding_edges.add(new_link(d, c))

    routing_graph_nodes.add(a)
    routing_graph_nodes.add(b)
    routing_graph_nodes.add(c)
    routing_graph_nodes.add(d)

    # for y in range(y_min, y_max+1):
    #     for x in range(x_min, x_max+1):
    #         # print((x, y))
    #         # input()
    #         # traverse_map[x, y] = 1

    #         # print(traverse_map)




for edge in colliding_edges:
    routing_links.add(edge)
for a in routing_graph_nodes:
    for b in routing_graph_nodes:
        if a == b: continue

        link = new_link(a, b)

        if link in colliding_edges: continue

        if raycast_ab(a, b, colliding_edges): continue

        routing_links.add(link)




class Pathfinding:
    class Node:
        def __init__(self) -> None:
            self.x = 0.0
            self.y = 0.0
            self.parent = None
            self.f = 0.0
            self.g = 0.0
            self.h = 0.0

    def __init__(self, start_xy, goal_xy) -> None:
        self.open_set = set()
        self.closed_set = set()

        self.start_xy = np.array(start_xy, dtype=int)
        self.goal_xy = np.array(goal_xy, dtype=int)

        self.solution_node = None

        self.explore_node(self.start_xy, None, None)
    
    def explore_node(self, xy, parent, g_increment):
        if parent == None:
            g = 0
        else:
            g = parent.g + g_increment

        h_manhattan = float(self.manhattan_heuristic(xy))

        f = g + h_manhattan

        q = self.Node()
        q.x = x
        q.y = y
        q.parent = parent
        q.f = f
        q.g = g
        q.h = h_manhattan

        self.open_set.add(q)

        # check if this the solution node
        if h_manhattan == 0:
            self.solution_node = q
    
    def manhattan_heuristic(self, xy):
        return np.linalg.norm(self.goal_xy - xy, ord=1)

    def do_next(self):
        min_h = np.inf
        q = None
        for node in self.open_set:
            if node.h < min_h:
                min_h = node.h
                q = node
        
        if q is None:
            raise StopIteration
        
        self.open_set.remove(q)

        # add successors
        for rel_offset in (
            (0, 1,),
            (1, 0,),
            (0, -1),
            (-1, 0,)
        ):
            self.explore_node(np.add((node.x, node.y), rel_offset), q, 1)
        
            # todo skip if successor already exists in open or closed lists
        



pathfinding = Pathfinding((0, 0), (5, 5))





if __name__ == "__main__":
      
      

    import pygame

    # Initialize pygame
    pygame.init()

    # Set the height and width of the screen
    size = [800, 600]
    screen = pygame.display.set_mode(size)

    screen_transform = lambda xy: tuple(np.array(xy)*(250, -250) + np.array(size)/2)

    # pygame.display.set_caption("Example code for the draw module")

    # Loop until the user clicks the close button.
    done = False
    clock = pygame.time.Clock()

    while not done:
        # This limits the while loop to a max of 60 times per second.
        # Leave this out and we will use all CPU we can.
        clock.tick(60)

        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT:  # If user clicked close
                done = True  # Flag that we are done so we exit this loop

        pressed_keys = pygame.key.get_pressed()

        screen.fill("black")


        screen_scaling = lambda xy: np.multiply(xy, 30)
        screen_transform = lambda xy: [ int(i) for i in screen_scaling(xy)+50 ]

        # draw a nice grid
        # for 

        for obstacle in obstacles:
            (x, y, w, h) = obstacle

            # w -= 0.2
            # h -= 0.2

            pygame.draw.rect(screen, "grey", (
                # (left top width height)

                screen_transform(( x - w/2, y - h/2, )),
                screen_scaling(( w, h, )),

                # x_min = math.floor(x - w/2)
                # y_min = math.floor(y - h/2)

                # x_max = math.ceil(x + w/2)
                # y_max = math.ceil(y + h/2)
            ))

        # for (row, col), value in np.ndenumerate(traverse_map):
        #     if value:
        #         pygame.draw.circle(screen, "red",
        #             screen_transform((row, col)),
        #             screen_scaling(0.05),
        #         )
        #     else:
        #         pygame.draw.circle(screen, "dark grey",
        #             screen_transform((row, col)),
        #             screen_scaling(0.05),
        #         )

        for node in routing_graph_nodes:
            pygame.draw.circle(screen, "white",
                screen_transform((node.x, node.y)),
                screen_scaling(0.10),
            )

        for (a, b) in colliding_edges:
            pygame.draw.aaline(screen, "red",
                screen_transform((a.x, a.y,)),
                screen_transform((b.x, b.y,)),
            True)

        for (a, b) in routing_links:
            pygame.draw.aaline(screen, "green",
                screen_transform((a.x, a.y,)),
                screen_transform((b.x, b.y,)),
            True)



        # ray_a = PositionalGraphNode(3.5, 3.5)
        # ray_b = PositionalGraphNode(5.0, 8.0)
        # for vec in raycast_ab(ray_a, ray_b, colliding_links):
        #     pygame.draw.aaline(screen, "green",
        #         screen_transform((ray_a.x, ray_a.y,)),
        #         screen_transform(vec),
        #     True)
        #     pygame.draw.circle(screen, "red",
        #         screen_transform(vec),
        #         screen_scaling(0.15),
        #     )
            



        # This MUST happen after all the other drawing commands.
        pygame.display.flip()

    # Be IDLE friendly
    pygame.quit()


