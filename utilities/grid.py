import random
import pygame
import sys
from collections import deque
from .cell import Cell

def event_handler():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()

# Make steps taken to find the solution
white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
gray = (128, 128, 128)
gray2 = (155, 155, 155)
yellow = (255, 255, 0)
orange = (245, 127, 0)
purple = (207, 43, 251)

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
        self._frontier = []
        self._in = set()
        self._grid_cell = {}
        for i in range(self.row):
            for j in range(self.col):
                self._grid_cell[(i, j)] = Cell((i, j), self.end)
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
        screen.fill(black)
        self.draw_maze(screen)
        print("Drawn maze successfully")
        #self.depth_first_search(generator_visit, screen)
        self.prim_algorithm(screen)
        print("Created maze successfully")
        self.solve_DFS(screen)
        #self.solve_BFS(screen)
        #self.solve_RHR(screen)
        print("Solved maze successfully")
        #self.print_grid()
        print("Set successfully!")

    def blit_distance(self, screen):
        for position, cell in self._grid_cell.items():
            symbol = self.grid[position[0]][position[1]]
            if symbol != "*":
                cell.draw_distance(screen, self.size)

    def draw_cell(self, screen, i, j, color):
        cell = pygame.Rect(j * self.size, i * self.size, self.size, self.size)
        pygame.draw.rect(screen, color, cell)
        return cell

    def draw_maze(self, screen):
        match_color_symbol = {"s":yellow, "e": red, " ": white, "*": black, "p": green}
        for i in range(len(self.grid)):
            row_length = len(self.grid[i])
            for j in range(row_length):
                color = match_color_symbol[self.grid[i][j]]
                self.draw_cell(screen, i, j, color)

    # Create the maze using depth_first_search
    def depth_first_search(self, visited, screen):
        while self.stack:
            current_pos = self.stack[-1]
            current_x, current_y = current_pos
            unvisited_neighbors = self._get_neighbors(current_pos, self._directions, "*", visited)
            # Try to draw on screen
            if current_pos != self.start and len(self.stack)>1:
                self.draw_cell(screen, current_x, current_y, orange)
            self.draw_cell(screen, current_x, current_y, purple)
            update_rects = []
            event_handler()
            if unvisited_neighbors:
                next_pos = random.choice(unvisited_neighbors)
                next_x, next_y = next_pos
                # Mark cell as new path
                middle_cell_x = (current_x + next_x) // 2
                middle_cell_y = (current_y + next_y) // 2
                self.grid[middle_cell_x][middle_cell_y] = " "
                middle_cell = self.draw_cell(screen, middle_cell_x, middle_cell_y, orange)
                update_rects.append(middle_cell)
                self.grid[next_x][next_y] = " "
                next_cell = self.draw_cell(screen, next_x, next_y, orange)
                update_rects.append(next_cell)
                visited.add(next_pos)
                self.stack.append(next_pos)
            else:
                if self.grid[current_x][current_y] == "s":
                    start_cell = self.draw_cell(screen, current_x, current_y, yellow)
                    update_rects.append(start_cell)
                self.stack.pop()
            if update_rects:
                pygame.display.update(update_rects)
            event_handler()

    # Create the maze using Prim's algorithm
    def prim_algorithm(self, screen):
        self._in.add(self.start)
        self._frontier = set(self._get_neighbors(self.start, self._directions, "*", self._in))
        self.grid[self.start[0]][self.start[1]] = " "
        while self._frontier:
            next_pos = random.choice(list(self._frontier))
            self._frontier.remove(next_pos)
            next_x, next_y = next_pos
            update_rects = []
            visited_neighbors = self._find_visited_neighbors(next_pos, self._directions, " ", self._in)
            if visited_neighbors:
                adjacent_cell = random.choice(visited_neighbors)
                adjacent_x, adjacent_y = adjacent_cell
                middle_cell_x = (adjacent_x + next_x) // 2
                middle_cell_y = (adjacent_y + next_y) // 2
                middle_cell = self.draw_cell(screen, middle_cell_x, middle_cell_y, orange)
                next_cell = self.draw_cell(screen, next_x, next_y, orange)
                self.grid[next_x][next_y] = " "
                self._in.add(next_pos)
                self.grid[middle_cell_x][middle_cell_y] = " "
                update_rects.append(middle_cell)
                update_rects.append(next_cell)
            new_frontier = self._get_neighbors(next_pos, self._directions, "*", self._in)
            for neighbor in new_frontier:
                self._frontier.add(neighbor)
            if update_rects:
                pygame.display.update(update_rects)
            event_handler()
        self.grid[self.start[0]][self.start[1]] = "s"

    # Solve the maze using DFS algorithm
    def solve_DFS(self, screen):
        current_x, current_y = self.start
        stack = [(current_x, current_y)]
        visit_list = set()
        visit_list.add(self.start)
        count = 0
        while True:
            count += 1
            if not stack:
                print("Couldn't find a solution")
                return
            current_pos = stack[-1]
            if current_pos == self.end:
                break
            """self.draw_cell(screen, current_pos[0], current_pos[1], green)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            pygame.display.update()"""
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
        print(f"Solution found with {len(stack)} steps")
        print(f"Total steps taken: {count}")

    # Solve the maze using BFS algorithm.
    def solve_BFS(self, screen):
        visited = set()
        visited.add(self.start)
        end_cell = None
        start_cell = self._grid_cell[self.start]
        count = 0
        # Use deque as a doubled ended queue for time efficiency, popping from the left is O(1).
        # When a list is used, popping takes O(n) time.
        queue = deque([start_cell])
        while queue:
            current_cell = queue.popleft()
            count += 1
            current_pos = current_cell.position
            if current_pos == self.end:
                end_cell = current_cell
                break
            neighbors = self._get_neighbors(current_pos, self._solve_directions, " ", visited)
            for next_pos in neighbors:
                visited.add(next_pos)
                next_cell = self._grid_cell[next_pos]
                # If the next position is the end then sets end cell to it and create its parent.
                if next_pos == self.end:
                    end_cell = next_cell
                    end_cell.add_parent(current_cell)
                    break
                # If the next cell already has a parent then keeps that parent, if not then add the current cell as parent
                if next_cell.get_parent() is None:
                    next_cell.add_parent(current_cell)
                queue.append(next_cell)
            self.draw_cell(screen, current_pos[0], current_pos[1], purple)
            event_handler()
        if end_cell:
            solution = end_cell.backtrack()
            print(f"Solution found with {len(solution)} steps.")
            for position in solution:
                self.grid[position[0]][position[1]] = "p"
        else:
            print("No solution")
        self.grid[self.start[0]][self.start[1]] = "s"
        self.grid[self.end[0]][self.end[1]] = "e"
        print(f"Total steps taken: {count}")

    def solve_RHR(self, screen):
        """current_direction = (0, 1)
        end_cell = self._grid_cell[self.end]
        solution = end_cell.backtrack()
        for pos in solution:
            x, y = pos[0], pos[1]
            self.grid[x][y] = "p"
        self.grid[self.start[0]][self.start[1]] = "s"
        self.grid[self.end[0]][self.end[1]] = "e"""
        pass

    # Function to get direction if move from current to next based on the 3 parameters listed below
    def _get_direction(self, current_direction, current_position ,next_position):
        move_x = next_position[0] - current_position[0]
        move_y = next_position[1] - current_position[1]
        move_direction = (move_x, move_y)
        dx, dy = current_direction
        straight = current_direction
        backward = (-dx, -dy)
        right = (dy, -dx)
        left = (-dy, dx)
        direction_map = {"straight": straight, "backward": backward, "right": right, "left": left}
        for key, values in direction_map.items():
            if move_direction == values:
                return key
        return None

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

    # Find neighbors that has already been visited for prim's algorithm
    def _find_visited_neighbors(self, start, direction, symbol, visited_list):
        current_x = start[0]
        current_y = start[1]
        neighbors = []
        for dir in direction:
            next_x = current_x + dir[0]
            next_y = current_y + dir[1]
            if 0 <= next_x < self.row and 0 <= next_y < self.col:
                if self.grid[next_x][next_y] == symbol and (next_x, next_y) in visited_list:
                    neighbors.append((next_x, next_y))
        return neighbors

    def load_map(self, grid):
        self.row = len(grid)
        self.col = len(grid[0])
        self.start = (0, 0)
        self.end = (self.row-2, self.col-2)
        for i in range(self.row):
            for j in range(self.col):
                self._grid_cell[(i,j)] = Cell((i,j), self.end)

    def save_maze(self, file_name):
        maze_content = ""
        for row in self.grid:
            maze_content += "".join(row)
            maze_content += "\n"
        with open(file_name, "w") as f:
            f.write(maze_content)

    # Print out grid to visualize
    def print_grid(self):
        for row in self.grid:
            print("".join(row))



