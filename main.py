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

#know how to draw itself
#keep track of all its neighbours
#know it's function by its color
#keep track of the coordinate
class Node:
    def __init__(self, row, column, width, total_rows):
        self.row = row
        self.column = column
        self.x = row * width
        self.y = column * width
        self.neighbours = []
        self.width = width
        self.colour = BABY_BLUE
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
        return self.colour == PASTEL_PINK

    def is_end(self):
        return self.colour == PASTEL_GREEN

    def reset(self):
        self.colour = BABY_BLUE

    def create_start_node(self):
        self.colour = PASTEL_PURPLE
    def create_open_node(self):
        self.colour = YELLOW
    def create_barrier(self):
        self.colour = PASTEL_PINK
    def create_close_node(self):
        self.colour = PASTEL_ORANGE
    def create_end_node(self):
        self.colour = PASTEL_GREEN
    def create_path(self):
        self.colour = LIGHT_BROWN

    def draw(self, win):
        pygame.draw.rect(win, self.colour, (self.x, self.y, self.width, self.width))

    def update_neighbours(self, grid):
        pass

    def __lt__(self, other):
        return False


def manhattan_distance(node_1, node_2):
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


def main(win, width):
    ROWS = 70
    grid = create_grid(ROWS, width)

    start = None
    end = None

    run = True
    started = False
    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get(): #loop through every event in pygame
            if event.type == pygame.QUIT:
                run = False

            if started:
                continue

            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = get_click_position(pos, ROWS, width)
                node = grid[row][col]
                if not start:
                    start = node
                    start.create_start_node()

                elif not end:
                    end = node
                    end.create_end_node()

                elif node != end and node != start:
                    node.create_barrier()



            elif pygame.mouse.get_pressed()[2]:
                pass



    pygame.quit()

main(WIN, WIDTH)