from asyncio.windows_events import NULL


class Wall:
    def __init__(self, space1, space2):
        self.space1 = space1
        self.space2 = space2
        self.neighbor1 = NULL
        self.neighbor2 = NULL
        self.set = False
    
    def addNeighbor(self, neighbor, num):
        if num == 1:
            self.neighbor1 = neighbor
            self.neighbor1.addNeighbor(self, 2)
        else:
            self.neighbor2 = neighbor

    def wallOff(self, neighbor = 0):
        if not self.set:
            self.space1.removeNeighbor(self.space2)
            self.space2.removeNeighbor(self.space1)
            match neighbor:
                case 0:
                    return
                case 1:
                    if self.neighbor1 != NULL:
                        self.neighbor1.wallOff()
                    else:
                        return False
                case 2:
                    if self.neighbor2 != NULL:
                        self.neighbor2.wallOff()
                    else:
                        return False
        else:
            return False




