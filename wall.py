from asyncio.windows_events import NULL


class Wall:
    # def __init__(self, space1, space2, space3, space4):
    def __init__(self, spaces):
        self.spaces = spaces
        # self.space1 = space1
        # self.space2 = space2
        # self.space3 = space3
        # self.space4 = space4
        # self.neighbor1 = NULL
        # self.neighbor2 = NULL
        self.set = False
    
    # def addNeighbor(self, neighbor, num):
    #     if num == 1:
    #         self.neighbor1 = neighbor
    #         self.neighbor1.addNeighbor(self, 2)
    #     else:
    #         self.neighbor2 = neighbor

    def wall_off(self, neighbor = 0):
        if not self.set:
            self.spaces[0].remove_neighbor(self.spaces[1])
            self.spaces[1].remove_neighbor(self.spaces[0])
            self.spaces[2].remove_neighbor(self.spaces[3])
            self.spaces[3].remove_neighbor(self.spaces[2])
            # self.space1.removeNeighbor(self.space2)
            # self.space2.removeNeighbor(self.space1)
            # self.space3.removeNeighbor(self.space4)
            # self.space4.removeNeighbor(self.space3)
            self.set = True
            # match neighbor:
            #     case 0:
            #         return
            #     case 1:
            #         if self.neighbor1 != NULL:
            #             self.neighbor1.wallOff()
            #         else:
            #             return False
            #     case 2:
            #         if self.neighbor2 != NULL:
            #             self.neighbor2.wallOff()
            #         else:
            #             return False
        return self.set




