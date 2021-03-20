import numpy as np
from pieces import rook, bishop, queen, king, knight, pawn
from board import board_, h_board_
from time import sleep

###     NOTE:      ###
###  (y,x,\/,>)    ###
###  x is knight   ###

piece_dict = {"p": pawn, "x": knight, "k": king, "q": queen, "b": bishop, "r": rook}
#coord conversion
def coord_trans_t(pos):
    return (pos[1]+pos[3]*2, pos[0]+pos[2]*2)

def coord_trans_f(pos):
    return (int(np.ceil((pos[1]/2)-np.floor(pos[1]/2))), int(np.ceil((pos[0]/2)-np.floor(pos[0]/2))),
            int(np.floor(pos[1]/2)), int(np.floor(pos[0]/2)))

class engine:
    def __init__(self, board, pieces):
        self.pieces = pieces
        self.board = board
        self.taken = []

    def update_board(self):
        self.board.board = np.full((2,2,4,4), self.board.empty_square)
        for piece in list(self.pieces):
            if self.pieces[piece].state:
                self.board.place_piece(self.pieces[piece])
            else:
                if not self.pieces[piece] in self.taken:
                    self.taken.append(self.pieces[piece])

    def check_ver(self, color, pieces, board):
        for piece in list(pieces):
            if pieces[piece].col != color:
                moves = pieces[piece].get_take_moves(board)
                for move_ in moves:
                    if board.board[move_].pt == "k" and board.board[move_].col == -color:
                        return True
        return False

class match:
    def __init__(self):
        self.pieces = {"1br": rook(-1, (0,0,0,0), 1), "2br": rook(-1, (0,1,0,3), 2),
                       "1wr": rook(1, (1,0,3,0), 1), "2wr": rook(1, (1,1,3,3), 2),
                       "1bb": bishop(-1, (0,0,0,1), 1), "2bb": bishop(-1, (0,1,0,2), 2),
                       "1wb": bishop(1, (1,0,3,1), 1), "2wb": bishop(1, (1,1,3,2), 2),
                       "1bq": queen(-1, (0,0,0,2), 1), "1wq": queen(1, (1,1,3,1), 1),
                       "1bk": king(-1, (0,1,0,1), 1), "1wk": king(1, (1,0,3,2), 1),
                       "1bx": knight(-1, (0,1,0,0), 1), "2bx": knight(-1, (0,0,0,3), 2),
                       "1wx": knight(1, (1,1,3,0), 1), "2wx": knight(1, (1,0,3,3), 2)}

        #making pawns:
        for color in [-1, 1]:
            for i in range(0,8):
                if color == 1:
                    self.pieces[str(str(i+1)+"wp")] = pawn(1, coord_trans_f((i,6)), i+1)
                if color == -1:
                    self.pieces[str(str(i+1)+"bp")] = pawn(-1, coord_trans_f((i,1)), i+1)

        self.game = engine(board_(), self.pieces)
        self.game.update_board()
        self.turn_n = 0
        #[IS WHITE IN CHECK, IS BLACK IN CHECK]
        self.check = [False, False]
        self.over = False

    def h_check_ver(self, color, piece_pos, new_pos):
        h_pieces = {}
        for piece in list(self.pieces):
            h_pieces[self.pieces[piece].code] = piece_dict[self.pieces[piece].pt](self.pieces[piece].col, self.pieces[piece].pos, self.pieces[piece].num)

        h_board = h_board_(h_pieces)
        h_pieces[h_board.board[piece_pos].code].move(new_pos, h_board)
        h_board.update(h_pieces)
        print(h_board.projection())
        return self.game.check_ver(color, pieces = h_pieces, board = h_board)

    def select(self,col,col_n, piece_pos_xy):
        if not piece_pos_xy[0]<8:
            print("Out of board bounds")
            return None
        self.piece_pos = coord_trans_f(piece_pos_xy)
        if self.game.board.board[self.piece_pos].code != "...":
            if self.pieces[self.game.board.board[self.piece_pos].code].col == col_n:
                return self.piece_pos
            else:
                print("Piece selected is the wrong color")
                return None
        else:
            print("Square selected is empty")
            return None

    def legal(self, col, col_n, piece_pos):
        self.new_pos = coord_trans_f(piece_pos)
        if self.pieces[self.game.board.board[self.piece_pos].code].legal(self.new_pos, self.game.board):
            if not self.h_check_ver(col_n, self.piece_pos, self.new_pos):
                return self.new_pos
            else:
                print("Move = Check")
                return None
        else:
            print("Illegal Move")
            return None

    def turn(self, pos):
        self.pieces[self.game.board.board[self.piece_pos].code].move(pos, self.game.board)
        self.game.update_board()
