import math
import numpy as np


import pygame


obstacles = [
    # CENTERED #
    # x, y, w, h
    (3.5, 3.5, 3.0, 3.0),
    (5.0, 8.0, 2.0, 2.0),
]
# get_obstacle_bounding_box = lambda xywh_centered: return


class PositionalGraphNode:
    def __init__(self, x:float, y:float) -> None:
        self.x = x
        self.y = y
        # self.parent = None
        # self.f = 0.0
        # self.g = 0.0
        # self.h = 0.0
        self.connections = set()

routing_graph_nodes = set()

def get_graph_links(graph_nodes):
    links = set()
    for a in graph_nodes:
        for b in a.connections:
            assert a in b.connections
            if id(a) < id(b):
                links.add((a, b,))
            else:
                links.add((b, a,))
    return links

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

    a.connections.add(c)
    c.connections.add(a)

    d.connections.add(b)
    b.connections.add(d)

    d.connections.add(c)
    c.connections.add(d)

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

        for (a, b) in get_graph_links(routing_graph_nodes):
            pygame.draw.aaline(screen, "red",
                screen_transform((a.x, a.y,)),
                screen_transform((b.x, b.y,)),
            True)

        # This MUST happen after all the other drawing commands.
        pygame.display.flip()

    # Be IDLE friendly
    pygame.quit()


