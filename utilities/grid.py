import random
import pygame
import sys

white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
gray = (128, 128, 128)
gray2 = (155, 155, 155)
yellow = (255, 255, 0)

class Grid:
    def __init__(self, cell_size, dimension):
        self.size = cell_size
        self.row = dimension[0]
        self.col = dimension[1]
        self._directions = [(-2, 0),  # UP
                            (2, 0),  # DOWN
                            (0, -2),  # LEFT
                            (0, 2)]  # RIGHT
        self._solve_directions = [(0, -1),  # LEFT
                                  (0, 1),  # RIGHT
                                  (-1, 0),  # UP
                                  (1, 0)]  # DOWN
        self.start = (0, 0)
        self.end = (self.row - 2, self.col - 2)
        self.stack = []
        self.grid = []
        self._generate_grid()

    # Initialize the grid based on what the user chooses.
    def _generate_grid(self):
        for i in range(self.row):
            self.grid.append([])
            for j in range(self.col):
                self.grid[i].append("*")

    # Set start point and end point of the maze if necessary
    def set_start_end(self, screen):
        generator_visit = set()
        generator_visit.add(self.start)
        self.stack.append(self.start)
        self.depth_first_search(generator_visit, screen)
        print("Created maze successfully")
        self.solve_DFS()
        print("Solved maze successfully")
        self.print_grid()
        print("Set successfully!")

    def draw_maze(self, screen):
        color = None
        for i in range(len(self.grid)):
            row_length = len(self.grid[i])
            for j in range(row_length):
                if self.grid[i][j] == "s":
                    color = yellow
                elif self.grid[i][j] == "e":
                    color = red
                elif self.grid[i][j] == " ":
                    color = white
                elif self.grid[i][j] == "*":
                    color = gray2
                elif self.grid[i][j] == "p":
                    color = green
                new_cell = pygame.Rect(j * self.size, i * self.size, self.size,
                                       self.size)
                pygame.draw.rect(screen, color, new_cell)

    # Create the maze using depth_first_search
    def depth_first_search(self, visited, screen):
        while self.stack:
            current_pos = self.stack[-1]
            current_x, current_y = current_pos
            unvisited_neighbors = self._get_neighbors(current_pos, self._directions, "*", visited)
            # Try to draw on screen
            screen.fill((0, 0, 0))
            search_cell = pygame.Rect(current_y * self.size, current_x * self.size, self.size, self.size)
            pygame.draw.rect(screen, (207, 43, 251), search_cell)
            pygame.display.update()
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            if unvisited_neighbors:
                next_pos = random.choice(unvisited_neighbors)
                next_x, next_y = next_pos
                # Mark cell as new path
                self.grid[(current_x + next_x) // 2][(current_y + next_y) // 2] = " "
                self.grid[next_x][next_y] = " "
                visited.add(next_pos)
                self.stack.append(next_pos)
            else:
                self.stack.pop()

    # Solve the maze using DFS algorithm
    def solve_DFS(self):
        current_x, current_y = self.start
        stack = [(current_x, current_y)]
        visit_list = set()
        visit_list.add(self.start)
        while True:
            if not stack:
                print("Couldn't find a solution")
                return
            current_pos = stack[-1]
            if current_pos == self.end:
                break
            unvisited_neighbors = self._get_neighbors(current_pos, self._solve_directions, " ", visit_list)
            if unvisited_neighbors:
                next_pos = random.choice(unvisited_neighbors)
                if next_pos == self.end:
                    stack.append(next_pos)
                    break
                visit_list.add(next_pos)
                stack.append(next_pos)
            else:
                stack.pop()
        for coors in stack:
            self.grid[coors[0]][coors[1]] = "p"
        self.grid[self.start[0]][self.start[1]] = "s"
        self.grid[self.end[0]][self.end[1]] = "e"

    """def _breadth_first_search(self):
        while self.stack:
            current_pos = self.stack[0]
            current_x, current_y = current_pos
            unvisited_neighbors = self._get_neighbors(current_pos)
            if unvisited_neighbors:
                next_pos = random.choice(unvisited_neighbors)
                next_x, next_y = next_pos
                self.grid[(current_x+next_x)//2][(current_y+next_y)//2] = " "
                self.grid[next_x][next_y] = " "
                self.stack.append(next_pos)
            else:
                self.stack.pop(0)
        self.grid[self.end[0]][self.end[1]] = "e"""

    # Get the neighbors based on current position
    def _get_neighbors(self, start, directions, symbol, visited_list):
        current_x = start[0]
        current_y = start[1]
        neighbors = []
        for dir in directions:
            next_x = current_x + dir[0]
            next_y = current_y + dir[1]
            if 0 <= next_x < self.row and 0 <= next_y < self.col:
                if self.grid[next_x][next_y] == symbol and (next_x, next_y) not in visited_list:
                    neighbors.append((next_x, next_y))
        return neighbors

    # Print out grid to visualize
    def print_grid(self):
        for row in self.grid:
            print("".join(row))



