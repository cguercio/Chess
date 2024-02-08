

class Piece:
    instances = []
    piece_list = []

    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.is_captured = False
        Piece.instances.append(self)