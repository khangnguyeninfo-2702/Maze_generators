class Cell:
    def __init__(self, coordinate):
        self.parent_cell = None
        self.position = coordinate
        self.parent = None
    
    def add_parent(self, parent):
        self.parent = parent
        self.parent_cell = Cell(parent)
    
    def backtrack(self, cell):
        path = set()
        