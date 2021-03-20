import numpy as np
from board import board_
import pygame

size = width, height = 800, 1200
board_size = 800
board_start = (height - board_size)/2
square_size = int(board_size/8)

def cord_pos(cord):
    return (cord[0]*square_size+square_size/2,
            board_start+cord[1]*square_size+square_size/2)

def coord_trans_t(pos):
    return (pos[1]+pos[3]*2, pos[0]+pos[2]*2)

class rook:
    def __init__(self, col, pos, num):
        self.num = num
        #white is 1; black is -1
        self.col = col
        if self.col == 1:
            self.code = str(num) + "wr"
            self.type = "wr"
        else:
            self.code = str(num) + "br"
            self.type = "br"

        self.pos = np.array(pos)
        #False if taken
        self.state = True
        #can this piece be taken (important for checkmate verification)
        self.killable = False
        self.turn = 0
        #piece type
        self.pt = "r"
        #piece image and rectangle
        self.image = pygame.transform.scale(pygame.image.load("piece_img/"+self.type+".png"), (int(0.85*square_size), int(0.85*square_size)))
        self.rect = self.image.get_rect(center=cord_pos(coord_trans_t(self.pos)))

    def get_take_moves(self, board):

        self.x_mov_u = list([self.pos[0]+i, self.pos[1], self.pos[2], self.pos[3]] for i in range(1, 2-self.pos[0]))
        self.y_mov_u = list([self.pos[0], self.pos[1]+i, self.pos[2], self.pos[3]] for i in range(1, 2-self.pos[1]))
        self.z_mov_u = list([self.pos[0], self.pos[1], self.pos[2]+i, self.pos[3]] for i in range(1, 4-self.pos[2]))
        self.w_mov_u = list([self.pos[0], self.pos[1], self.pos[2], self.pos[3]+i] for i in range(1, 4-self.pos[3]))
        #down (decreasing)
        self.x_mov_d = list([self.pos[0]-i, self.pos[1], self.pos[2], self.pos[3]] for i in range(1, self.pos[0]+1))
        self.y_mov_d = list([self.pos[0], self.pos[1]-i, self.pos[2], self.pos[3]] for i in range(1, self.pos[1]+1))
        self.z_mov_d = list([self.pos[0], self.pos[1], self.pos[2]-i, self.pos[3]] for i in range(1, self.pos[2]+1))
        self.w_mov_d = list([self.pos[0], self.pos[1], self.pos[2], self.pos[3]-i] for i in range(1, self.pos[3]+1))
        #pos_moves as an array (without factoring in collision)
        self.pos_mov = [self.x_mov_u, self.y_mov_u, self.z_mov_u, self.w_mov_u,
                        self.x_mov_d, self.y_mov_d, self.z_mov_d, self.w_mov_d]

        self.take_mov = []
        for direction in self.pos_mov:
            for position in direction:
                if board.board[tuple(position)].col == 0-self.col:
                    self.take_mov.append(tuple(position))
                    break
                elif board.board[tuple(position)].col == self.col:
                    break

        return self.take_mov

    #"get possible moves"
    def get_pos_moves(self, board):
        #this is rly ugly and im sorry
        #pos moves for all direction in all dimensions
        #up (increasing)
        self.x_mov_u = list([self.pos[0]+i, self.pos[1], self.pos[2], self.pos[3]] for i in range(1, 2-self.pos[0]))
        self.y_mov_u = list([self.pos[0], self.pos[1]+i, self.pos[2], self.pos[3]] for i in range(1, 2-self.pos[1]))
        self.z_mov_u = list([self.pos[0], self.pos[1], self.pos[2]+i, self.pos[3]] for i in range(1, 4-self.pos[2]))
        self.w_mov_u = list([self.pos[0], self.pos[1], self.pos[2], self.pos[3]+i] for i in range(1, 4-self.pos[3]))
        #down (decreasing)
        self.x_mov_d = list([self.pos[0]-i, self.pos[1], self.pos[2], self.pos[3]] for i in range(1, self.pos[0]+1))
        self.y_mov_d = list([self.pos[0], self.pos[1]-i, self.pos[2], self.pos[3]] for i in range(1, self.pos[1]+1))
        self.z_mov_d = list([self.pos[0], self.pos[1], self.pos[2]-i, self.pos[3]] for i in range(1, self.pos[2]+1))
        self.w_mov_d = list([self.pos[0], self.pos[1], self.pos[2], self.pos[3]-i] for i in range(1, self.pos[3]+1))
        #pos_moves as an array (without factoring in collision)
        self.pos_mov = [self.x_mov_u, self.y_mov_u, self.z_mov_u, self.w_mov_u,
                        self.x_mov_d, self.y_mov_d, self.z_mov_d, self.w_mov_d]
        #legal moves
        #ik appending sukk but like...
        self.leg_mov = []
        for direction in self.pos_mov:
            for position in direction:
                if board.board[tuple(position)] == board.empty_square:
                    self.leg_mov.append(tuple(position))
                elif board.board[tuple(position)].col != self.col:
                    self.leg_mov.append(tuple(position))
                    break
                elif board.board[tuple(position)].col == self.col:
                    break

        return self.leg_mov

    def is_taken(self, n_pos, board):

        if board.board[n_pos].col == -self.col:
            return True
        return False

    def legal(self, n_pos, board):
        if n_pos in self.get_pos_moves(board):
            return True
        return False

    def move(self, n_pos, board):
        self.pos = n_pos

        self.turn += 1
        if self.is_taken(n_pos, board):
            board.board[n_pos].state = False


