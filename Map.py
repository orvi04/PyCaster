class Map:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def set_map(self, map):
        self.map = map

    def get_cell(self, x, y):
        # Convert to integers and check bounds
        x = int(x)
        y = int(y)
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return 1  # Treat out of bounds as wall
        return self.map[y][x]
        