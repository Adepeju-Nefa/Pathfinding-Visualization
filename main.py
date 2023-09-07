import pygame

import math
from queue import PriorityQueue


WIDTH = 800
WIN = pygame.display.set_mode((WIDTH,WIDTH))
pygame.display.set_caption("My A* PathFinding Visualizer")

PASTEL_PINK = (255, 186, 205)
PASTEL_PURPLE = (197, 179, 247)
YELLOW = (255, 255, 0) #open
BABY_BLUE = (173, 216, 230) #background
PASTEL_ORANGE = (255, 179, 71) #closed
PASTEL_GREEN = (173, 255, 153)
LIGHT_BROWN = (205, 133, 63)
GREY = (128, 128, 128)

# know how to draw itself
# keep track of all its neighbours
# know it's function by its color
# keep track of the coordinate
class Node:
    def __init__(self, row, column, width, total_rows):
        self.row = row
        self.column = column
        self.x = row * width
        self.y = column * width
        self.neighbours = []
        self.width = width
        self.colour = PASTEL_PINK
        self.total_rows = total_rows

    def get_position(self):
        return self.row, self.column

    def is_closed(self):
        return self.colour == PASTEL_ORANGE

    def is_open(self):
        return self.colour == YELLOW

    def is_start(self):
        return self.colour == PASTEL_PURPLE

    def is_barrier(self):
        return self.colour == BABY_BLUE

    def is_end(self):
        return self.colour == PASTEL_GREEN

    def reset(self):
        self.colour = PASTEL_PINK

    def create_start_node(self):
        self.colour = PASTEL_PURPLE

    def create_open_node(self):
        self.colour = YELLOW

    def create_barrier(self):
        self.colour = BABY_BLUE

    def create_close_node(self):
        self.colour = PASTEL_ORANGE

    def create_end_node(self):
        self.colour = PASTEL_GREEN

    def create_path(self):
        self.colour = LIGHT_BROWN

    def draw(self, win):
        pygame.draw.rect(win, self.colour, (self.x, self.y, self.width, self.width))

    # update a list of neighbouring node for the given node grid
    def update_neighbours(self, grid):
        self.neighbours = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.column].is_barrier(): # check if  there is a barrier down
            self.neighbours.append(grid[self.row + 1][self.column]) # append to neighbour if no barrier is found

        if self.row > 0 and not grid[self.row - 1][self.column].is_barrier(): # check if there is a barrier up
            self.neighbours.append(grid[self.row - 1][self.column])

        if self.column < self.total_rows - 1 and not grid[self.row][self.column + 1].is_barrier(): # check right
            self.neighbours.append(grid[self.row][self.column + 1])

        if self.column > 0 and not grid[self.row][self.column - 1].is_barrier(): # check left
            self.neighbours.append(grid[self.row][self.column - 1])

    def __lt__(self, other):
        return False

#heuristics
def h(node_1, node_2):
        x1, y1 = node_1
        x2, y2 = node_2
        dist = abs(x2 - x1) + (y2 - y1)
        return dist


def create_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Node(i, j, gap, rows)
            grid[i].append(spot)

    return grid

# draw grid lines
# calculate the gap in each node,
# for every row iteratively draw a horizontal line, starts at position 0 and i * gap


def draw_grid_lines(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, (i * gap)), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))


def draw(win, grid, rows, width):
    win.fill(BABY_BLUE)

    for row in grid:
        for spot in row:
            spot.draw(win)

    draw_grid_lines(win, rows, width)
    pygame.display.update()


def get_click_position(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap

    return row, col


def construct_path(came_from, current, draw):

    while current in came_from:
        current = came_from[current]
        current.create_path()

        draw()


def alg( draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start)) # put start node in open set
    came_from = {} # dictionary containing nodes we've traversed

    # initialize the g, f and h scores at the start as 0
    g = {node: float("inf") for row in grid for node in row} # current shortest distance to get from start node to current node
    g[start] = 0

    f = {node: float("inf") for row in grid for node in row}
    f[start] = h(start.get_position(), end.get_position()) # initialize it to the heuristics of start to end distance

    # keep track of items in the priorityqueue, stores the same thing in the queue
    open_set_hash = {start}

    while not open_set.empty():
        # allow user to quit simulation even when started
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        # get minimum f score's node
        current = open_set.get()[2]
        open_set_hash.remove(current)

        # path found
        if current == end:
            construct_path(came_from, end, draw)
            end.create_end_node()
            return True

        # else calculate the g score for the neighbours
        # check if the neighbour is a barrier
        for neighbour in current.neighbours:
            if not neighbour.is_barrier():
                temp_g = g[current] + 1

            # if a smaller g score is found then there is a better path
            # update the came from list to include the current node
            # update g score and f score
            if temp_g < g[neighbour]:
                came_from[neighbour] = current
                g[neighbour] = temp_g
                f[neighbour] = temp_g + h(neighbour.get_position(), end.get_position())
                if neighbour not in open_set_hash:
                    count += 1
                    open_set.put((f[neighbour], count, neighbour))
                    open_set_hash.add(neighbour)
                    neighbour.create_open_node()

        draw()

        if current != start:
            current.create_close_node()


    return False


def main(win, width):

    ROWS = 50
    grid = create_grid(ROWS, width)

    start = None
    end = None

    run = True
    started = False
    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():  # loop through every event in pygame
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]: # if left button gets pressed
                pos = pygame.mouse.get_pos() # find the position of the mouse
                row, col = get_click_position(pos, ROWS, width)
                node = grid[row][col]
                if not start and node != end:
                    start = node
                    start.create_start_node()

                elif not end and node != start:
                    end = node
                    end.create_end_node()

                elif node != end and node != start:
                    node.create_barrier()

            elif pygame.mouse.get_pressed()[2]: # right click
                pos = pygame.mouse.get_pos()  # find the position of the mouse
                row, col = get_click_position(pos, ROWS, width)
                node = grid[row][col]
                node.reset()
                if node == start:
                    start = None
                elif node == end:
                    end = None
                # elif node != end and node != start:
                #     node.reset()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for node in row:
                            node.update_neighbours(grid)
                    alg(lambda: draw(win, grid, ROWS, width), grid, start, end)

                if event.key == pygame.K_c: # clear the screen if 'c' is pressed
                    start = None
                    end = None
                    grid = create_grid(ROWS, width)

    pygame.quit()


main(WIN, WIDTH)