class bishop:
    def __init__(self, col, pos, num):
        self.num = num
        #white is 1; black is -1
        self.col = col
        if self.col == 1:
            self.code = str(num) + "wb"
            self.type = "wb"
        else:
            self.code = str(num) + "bb"
            self.type = "bb"

        self.pos = np.array(pos)
        #False if taken
        self.state = True
        #can this piece be taken (important for checkmate verification)
        self.killable = False
        self.turn = 0

        self.pt = "b"
        #piece image and rectangle
        self.image = pygame.transform.scale(pygame.image.load("piece_img/"+self.type+".png"), (int(0.9*square_size), int(0.9*square_size)))
        self.rect = self.image.get_rect(center=cord_pos(coord_trans_t(self.pos)))

    def get_take_moves(self, board):
        #this is rly ugly and im sorry
        #muchachos stinky
        #pos moves for all 2 dimensional diagonals
        self.xy_mov_u = list([self.pos[0]+i, self.pos[1]+i, self.pos[2], self.pos[3]] for i in range(1, min([2 - self.pos[0], 2 - self.pos[1]])))
        self.xz_mov_u = list([self.pos[0]+i, self.pos[1], self.pos[2]+i, self.pos[3]] for i in range(1, min([2 - self.pos[0], 4 - self.pos[2]])))
        self.xw_mov_u = list([self.pos[0]+i, self.pos[1], self.pos[2], self.pos[3]+i] for i in range(1, min([2 - self.pos[0], 4 - self.pos[3]])))
        self.yz_mov_u = list([self.pos[0], self.pos[1]+i, self.pos[2]+i, self.pos[3]] for i in range(1, min([2 - self.pos[1], 4 - self.pos[2]])))
        self.yw_mov_u = list([self.pos[0], self.pos[1]+i, self.pos[2], self.pos[3]+i] for i in range(1, min([2 - self.pos[1], 4 - self.pos[3]])))
        self.zw_mov_u = list([self.pos[0], self.pos[1], self.pos[2]+i, self.pos[3]+i] for i in range(1, min([4 - self.pos[2], 4 - self.pos[3]])))

        self.xy_mov_ud = list([self.pos[0]+i, self.pos[1]-i, self.pos[2], self.pos[3]] for i in range(1, min([2 - self.pos[0], self.pos[1]+1])))
        self.xz_mov_ud = list([self.pos[0]+i, self.pos[1], self.pos[2]-i, self.pos[3]] for i in range(1, min([2 - self.pos[0], self.pos[2]+1])))
        self.xw_mov_ud = list([self.pos[0]+i, self.pos[1], self.pos[2], self.pos[3]-i] for i in range(1, min([2 - self.pos[0], self.pos[3]+1])))
        self.yz_mov_ud = list([self.pos[0], self.pos[1]+i, self.pos[2]-i, self.pos[3]] for i in range(1, min([2 - self.pos[1], self.pos[2]+1])))
        self.yw_mov_ud = list([self.pos[0], self.pos[1]+i, self.pos[2], self.pos[3]-i] for i in range(1, min([2 - self.pos[1], self.pos[3]+1])))
        self.zw_mov_ud = list([self.pos[0], self.pos[1], self.pos[2]+i, self.pos[3]-i] for i in range(1, min([4 - self.pos[2], self.pos[3]+1])))

        self.xy_mov_du = list([self.pos[0]-i, self.pos[1]+i, self.pos[2], self.pos[3]] for i in range(1, min([self.pos[0]+1, 2 - self.pos[1]])))
        self.xz_mov_du = list([self.pos[0]-i, self.pos[1], self.pos[2]+i, self.pos[3]] for i in range(1, min([self.pos[0]+1, 2 - self.pos[2]])))
        self.xw_mov_du = list([self.pos[0]-i, self.pos[1], self.pos[2], self.pos[3]+i] for i in range(1, min([self.pos[0]+1, 2 - self.pos[3]])))
        self.yz_mov_du = list([self.pos[0], self.pos[1]-i, self.pos[2]+i, self.pos[3]] for i in range(1, min([self.pos[1]+1, 4 - self.pos[2]])))
        self.yw_mov_du = list([self.pos[0], self.pos[1]-i, self.pos[2], self.pos[3]+i] for i in range(1, min([self.pos[1]+1, 4 - self.pos[3]])))
        self.zw_mov_du = list([self.pos[0], self.pos[1], self.pos[2]-i, self.pos[3]+i] for i in range(1, min([self.pos[2]+1, 4 - self.pos[3]])))

        self.xy_mov_d = list([self.pos[0]-i, self.pos[1]-i, self.pos[2], self.pos[3]] for i in range(1, min([self.pos[0]+1, self.pos[1]+1])))
        self.xz_mov_d = list([self.pos[0]-i, self.pos[1], self.pos[2]-i, self.pos[3]] for i in range(1, min([self.pos[0]+1, self.pos[2]+1])))
        self.xw_mov_d = list([self.pos[0]-i, self.pos[1], self.pos[2], self.pos[3]-i] for i in range(1, min([self.pos[0]+1, self.pos[3]+1])))
        self.yz_mov_d = list([self.pos[0], self.pos[1]-i, self.pos[2]-i, self.pos[3]] for i in range(1, min([self.pos[1]+1, self.pos[2]+1])))
        self.yw_mov_d = list([self.pos[0], self.pos[1]-i, self.pos[2], self.pos[3]-i] for i in range(1, min([self.pos[1]+1, self.pos[3]+1])))
        self.zw_mov_d = list([self.pos[0], self.pos[1], self.pos[2]-i, self.pos[3]-i] for i in range(1, min([self.pos[2]+1, self.pos[3]+1])))
        #pos_moves as an array (without factoring in collision)
        self.pos_mov = [self.xy_mov_u, self.xz_mov_u, self.xw_mov_u, self.yz_mov_u, self.yw_mov_u, self.zw_mov_u,
                        self.xy_mov_d, self.xz_mov_d, self.xw_mov_d, self.yz_mov_d, self.yw_mov_d, self.zw_mov_d,
                        self.xy_mov_ud, self.xz_mov_ud, self.xw_mov_ud, self.yz_mov_ud, self.yw_mov_ud, self.zw_mov_ud,
                        self.xy_mov_du, self.xz_mov_du, self.xw_mov_du, self.yz_mov_du, self.yw_mov_du, self.zw_mov_du]
        #legal moves
        #ik appending sukk but like...
        self.take_mov = []
        for direction in self.pos_mov:
            for position in direction:
                if board.board[tuple(position)].col == 0-self.col:
                    self.take_mov.append(tuple(position))
                    break
                elif board.board[tuple(position)].col == self.col:
                    break

        return self.take_mov

    def get_pos_moves(self, board):
        #this is rly ugly and im sorry
        #muchachos stinky
        #pos moves for all 2 dimensional diagonals
        self.xy_mov_u = list([self.pos[0]+i, self.pos[1]+i, self.pos[2], self.pos[3]] for i in range(1, min([2 - self.pos[0], 2 - self.pos[1]])))
        self.xz_mov_u = list([self.pos[0]+i, self.pos[1], self.pos[2]+i, self.pos[3]] for i in range(1, min([2 - self.pos[0], 4 - self.pos[2]])))
        self.xw_mov_u = list([self.pos[0]+i, self.pos[1], self.pos[2], self.pos[3]+i] for i in range(1, min([2 - self.pos[0], 4 - self.pos[3]])))
        self.yz_mov_u = list([self.pos[0], self.pos[1]+i, self.pos[2]+i, self.pos[3]] for i in range(1, min([2 - self.pos[1], 4 - self.pos[2]])))
        self.yw_mov_u = list([self.pos[0], self.pos[1]+i, self.pos[2], self.pos[3]+i] for i in range(1, min([2 - self.pos[1], 4 - self.pos[3]])))
        self.zw_mov_u = list([self.pos[0], self.pos[1], self.pos[2]+i, self.pos[3]+i] for i in range(1, min([4 - self.pos[2], 4 - self.pos[3]])))

        self.xy_mov_ud = list([self.pos[0]+i, self.pos[1]-i, self.pos[2], self.pos[3]] for i in range(1, min([2 - self.pos[0], self.pos[1]+1])))
        self.xz_mov_ud = list([self.pos[0]+i, self.pos[1], self.pos[2]-i, self.pos[3]] for i in range(1, min([2 - self.pos[0], self.pos[2]+1])))
        self.xw_mov_ud = list([self.pos[0]+i, self.pos[1], self.pos[2], self.pos[3]-i] for i in range(1, min([2 - self.pos[0], self.pos[3]+1])))
        self.yz_mov_ud = list([self.pos[0], self.pos[1]+i, self.pos[2]-i, self.pos[3]] for i in range(1, min([2 - self.pos[1], self.pos[2]+1])))
        self.yw_mov_ud = list([self.pos[0], self.pos[1]+i, self.pos[2], self.pos[3]-i] for i in range(1, min([2 - self.pos[1], self.pos[3]+1])))
        self.zw_mov_ud = list([self.pos[0], self.pos[1], self.pos[2]+i, self.pos[3]-i] for i in range(1, min([4 - self.pos[2], self.pos[3]+1])))

        self.xy_mov_du = list([self.pos[0]-i, self.pos[1]+i, self.pos[2], self.pos[3]] for i in range(1, min([self.pos[0]+1, 2 - self.pos[1]])))
        self.xz_mov_du = list([self.pos[0]-i, self.pos[1], self.pos[2]+i, self.pos[3]] for i in range(1, min([self.pos[0]+1, 2 - self.pos[2]])))
        self.xw_mov_du = list([self.pos[0]-i, self.pos[1], self.pos[2], self.pos[3]+i] for i in range(1, min([self.pos[0]+1, 2 - self.pos[3]])))
        self.yz_mov_du = list([self.pos[0], self.pos[1]-i, self.pos[2]+i, self.pos[3]] for i in range(1, min([self.pos[1]+1, 4 - self.pos[2]])))
        self.yw_mov_du = list([self.pos[0], self.pos[1]-i, self.pos[2], self.pos[3]+i] for i in range(1, min([self.pos[1]+1, 4 - self.pos[3]])))
        self.zw_mov_du = list([self.pos[0], self.pos[1], self.pos[2]-i, self.pos[3]+i] for i in range(1, min([self.pos[2]+1, 4 - self.pos[3]])))

        self.xy_mov_d = list([self.pos[0]-i, self.pos[1]-i, self.pos[2], self.pos[3]] for i in range(1, min([self.pos[0]+1, self.pos[1]+1])))
        self.xz_mov_d = list([self.pos[0]-i, self.pos[1], self.pos[2]-i, self.pos[3]] for i in range(1, min([self.pos[0]+1, self.pos[2]+1])))
        self.xw_mov_d = list([self.pos[0]-i, self.pos[1], self.pos[2], self.pos[3]-i] for i in range(1, min([self.pos[0]+1, self.pos[3]+1])))
        self.yz_mov_d = list([self.pos[0], self.pos[1]-i, self.pos[2]-i, self.pos[3]] for i in range(1, min([self.pos[1]+1, self.pos[2]+1])))
        self.yw_mov_d = list([self.pos[0], self.pos[1]-i, self.pos[2], self.pos[3]-i] for i in range(1, min([self.pos[1]+1, self.pos[3]+1])))
        self.zw_mov_d = list([self.pos[0], self.pos[1], self.pos[2]-i, self.pos[3]-i] for i in range(1, min([self.pos[2]+1, self.pos[3]+1])))
        #pos_moves as an array (without factoring in collision)
        self.pos_mov = [self.xy_mov_u, self.xz_mov_u, self.xw_mov_u, self.yz_mov_u, self.yw_mov_u, self.zw_mov_u,
                        self.xy_mov_d, self.xz_mov_d, self.xw_mov_d, self.yz_mov_d, self.yw_mov_d, self.zw_mov_d,
                        self.xy_mov_ud, self.xz_mov_ud, self.xw_mov_ud, self.yz_mov_ud, self.yw_mov_ud, self.zw_mov_ud,
                        self.xy_mov_du, self.xz_mov_du, self.xw_mov_du, self.yz_mov_du, self.yw_mov_du, self.zw_mov_du]
        #legal moves
        #ik appending sukk but like...
        self.leg_mov = []
        for direction in self.pos_mov:
            for position in direction:
                if board.board[tuple(position)] == board.empty_square:
                    self.leg_mov.append(tuple(position))
                elif board.board[tuple(position)].col != self.col:
                    self.leg_mov.append(tuple(position))
                    break
                elif board.board[tuple(position)].col == self.col:
                    break

        return self.leg_mov

    def is_taken(self, n_pos, board):
        if board.board[n_pos].col == -self.col:
            return True
        return False

    def legal(self, n_pos, board):
        if n_pos in self.get_pos_moves(board):
            return True
        return False

    def move(self, n_pos, board):
        self.pos = n_pos
        self.turn += 1
        if self.is_taken(n_pos, board):
            board.board[n_pos].state = False


