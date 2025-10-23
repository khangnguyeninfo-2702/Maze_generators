class Cell:
    def __init__(self, coordinate):
        self.parent_cell = None
        self.position = coordinate
        self.parent = None
    
    def add_parent(self, parent):
        self.parent_cell = parent
        self.parent = parent.position

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