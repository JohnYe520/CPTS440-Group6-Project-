
# the location and designated turn order of a player on the board
class Player:
    def __init__(self, x, y, num):
        self.X = x
        self.Y = y
        self.PlayerNo = num

    # sets the player's internal location to a given position; doesn't directly affect board logic
    def move(self, x, y):
        self.X = x
        self.Y = y