class queen:
    def __init__(self, col, pos, num):
        self.num = num
        #white is 1; black is -1
        self.col = col
        if self.col == 1:
            self.code = str(num) + "wq"
            self.type = "wq"
        else:
            self.code = str(num) + "bq"
            self.type = "bq"

        self.pos = np.array(pos)
        #False if taken
        self.state = True
        #can this piece be taken (important for checkmate verification)
        self.killable = False
        self.turn = 0

        self.pt = "q"
        #piece image and rectangle
        self.image = pygame.transform.scale(pygame.image.load("piece_img/"+self.type+".png"), (int(0.9*square_size), int(0.9*square_size)))
        self.rect = self.image.get_rect(center=cord_pos(coord_trans_t(self.pos)))

    def get_take_moves(self, board):
        #this is rly ugly and im sorry
        #muchachos stinky
        #pos moves for all 2 dimensional diagonals
        self.xy_mov_uu = list([self.pos[0]+i, self.pos[1]+i, self.pos[2], self.pos[3]] for i in range(1, min([2 - self.pos[0], 2 - self.pos[1]])))
        self.xz_mov_uu = list([self.pos[0]+i, self.pos[1], self.pos[2]+i, self.pos[3]] for i in range(1, min([2 - self.pos[0], 4 - self.pos[2]])))
        self.xw_mov_uu = list([self.pos[0]+i, self.pos[1], self.pos[2], self.pos[3]+i] for i in range(1, min([2 - self.pos[0], 4 - self.pos[3]])))
        self.yz_mov_uu = list([self.pos[0], self.pos[1]+i, self.pos[2]+i, self.pos[3]] for i in range(1, min([2 - self.pos[1], 4 - self.pos[2]])))
        self.yw_mov_uu = list([self.pos[0], self.pos[1]+i, self.pos[2], self.pos[3]+i] for i in range(1, min([2 - self.pos[1], 4 - self.pos[3]])))
        self.zw_mov_uu = list([self.pos[0], self.pos[1], self.pos[2]+i, self.pos[3]+i] for i in range(1, min([4 - self.pos[2], 4 - self.pos[3]])))

        self.xy_mov_ud = list([self.pos[0]+i, self.pos[1]-i, self.pos[2], self.pos[3]] for i in range(1, min([2 - self.pos[0], self.pos[1]+1])))
        self.xz_mov_ud = list([self.pos[0]+i, self.pos[1], self.pos[2]-i, self.pos[3]] for i in range(1, min([2 - self.pos[0], self.pos[2]+1])))
        self.xw_mov_ud = list([self.pos[0]+i, self.pos[1], self.pos[2], self.pos[3]-i] for i in range(1, min([2 - self.pos[0], self.pos[3]+1])))
        self.yz_mov_ud = list([self.pos[0], self.pos[1]+i, self.pos[2]-i, self.pos[3]] for i in range(1, min([2 - self.pos[1], self.pos[2]+1])))
        self.yw_mov_ud = list([self.pos[0], self.pos[1]+i, self.pos[2], self.pos[3]-i] for i in range(1, min([2 - self.pos[1], self.pos[3]+1])))
        self.zw_mov_ud = list([self.pos[0], self.pos[1], self.pos[2]+i, self.pos[3]-i] for i in range(1, min([4 - self.pos[2], self.pos[3]+1])))

        self.xy_mov_du = list([self.pos[0]-i, self.pos[1]+i, self.pos[2], self.pos[3]] for i in range(1, min([self.pos[0]+1, 2 - self.pos[1]])))
        self.xz_mov_du = list([self.pos[0]-i, self.pos[1], self.pos[2]+i, self.pos[3]] for i in range(1, min([self.pos[0]+1, 2 - self.pos[2]])))
        self.xw_mov_du = list([self.pos[0]-i, self.pos[1], self.pos[2], self.pos[3]+i] for i in range(1, min([self.pos[0]+1, 2 - self.pos[3]])))
        self.yz_mov_du = list([self.pos[0], self.pos[1]-i, self.pos[2]+i, self.pos[3]] for i in range(1, min([self.pos[1]+1, 4 - self.pos[2]])))
        self.yw_mov_du = list([self.pos[0], self.pos[1]-i, self.pos[2], self.pos[3]+i] for i in range(1, min([self.pos[1]+1, 4 - self.pos[3]])))
        self.zw_mov_du = list([self.pos[0], self.pos[1], self.pos[2]-i, self.pos[3]+i] for i in range(1, min([self.pos[2]+1, 4 - self.pos[3]])))

        self.xy_mov_dd = list([self.pos[0]-i, self.pos[1]-i, self.pos[2], self.pos[3]] for i in range(1, min([self.pos[0]+1, self.pos[1]+1])))
        self.xz_mov_dd = list([self.pos[0]-i, self.pos[1], self.pos[2]-i, self.pos[3]] for i in range(1, min([self.pos[0]+1, self.pos[2]+1])))
        self.xw_mov_dd = list([self.pos[0]-i, self.pos[1], self.pos[2], self.pos[3]-i] for i in range(1, min([self.pos[0]+1, self.pos[3]+1])))
        self.yz_mov_dd = list([self.pos[0], self.pos[1]-i, self.pos[2]-i, self.pos[3]] for i in range(1, min([self.pos[1]+1, self.pos[2]+1])))
        self.yw_mov_dd = list([self.pos[0], self.pos[1]-i, self.pos[2], self.pos[3]-i] for i in range(1, min([self.pos[1]+1, self.pos[3]+1])))
        self.zw_mov_dd = list([self.pos[0], self.pos[1], self.pos[2]-i, self.pos[3]-i] for i in range(1, min([self.pos[2]+1, self.pos[3]+1])))

        self.x_mov_u = list([self.pos[0]+i, self.pos[1], self.pos[2], self.pos[3]] for i in range(1, 2-self.pos[0]))
        self.y_mov_u = list([self.pos[0], self.pos[1]+i, self.pos[2], self.pos[3]] for i in range(1, 2-self.pos[1]))
        self.z_mov_u = list([self.pos[0], self.pos[1], self.pos[2]+i, self.pos[3]] for i in range(1, 4-self.pos[2]))
        self.w_mov_u = list([self.pos[0], self.pos[1], self.pos[2], self.pos[3]+i] for i in range(1, 4-self.pos[3]))

        self.x_mov_d = list([self.pos[0]-i, self.pos[1], self.pos[2], self.pos[3]] for i in range(1, self.pos[0]+1))
        self.y_mov_d = list([self.pos[0], self.pos[1]-i, self.pos[2], self.pos[3]] for i in range(1, self.pos[1]+1))
        self.z_mov_d = list([self.pos[0], self.pos[1], self.pos[2]-i, self.pos[3]] for i in range(1, self.pos[2]+1))
        self.w_mov_d = list([self.pos[0], self.pos[1], self.pos[2], self.pos[3]-i] for i in range(1, self.pos[3]+1))

        #pos_moves as an array (without factoring in collision)
        self.pos_mov = [self.x_mov_u, self.y_mov_u, self.z_mov_u, self.w_mov_u,
                        self.x_mov_d, self.y_mov_d, self.z_mov_d, self.w_mov_d,
                        self.xy_mov_uu, self.xz_mov_uu, self.xw_mov_uu, self.yz_mov_uu, self.yw_mov_uu, self.zw_mov_uu,
                        self.xy_mov_dd, self.xz_mov_dd, self.xw_mov_dd, self.yz_mov_dd, self.yw_mov_dd, self.zw_mov_dd,
                        self.xy_mov_ud, self.xz_mov_ud, self.xw_mov_ud, self.yz_mov_ud, self.yw_mov_ud, self.zw_mov_ud,
                        self.xy_mov_du, self.xz_mov_du, self.xw_mov_du, self.yz_mov_du, self.yw_mov_du, self.zw_mov_du]
        #legal moves
        #ik appending sukk but like...
        self.take_mov = []
        for direction in self.pos_mov:
            for position in direction:
                if board.board[tuple(position)].col == 0-self.col:
                    self.take_mov.append(tuple(position))
                    break
                elif board.board[tuple(position)].col == self.col:
                    break

        return self.take_mov

    def get_pos_moves(self, board):
        #this is rly ugly and im sorry
        #muchachos stinky
        #pos moves for all 2 dimensional diagonals
        self.xy_mov_uu = list([self.pos[0]+i, self.pos[1]+i, self.pos[2], self.pos[3]] for i in range(1, min([2 - self.pos[0], 2 - self.pos[1]])))
        self.xz_mov_uu = list([self.pos[0]+i, self.pos[1], self.pos[2]+i, self.pos[3]] for i in range(1, min([2 - self.pos[0], 4 - self.pos[2]])))
        self.xw_mov_uu = list([self.pos[0]+i, self.pos[1], self.pos[2], self.pos[3]+i] for i in range(1, min([2 - self.pos[0], 4 - self.pos[3]])))
        self.yz_mov_uu = list([self.pos[0], self.pos[1]+i, self.pos[2]+i, self.pos[3]] for i in range(1, min([2 - self.pos[1], 4 - self.pos[2]])))
        self.yw_mov_uu = list([self.pos[0], self.pos[1]+i, self.pos[2], self.pos[3]+i] for i in range(1, min([2 - self.pos[1], 4 - self.pos[3]])))
        self.zw_mov_uu = list([self.pos[0], self.pos[1], self.pos[2]+i, self.pos[3]+i] for i in range(1, min([4 - self.pos[2], 4 - self.pos[3]])))

        self.xy_mov_ud = list([self.pos[0]+i, self.pos[1]-i, self.pos[2], self.pos[3]] for i in range(1, min([2 - self.pos[0], self.pos[1]+1])))
        self.xz_mov_ud = list([self.pos[0]+i, self.pos[1], self.pos[2]-i, self.pos[3]] for i in range(1, min([2 - self.pos[0], self.pos[2]+1])))
        self.xw_mov_ud = list([self.pos[0]+i, self.pos[1], self.pos[2], self.pos[3]-i] for i in range(1, min([2 - self.pos[0], self.pos[3]+1])))
        self.yz_mov_ud = list([self.pos[0], self.pos[1]+i, self.pos[2]-i, self.pos[3]] for i in range(1, min([2 - self.pos[1], self.pos[2]+1])))
        self.yw_mov_ud = list([self.pos[0], self.pos[1]+i, self.pos[2], self.pos[3]-i] for i in range(1, min([2 - self.pos[1], self.pos[3]+1])))
        self.zw_mov_ud = list([self.pos[0], self.pos[1], self.pos[2]+i, self.pos[3]-i] for i in range(1, min([4 - self.pos[2], self.pos[3]+1])))

        self.xy_mov_du = list([self.pos[0]-i, self.pos[1]+i, self.pos[2], self.pos[3]] for i in range(1, min([self.pos[0]+1, 2 - self.pos[1]])))
        self.xz_mov_du = list([self.pos[0]-i, self.pos[1], self.pos[2]+i, self.pos[3]] for i in range(1, min([self.pos[0]+1, 2 - self.pos[2]])))
        self.xw_mov_du = list([self.pos[0]-i, self.pos[1], self.pos[2], self.pos[3]+i] for i in range(1, min([self.pos[0]+1, 2 - self.pos[3]])))
        self.yz_mov_du = list([self.pos[0], self.pos[1]-i, self.pos[2]+i, self.pos[3]] for i in range(1, min([self.pos[1]+1, 4 - self.pos[2]])))
        self.yw_mov_du = list([self.pos[0], self.pos[1]-i, self.pos[2], self.pos[3]+i] for i in range(1, min([self.pos[1]+1, 4 - self.pos[3]])))
        self.zw_mov_du = list([self.pos[0], self.pos[1], self.pos[2]-i, self.pos[3]+i] for i in range(1, min([self.pos[2]+1, 4 - self.pos[3]])))

        self.xy_mov_dd = list([self.pos[0]-i, self.pos[1]-i, self.pos[2], self.pos[3]] for i in range(1, min([self.pos[0]+1, self.pos[1]+1])))
        self.xz_mov_dd = list([self.pos[0]-i, self.pos[1], self.pos[2]-i, self.pos[3]] for i in range(1, min([self.pos[0]+1, self.pos[2]+1])))
        self.xw_mov_dd = list([self.pos[0]-i, self.pos[1], self.pos[2], self.pos[3]-i] for i in range(1, min([self.pos[0]+1, self.pos[3]+1])))
        self.yz_mov_dd = list([self.pos[0], self.pos[1]-i, self.pos[2]-i, self.pos[3]] for i in range(1, min([self.pos[1]+1, self.pos[2]+1])))
        self.yw_mov_dd = list([self.pos[0], self.pos[1]-i, self.pos[2], self.pos[3]-i] for i in range(1, min([self.pos[1]+1, self.pos[3]+1])))
        self.zw_mov_dd = list([self.pos[0], self.pos[1], self.pos[2]-i, self.pos[3]-i] for i in range(1, min([self.pos[2]+1, self.pos[3]+1])))

        self.x_mov_u = list([self.pos[0]+i, self.pos[1], self.pos[2], self.pos[3]] for i in range(1, 2-self.pos[0]))
        self.y_mov_u = list([self.pos[0], self.pos[1]+i, self.pos[2], self.pos[3]] for i in range(1, 2-self.pos[1]))
        self.z_mov_u = list([self.pos[0], self.pos[1], self.pos[2]+i, self.pos[3]] for i in range(1, 4-self.pos[2]))
        self.w_mov_u = list([self.pos[0], self.pos[1], self.pos[2], self.pos[3]+i] for i in range(1, 4-self.pos[3]))

        self.x_mov_d = list([self.pos[0]-i, self.pos[1], self.pos[2], self.pos[3]] for i in range(1, self.pos[0]+1))
        self.y_mov_d = list([self.pos[0], self.pos[1]-i, self.pos[2], self.pos[3]] for i in range(1, self.pos[1]+1))
        self.z_mov_d = list([self.pos[0], self.pos[1], self.pos[2]-i, self.pos[3]] for i in range(1, self.pos[2]+1))
        self.w_mov_d = list([self.pos[0], self.pos[1], self.pos[2], self.pos[3]-i] for i in range(1, self.pos[3]+1))

        #pos_moves as an array (without factoring in collision)
        self.pos_mov = [self.x_mov_u, self.y_mov_u, self.z_mov_u, self.w_mov_u,
                        self.x_mov_d, self.y_mov_d, self.z_mov_d, self.w_mov_d,
                        self.xy_mov_uu, self.xz_mov_uu, self.xw_mov_uu, self.yz_mov_uu, self.yw_mov_uu, self.zw_mov_uu,
                        self.xy_mov_dd, self.xz_mov_dd, self.xw_mov_dd, self.yz_mov_dd, self.yw_mov_dd, self.zw_mov_dd,
                        self.xy_mov_ud, self.xz_mov_ud, self.xw_mov_ud, self.yz_mov_ud, self.yw_mov_ud, self.zw_mov_ud,
                        self.xy_mov_du, self.xz_mov_du, self.xw_mov_du, self.yz_mov_du, self.yw_mov_du, self.zw_mov_du]
        #legal moves
        #ik appending sukk but like...
        self.leg_mov = []
        for direction in self.pos_mov:
            for position in direction:
                if board.board[tuple(position)] == board.empty_square:
                    self.leg_mov.append(tuple(position))
                elif board.board[tuple(position)].col != self.col:
                    self.leg_mov.append(tuple(position))
                    break
                elif board.board[tuple(position)].col == self.col:
                    break

        return self.leg_mov

    def is_taken(self, n_pos, board):
        if board.board[n_pos].col == -self.col:
            return True
        return False

    def legal(self, n_pos, board):
        if n_pos in self.get_pos_moves(board):
            return True
        return False

    def move(self, n_pos, board):
        self.pos = n_pos
        self.turn += 1
        if self.is_taken(n_pos, board):
            board.board[n_pos].state = False


