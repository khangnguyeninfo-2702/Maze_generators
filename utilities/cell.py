import pygame

distance_color = (0, 0, 0)

class Cell:
    def __init__(self, coordinate, end):
        self.parent_cell = None
        self.position = coordinate
        self.parent = None
        self.step_to_end = end[0] - self.position[0] + end[1] - self.position[1]
    
    def add_parent(self, parent):
        self.parent_cell = parent
        self.parent = parent.position

    def draw_distance(self, screen, cell_size):
        font = pygame.font.Font(None, 15)
        distance_text = font.render(f"{self.step_to_end}", True, distance_color)
        screen.blit(distance_text, (self.position[1]*cell_size, self.position[0]*cell_size))

    def get_parent(self):
        return self.parent_cell
    
    def backtrack(self):
        path = []
        current_cell = self
        while current_cell is not None:
            path.append(current_cell.position)
            current_cell = current_cell.get_parent()
        path.reverse()
        return path