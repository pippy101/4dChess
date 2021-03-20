import numpy as np

###EMPTY SQUARE###
class empty_square:
    def __init__(self):
        self.col = None
        self.code = "..."


###BOARD###
class board_:
    def __init__(self):
        self.empty_square = empty_square()
        self.board = np.full((2,2,4,4), self.empty_square)

    def place_piece(self, piece):
        self.board[tuple(piece.pos)] = piece

    def projection(self):
        self.proj = np.full((8,8), '...')
        for x in range(2):
            for y in range(2):
                for z in range(4):
                    for w in range(4):
                        self.proj[x + 2 * z, y + 2 * w] = self.board[x, y, z, w].code

        return self.proj

class h_board_:
    def __init__(self, pieces):
        self.empty_square = empty_square()
        self.board = np.full((2,2,4,4), self.empty_square)
        for piece in list(pieces):
            if pieces[piece].state:
                self.board[tuple(pieces[piece].pos)] = pieces[piece]

    def update(self, pieces):
        self.board = np.full((2,2,4,4), self.empty_square)
        for piece in list(pieces):
            if pieces[piece].state:
                self.board[tuple(pieces[piece].pos)] = pieces[piece]

    def projection(self):
        self.proj = np.full((8,8), '...')
        for x in range(2):
            for y in range(2):
                for z in range(4):
                    for w in range(4):
                        self.proj[x + 2 * z, y + 2 * w] = self.board[x, y, z, w].code

        return self.proj