class king:
    def __init__(self, col, pos, num):
        self.num = num
        #white is 1; black is -1
        self.col = col
        if self.col == 1:
            self.code = str(num) + "wk"
            self.type = "wk"
        else:
            self.code = str(num) + "bk"
            self.type = "bk"

        self.pos = np.array(pos)
        #False if taken
        self.state = True
        #can this piece be taken (important for checkmate verification)
        self.killable = False
        self.turn = 0

        self.pt = "k"
        #piece image and rectangle
        self.image = pygame.transform.scale(pygame.image.load("piece_img/"+self.type+".png"), (int(0.9*square_size), int(0.9*square_size)))
        self.rect = self.image.get_rect(center=cord_pos(coord_trans_t(self.pos)))

    def get_take_moves(self, board):
        #this is rly ugly and im sorry
        #pos moves for all direction in all dimensions
        self.xy_mov_uu = list([self.pos[0]+i, self.pos[1]+i, self.pos[2], self.pos[3]] for i in range(1, min([2 - self.pos[0], 2 - self.pos[1], 2])))
        self.xz_mov_uu = list([self.pos[0]+i, self.pos[1], self.pos[2]+i, self.pos[3]] for i in range(1, min([2 - self.pos[0], 4 - self.pos[2], 2])))
        self.xw_mov_uu = list([self.pos[0]+i, self.pos[1], self.pos[2], self.pos[3]+i] for i in range(1, min([2 - self.pos[0], 4 - self.pos[3], 2])))
        self.yz_mov_uu = list([self.pos[0], self.pos[1]+i, self.pos[2]+i, self.pos[3]] for i in range(1, min([2 - self.pos[1], 4 - self.pos[2], 2])))
        self.yw_mov_uu = list([self.pos[0], self.pos[1]+i, self.pos[2], self.pos[3]+i] for i in range(1, min([2 - self.pos[1], 4 - self.pos[3], 2])))
        self.zw_mov_uu = list([self.pos[0], self.pos[1], self.pos[2]+i, self.pos[3]+i] for i in range(1, min([4 - self.pos[2], 4 - self.pos[3], 2])))

        self.xy_mov_ud = list([self.pos[0]+i, self.pos[1]-i, self.pos[2], self.pos[3]] for i in range(1, min([2 - self.pos[0], self.pos[1]+1, 2])))
        self.xz_mov_ud = list([self.pos[0]+i, self.pos[1], self.pos[2]-i, self.pos[3]] for i in range(1, min([2 - self.pos[0], self.pos[2]+1, 2])))
        self.xw_mov_ud = list([self.pos[0]+i, self.pos[1], self.pos[2], self.pos[3]-i] for i in range(1, min([2 - self.pos[0], self.pos[3]+1, 2])))
        self.yz_mov_ud = list([self.pos[0], self.pos[1]+i, self.pos[2]-i, self.pos[3]] for i in range(1, min([2 - self.pos[1], self.pos[2]+1, 2])))
        self.yw_mov_ud = list([self.pos[0], self.pos[1]+i, self.pos[2], self.pos[3]-i] for i in range(1, min([2 - self.pos[1], self.pos[3]+1, 2])))
        self.zw_mov_ud = list([self.pos[0], self.pos[1], self.pos[2]+i, self.pos[3]-i] for i in range(1, min([4 - self.pos[2], self.pos[3]+1, 2])))

        self.xy_mov_du = list([self.pos[0]-i, self.pos[1]+i, self.pos[2], self.pos[3]] for i in range(1, min([self.pos[0]+1, 2 - self.pos[1], 2])))
        self.xz_mov_du = list([self.pos[0]-i, self.pos[1], self.pos[2]+i, self.pos[3]] for i in range(1, min([self.pos[0]+1, 2 - self.pos[2], 2])))
        self.xw_mov_du = list([self.pos[0]-i, self.pos[1], self.pos[2], self.pos[3]+i] for i in range(1, min([self.pos[0]+1, 2 - self.pos[3], 2])))
        self.yz_mov_du = list([self.pos[0], self.pos[1]-i, self.pos[2]+i, self.pos[3]] for i in range(1, min([self.pos[1]+1, 4 - self.pos[2], 2])))
        self.yw_mov_du = list([self.pos[0], self.pos[1]-i, self.pos[2], self.pos[3]+i] for i in range(1, min([self.pos[1]+1, 4 - self.pos[3], 2])))
        self.zw_mov_du = list([self.pos[0], self.pos[1], self.pos[2]-i, self.pos[3]+i] for i in range(1, min([self.pos[2]+1, 4 - self.pos[3], 2])))

        self.xy_mov_dd = list([self.pos[0]-i, self.pos[1]-i, self.pos[2], self.pos[3]] for i in range(1, min([self.pos[0]+1, self.pos[1]+1, 2])))
        self.xz_mov_dd = list([self.pos[0]-i, self.pos[1], self.pos[2]-i, self.pos[3]] for i in range(1, min([self.pos[0]+1, self.pos[2]+1, 2])))
        self.xw_mov_dd = list([self.pos[0]-i, self.pos[1], self.pos[2], self.pos[3]-i] for i in range(1, min([self.pos[0]+1, self.pos[3]+1, 2])))
        self.yz_mov_dd = list([self.pos[0], self.pos[1]-i, self.pos[2]-i, self.pos[3]] for i in range(1, min([self.pos[1]+1, self.pos[2]+1, 2])))
        self.yw_mov_dd = list([self.pos[0], self.pos[1]-i, self.pos[2], self.pos[3]-i] for i in range(1, min([self.pos[1]+1, self.pos[3]+1, 2])))
        self.zw_mov_dd = list([self.pos[0], self.pos[1], self.pos[2]-i, self.pos[3]-i] for i in range(1, min([self.pos[2]+1, self.pos[3]+1, 2])))

        self.x_mov_u = list([self.pos[0]+i, self.pos[1], self.pos[2], self.pos[3]] for i in range(1, min(2-self.pos[0], 2)))
        self.y_mov_u = list([self.pos[0], self.pos[1]+i, self.pos[2], self.pos[3]] for i in range(1, min(2-self.pos[1], 2)))
        self.z_mov_u = list([self.pos[0], self.pos[1], self.pos[2]+i, self.pos[3]] for i in range(1, min(4-self.pos[2], 2)))
        self.w_mov_u = list([self.pos[0], self.pos[1], self.pos[2], self.pos[3]+i] for i in range(1, min(4-self.pos[3], 2)))

        self.x_mov_d = list([self.pos[0]-i, self.pos[1], self.pos[2], self.pos[3]] for i in range(1, min(self.pos[0]+1, 2)))
        self.y_mov_d = list([self.pos[0], self.pos[1]-i, self.pos[2], self.pos[3]] for i in range(1, min(self.pos[1]+1, 2)))
        self.z_mov_d = list([self.pos[0], self.pos[1], self.pos[2]-i, self.pos[3]] for i in range(1, min(self.pos[2]+1, 2)))
        self.w_mov_d = list([self.pos[0], self.pos[1], self.pos[2], self.pos[3]-i] for i in range(1, min(self.pos[3]+1, 2)))
        #pos_moves as an array (without factoring in collision)
        self.pos_mov = [self.x_mov_u, self.y_mov_u, self.z_mov_u, self.w_mov_u,
                        self.x_mov_d, self.y_mov_d, self.z_mov_d, self.w_mov_d,
                        self.xy_mov_uu, self.xz_mov_uu, self.xw_mov_uu, self.yz_mov_uu, self.yw_mov_uu, self.zw_mov_uu,
                        self.xy_mov_dd, self.xz_mov_dd, self.xw_mov_dd, self.yz_mov_dd, self.yw_mov_dd, self.zw_mov_dd,
                        self.xy_mov_ud, self.xz_mov_ud, self.xw_mov_ud, self.yz_mov_ud, self.yw_mov_ud, self.zw_mov_ud,
                        self.xy_mov_du, self.xz_mov_du, self.xw_mov_du, self.yz_mov_du, self.yw_mov_du, self.zw_mov_du]

        #legal moves
        #ik appending sukk but like...
        self.take_mov = []
        for direction in self.pos_mov:
            for position in direction:
                if board.board[tuple(position)].col == 0-self.col:
                    self.take_mov.append(tuple(position))
                    break
                elif board.board[tuple(position)].col == self.col:
                    break

        return self.take_mov

    #"get possible moves"
    def get_pos_moves(self, board):
        #this is rly ugly and im sorry
        #pos moves for all direction in all dimensions
        self.xy_mov_uu = list([self.pos[0]+i, self.pos[1]+i, self.pos[2], self.pos[3]] for i in range(1, min([2 - self.pos[0], 2 - self.pos[1], 2])))
        self.xz_mov_uu = list([self.pos[0]+i, self.pos[1], self.pos[2]+i, self.pos[3]] for i in range(1, min([2 - self.pos[0], 4 - self.pos[2], 2])))
        self.xw_mov_uu = list([self.pos[0]+i, self.pos[1], self.pos[2], self.pos[3]+i] for i in range(1, min([2 - self.pos[0], 4 - self.pos[3], 2])))
        self.yz_mov_uu = list([self.pos[0], self.pos[1]+i, self.pos[2]+i, self.pos[3]] for i in range(1, min([2 - self.pos[1], 4 - self.pos[2], 2])))
        self.yw_mov_uu = list([self.pos[0], self.pos[1]+i, self.pos[2], self.pos[3]+i] for i in range(1, min([2 - self.pos[1], 4 - self.pos[3], 2])))
        self.zw_mov_uu = list([self.pos[0], self.pos[1], self.pos[2]+i, self.pos[3]+i] for i in range(1, min([4 - self.pos[2], 4 - self.pos[3], 2])))

        self.xy_mov_ud = list([self.pos[0]+i, self.pos[1]-i, self.pos[2], self.pos[3]] for i in range(1, min([2 - self.pos[0], self.pos[1]+1, 2])))
        self.xz_mov_ud = list([self.pos[0]+i, self.pos[1], self.pos[2]-i, self.pos[3]] for i in range(1, min([2 - self.pos[0], self.pos[2]+1, 2])))
        self.xw_mov_ud = list([self.pos[0]+i, self.pos[1], self.pos[2], self.pos[3]-i] for i in range(1, min([2 - self.pos[0], self.pos[3]+1, 2])))
        self.yz_mov_ud = list([self.pos[0], self.pos[1]+i, self.pos[2]-i, self.pos[3]] for i in range(1, min([2 - self.pos[1], self.pos[2]+1, 2])))
        self.yw_mov_ud = list([self.pos[0], self.pos[1]+i, self.pos[2], self.pos[3]-i] for i in range(1, min([2 - self.pos[1], self.pos[3]+1, 2])))
        self.zw_mov_ud = list([self.pos[0], self.pos[1], self.pos[2]+i, self.pos[3]-i] for i in range(1, min([4 - self.pos[2], self.pos[3]+1, 2])))

        self.xy_mov_du = list([self.pos[0]-i, self.pos[1]+i, self.pos[2], self.pos[3]] for i in range(1, min([self.pos[0]+1, 2 - self.pos[1], 2])))
        self.xz_mov_du = list([self.pos[0]-i, self.pos[1], self.pos[2]+i, self.pos[3]] for i in range(1, min([self.pos[0]+1, 2 - self.pos[2], 2])))
        self.xw_mov_du = list([self.pos[0]-i, self.pos[1], self.pos[2], self.pos[3]+i] for i in range(1, min([self.pos[0]+1, 2 - self.pos[3], 2])))
        self.yz_mov_du = list([self.pos[0], self.pos[1]-i, self.pos[2]+i, self.pos[3]] for i in range(1, min([self.pos[1]+1, 4 - self.pos[2], 2])))
        self.yw_mov_du = list([self.pos[0], self.pos[1]-i, self.pos[2], self.pos[3]+i] for i in range(1, min([self.pos[1]+1, 4 - self.pos[3], 2])))
        self.zw_mov_du = list([self.pos[0], self.pos[1], self.pos[2]-i, self.pos[3]+i] for i in range(1, min([self.pos[2]+1, 4 - self.pos[3], 2])))

        self.xy_mov_dd = list([self.pos[0]-i, self.pos[1]-i, self.pos[2], self.pos[3]] for i in range(1, min([self.pos[0]+1, self.pos[1]+1, 2])))
        self.xz_mov_dd = list([self.pos[0]-i, self.pos[1], self.pos[2]-i, self.pos[3]] for i in range(1, min([self.pos[0]+1, self.pos[2]+1, 2])))
        self.xw_mov_dd = list([self.pos[0]-i, self.pos[1], self.pos[2], self.pos[3]-i] for i in range(1, min([self.pos[0]+1, self.pos[3]+1, 2])))
        self.yz_mov_dd = list([self.pos[0], self.pos[1]-i, self.pos[2]-i, self.pos[3]] for i in range(1, min([self.pos[1]+1, self.pos[2]+1, 2])))
        self.yw_mov_dd = list([self.pos[0], self.pos[1]-i, self.pos[2], self.pos[3]-i] for i in range(1, min([self.pos[1]+1, self.pos[3]+1, 2])))
        self.zw_mov_dd = list([self.pos[0], self.pos[1], self.pos[2]-i, self.pos[3]-i] for i in range(1, min([self.pos[2]+1, self.pos[3]+1, 2])))

        self.x_mov_u = list([self.pos[0]+i, self.pos[1], self.pos[2], self.pos[3]] for i in range(1, min(2-self.pos[0], 2)))
        self.y_mov_u = list([self.pos[0], self.pos[1]+i, self.pos[2], self.pos[3]] for i in range(1, min(2-self.pos[1], 2)))
        self.z_mov_u = list([self.pos[0], self.pos[1], self.pos[2]+i, self.pos[3]] for i in range(1, min(4-self.pos[2], 2)))
        self.w_mov_u = list([self.pos[0], self.pos[1], self.pos[2], self.pos[3]+i] for i in range(1, min(4-self.pos[3], 2)))

        self.x_mov_d = list([self.pos[0]-i, self.pos[1], self.pos[2], self.pos[3]] for i in range(1, min(self.pos[0]+1, 2)))
        self.y_mov_d = list([self.pos[0], self.pos[1]-i, self.pos[2], self.pos[3]] for i in range(1, min(self.pos[1]+1, 2)))
        self.z_mov_d = list([self.pos[0], self.pos[1], self.pos[2]-i, self.pos[3]] for i in range(1, min(self.pos[2]+1, 2)))
        self.w_mov_d = list([self.pos[0], self.pos[1], self.pos[2], self.pos[3]-i] for i in range(1, min(self.pos[3]+1, 2)))
        #pos_moves as an array (without factoring in collision)
        self.pos_mov = [self.x_mov_u, self.y_mov_u, self.z_mov_u, self.w_mov_u,
                        self.x_mov_d, self.y_mov_d, self.z_mov_d, self.w_mov_d,
                        self.xy_mov_uu, self.xz_mov_uu, self.xw_mov_uu, self.yz_mov_uu, self.yw_mov_uu, self.zw_mov_uu,
                        self.xy_mov_dd, self.xz_mov_dd, self.xw_mov_dd, self.yz_mov_dd, self.yw_mov_dd, self.zw_mov_dd,
                        self.xy_mov_ud, self.xz_mov_ud, self.xw_mov_ud, self.yz_mov_ud, self.yw_mov_ud, self.zw_mov_ud,
                        self.xy_mov_du, self.xz_mov_du, self.xw_mov_du, self.yz_mov_du, self.yw_mov_du, self.zw_mov_du]

        #legal moves
        #ik appending sukk but like...
        self.leg_mov = []
        for direction in self.pos_mov:
            for position in direction:
                if board.board[tuple(position)] == board.empty_square:
                    self.leg_mov.append(tuple(position))
                elif board.board[tuple(position)].col != self.col:
                    self.leg_mov.append(tuple(position))
                    break
                elif board.board[tuple(position)].col == self.col:
                    break

        return self.leg_mov

    def is_taken(self, n_pos, board):
        if board.board[n_pos].col == -self.col:
            return True
        return False

    def legal(self, n_pos, board):
        if n_pos in self.get_pos_moves(board):
            return True
        return False

    def move(self, n_pos, board):
        self.pos = n_pos
        self.turn += 1
        if self.is_taken(n_pos, board):
            board.board[n_pos].state = False


