from asyncio.windows_events import NULL


class Wall:
    def __init__(self, spaces):
        self.spaces = spaces
        self.set = False
        self.neighbors = []

    def add_neighbor(self, wall):
        self.neighbors.append(wall)

    def wall_off(self):
        if not self.set:
            self.spaces[0].remove_neighbor(self.spaces[1])
            self.spaces[1].remove_neighbor(self.spaces[0])
            self.spaces[2].remove_neighbor(self.spaces[3])
            self.spaces[3].remove_neighbor(self.spaces[2])
            self.set = True
            for n in self.neighbors:
                n.set = True
        return self.set




