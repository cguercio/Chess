

class Piece:
    instances = []

    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        Piece.instances.append(self)