class knight:
    def __init__(self, col, pos, num):
        self.dim_lim = (2,2,4,4)
        self.num = num
        #white is 1; black is -1
        self.col = col
        if self.col == 1:
            self.code = str(num) + "wx"
            self.type = "wx"
        else:
            self.code = str(num) + "bx"
            self.type = "bx"

        self.pos = np.array(pos)
        #False if taken
        self.state = True
        #can this piece be taken (important for checkmate verification)
        self.killable = False
        self.turn = 0

        self.pt = "x"
        #piece image and rectangle
        self.image = pygame.transform.scale(pygame.image.load("piece_img/"+self.type+".png"), (int(0.9*square_size), int(0.9*square_size)))
        self.rect = self.image.get_rect(center=cord_pos(coord_trans_t(self.pos)))

    def get_take_moves(self, board):
        #legal moves
        self.take_mov = []
        #big dimension and direction
        for dim in range(2,4):
            #-1 down; 1 up
            for dir in [-1,1]:
                #test if move can be made for big dim and dir
                if -1<self.pos[dim]+2*dir and self.pos[dim]+2*dir<4:
                    #short dimension and direction
                    for com_dim in range(0, 4):
                        #(com_dim can not == dim)
                        if com_dim != dim:
                            for com_dir in [-1, 1]:
                                self.mov = list(self.pos)
                                self.mov[dim] = self.mov[dim]+2*dir
                                self.mov[com_dim] = self.mov[com_dim]+com_dir
                                #range test for small dim and dir (and collision test)
                                if -1<self.pos[com_dim]+com_dir and self.pos[com_dim]+com_dir<self.dim_lim[com_dim] and board.board[tuple(self.mov)].col == 0-self.col:

                                    self.take_mov.append(tuple(self.mov))

        return self.take_mov

    #"get possible moves"
    def get_pos_moves(self, board):
        #legal moves
        self.leg_mov = []
        #big dimension and direction
        for dim in range(2,4):
            #-1 down; 1 up
            for dir in [-1,1]:
                #test if move can be made for big dim and dir
                if -1<self.pos[dim]+2*dir and self.pos[dim]+2*dir<4:
                    #short dimension and direction
                    for com_dim in range(0, 4):
                        #(com_dim can not == dim)
                        if com_dim != dim:
                            for com_dir in [-1, 1]:
                                self.mov = list(self.pos)
                                self.mov[dim] = self.mov[dim]+2*dir
                                self.mov[com_dim] = self.mov[com_dim]+com_dir
                                #range test for small dim and dir (and collision test)
                                if -1<self.pos[com_dim]+com_dir and self.pos[com_dim]+com_dir<self.dim_lim[com_dim] and board.board[tuple(self.mov)].col != self.col:

                                    self.leg_mov.append(tuple(self.mov))

        return self.leg_mov

    def is_taken(self, n_pos, board):
        if board.board[n_pos].col == -self.col:
            return True
        return False

    def legal(self, n_pos, board):
        if n_pos in self.get_pos_moves(board):
            return True
        return False

    def move(self, n_pos, board):
        self.pos = n_pos
        self.turn += 1
        if self.is_taken(n_pos, board):
            board.board[n_pos].state = False


