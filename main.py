import pygame
import math
from queue import PriorityQueue
from collections import deque


GREEN = (34, 164, 86)  # for searched space
BLUE = (184, 45, 32)  # for looking nodes
RED = (255, 0, 0)  # for path
PINK = (182, 76, 155)  # for starting node
YELLOW = (244, 187, 67)  # for ending node
LITE_GRAY = (39, 53, 68)  # for empty space
DARKER_GRAY = (87, 87, 87)  # for walls
BLACK = (0, 0, 0)  # for edges
WHITE = (244, 244, 244)  # for grid lines
GREY = (128, 128, 128)
PURPLE = (128, 0, 128)

WIDTH = 800
HEIGHT = 600

states = {RED: 'explored', GREEN: 'open', BLACK: 'barrier', BLUE: 'start', PINK: 'end', PURPLE:'path'}


class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.width = width
        self.color = WHITE
        self.neighbors = []
        self.total_rows = total_rows
        self.pos_pixel_x = self.col * width
        self.pos_pixel_y = self.row * width

    def get_pos(self):
        return self.row, self.col

    def get_state(self) -> str:
        value = states[self.color]
        return value

    def reset(self):
        self.color = WHITE

    def change_state(self, state: str) -> None:
        value = [i for i in states if states[i] == state]
        if value:
            self.color = value[0]

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.pos_pixel_x, self.pos_pixel_y, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and grid[self.row + 1][self.col].color != BLACK:  # Down
            self.neighbors.append(grid[self.row + 1][self.col])
        if self.row > 0 and grid[self.row - 1][self.col].color != BLACK:  # Up
            self.neighbors.append(grid[self.row - 1][self.col])
        if self.col < self.total_rows - 1 and grid[self.row][self.col + 1].color != BLACK:  # Right
            self.neighbors.append(grid[self.row][self.col + 1])
        if self.col > 0 and grid[self.row][self.col - 1].color != BLACK:  # Left
            self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self, other):
        return False


def h(p1, p2):
    return abs(p2[0] - p1[0]) + abs(p2[1] - p1[1])


def reconstruct_path(came_from, current,start, draw):
    path = []
    while current in came_from:
        current = came_from[current]
        if current != start:
            current.change_state('path')
        path.append(current.get_pos())
        draw()
    path.reverse()
    path_length = len(path)
    print(f"Path\n")
    for elem in path:
        print(elem)
    print(f"Path Length: {path_length}")


def astar(draw, grid, start, end):
    priority = 0
    open_set = PriorityQueue()
    open_set.put((0, priority, start))
    came_from = {}

    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0
    f_score = {node: float("inf") for row in grid for node in row}
    f_score[start] = h(start.get_pos(), end.get_pos())

    inQueue = {start}

    while not open_set.empty():

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit() #check for an event

        current = open_set.get()[2]
        inQueue.remove(current)

        if current == end:
            reconstruct_path(came_from, end, start, draw)
            end.change_state('end')
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                if neighbor not in inQueue:
                    priority += 1
                    open_set.put((f_score[neighbor], priority, neighbor))
                    inQueue.add(neighbor)
                    neighbor.change_state('open')
        draw()
        if(current != start):
            current.change_state('explored')
    return False


def bfs(draw, grid, start, end):
    queue = deque([start])
    came_from = {}
    visited = {start}

    while queue:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = queue.popleft()

        if current == end:
            reconstruct_path(came_from, end, start, draw)
            end.change_state('end')
            return True

        for neighbor in current.neighbors:
            if neighbor not in visited:
                came_from[neighbor] = current
                visited.add(neighbor)
                queue.append(neighbor)
                neighbor.change_state('open')

        draw()
        if current != start:
            current.change_state('explored')

    return False

def dfs(draw, grid, start, end):
    queue = deque([start])
    came_from = {}
    visited = {start}

    while queue:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = queue.pop()

        if current == end:
            reconstruct_path(came_from, end, start, draw)
            end.change_state('end')
            return True

        for neighbor in current.neighbors:
            if neighbor not in visited:
                came_from[neighbor] = current
                visited.add(neighbor)
                queue.append(neighbor)
                neighbor.change_state('open')

        draw()
        if current != start:
            current.change_state('explored')

    return False

def dijkstra(draw, grid, start, end):
    priority = 0
    open_set = PriorityQueue()
    open_set.put((0, priority, start))
    came_from = {}

    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0

    inQueue = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        inQueue.remove(current)

        if current == end:
            reconstruct_path(came_from, end, start, draw)
            end.change_state('end')
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                if neighbor not in inQueue:
                    priority += 1
                    open_set.put((g_score[neighbor], priority, neighbor))
                    inQueue.add(neighbor)
                    neighbor.change_state('open')
        draw()
        if current != start:
            current.change_state('explored')
    return False


def UCS(draw, grid, start, end):
    priority = 0
    open_set = PriorityQueue()
    open_set.put((0, priority, start))
    came_from = {}

    visited = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        g_score_current, _, current = open_set.get()

        if current == end:
            reconstruct_path(came_from, end, start, draw)
            end.change_state('end')
            return True

        # Explore neighbors
        for neighbor in current.neighbors:
            if neighbor not in visited:
                priority += 1
                came_from[neighbor] = current
                new_cost = g_score_current + 1
                open_set.put((new_cost, priority, neighbor))
                visited.add(neighbor)
                neighbor.change_state('open')

        draw()
        if current != start:
            current.change_state('explored')

    return False


def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, rows)
            grid[i].append(node)
    return grid


def draw_grid_lines(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))


def draw(win, grid, rows, width):
    win.fill(WHITE)

    for row in grid:
        for node in row:
            node.draw(win)
    draw_grid_lines(win, rows, width)
    pygame.display.update()


def get_clicked_node_index(pos, rows, width):
    gap = width // rows
    x, y = pos
    row = y // gap
    col = x // gap

    return row, col


def main(win, width):
    ROWS = 50
    grid = make_grid(ROWS, width)

    start = None
    end = None

    run = True
    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]:  # LEFT
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_node_index(pos, ROWS, width)
                spot = grid[row][col]
                if not start and spot != end:
                    start = spot
                    print(f"Start spot set at {start.get_pos()}")
                    start.change_state('start')

                elif not end and spot != start:
                    end = spot
                    print(f"End spot set at {end.get_pos()}")
                    end.change_state('end')

                elif spot != end and spot != start:
                    spot.change_state('barrier')

            elif pygame.mouse.get_pressed()[2]:  # RIGHT
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_node_index(pos, ROWS, width)
                spot = grid[row][col]
                spot.reset()
                if spot == start:
                    start = None
                elif spot == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)

                    astar(lambda: draw(win, grid, ROWS, width), grid, start, end)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and start and end:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)

                    bfs(lambda: draw(win, grid, ROWS, width), grid, start, end)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RCTRL and start and end:
                        for row in grid:
                            for spot in row:
                                spot.update_neighbors(grid)

                        dfs(lambda: draw(win, grid, ROWS, width), grid, start, end)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT and start and end:
                        for row in grid:
                            for spot in row:
                                spot.update_neighbors(grid)

                        dijkstra(lambda: draw(win, grid, ROWS, width), grid, start, end)

                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)

    pygame.quit()


if __name__ == '__main__':
    window = pygame.display.set_mode(size=(WIDTH, HEIGHT))
    main(window, WIDTH)