class pawn:
    def __init__(self, col, pos, num):
        self.dim_lim = (2,2,4,4)
        self.num = num
        #white is 1; black is -1
        self.col = col
        if self.col == 1:
            self.code = str(num) + "wp"
            self.type = "wp"
        else:
            self.code = str(num) + "bp"
            self.type = "bp"

        self.pos = np.array(pos)
        #False if taken
        self.state = True
        #can this piece be taken (important for checkmate verification)
        self.killable = False
        self.turn = 0

        self.pt = "p"
        #piece image and rectangle
        self.image = pygame.transform.scale(pygame.image.load("piece_img/"+self.type+".png"), (int(0.8*square_size), int(0.8*square_size)))
        self.rect = self.image.get_rect(center=cord_pos(coord_trans_t(self.pos)))

    def get_take_moves(self, board):
        #legal moves
        self.take_mov = []
        self.move_dir = 0-self.col

        for dim in [1, 3]:
            for dir in [-1, 1]:
                self.mov = list(self.pos)
                self.mov[2] = self.mov[2]+self.move_dir
                self.mov[dim] = self.mov[dim]+dir
                if -1<self.mov[dim] and self.mov[dim]<self.dim_lim[dim] and board.board[tuple(self.mov)].col == 0 - self.col:
                    self.take_mov.append(tuple(self.mov))

        return self.take_mov

    #"get possible moves"
    def get_pos_moves(self, board):
        #legal moves
        self.leg_mov = []
        #z dim
        #pawns move away from their side of the board
        #(straight move)
        self.move_dir = 0-self.col
        self.mov = list(self.pos)
        for i in range(0, 2):
            self.mov[2] = self.mov[2]+self.move_dir
            if self.mov[2]<4:
                if board.board[tuple(self.mov)].col == None:
                    self.leg_mov.append(tuple(self.mov))

        #diagonal take

        #can only go diagonal in the x(1) and w(3) dimensions
        #(similar to the fukky knight loops)
        for dim in [1, 3]:
            for dir in [-1, 1]:
                self.mov = list(self.pos)
                self.mov[2] = self.mov[2]+self.move_dir
                self.mov[dim] = self.mov[dim]+dir
                if -1<self.mov[dim] and self.mov[dim]<self.dim_lim[dim] and board.board[tuple(self.mov)].col == 0 - self.col:
                    self.leg_mov.append(tuple(self.mov))

        return self.leg_mov

    def is_taken(self, n_pos, board):
        if board.board[n_pos].col == -self.col:
            return True
        return False

    def legal(self, n_pos, board):
        if n_pos in self.get_pos_moves(board):
            return True
        return False

    def move(self, n_pos, board):
        self.pos = n_pos
        self.turn += 1
        if self.is_taken(n_pos, board):
            board.board[n_pos].state = False
        if self.col == -1:
            if self.pos[2]==3:
                self.state = False

        if self.col == 1:
            if self.pos[2]==0:
                self.state = False
