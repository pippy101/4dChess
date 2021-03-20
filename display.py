import numpy as np
import sys, pygame
from engine import match, coord_trans_t, coord_trans_f

size = width, height = 800, 1200
#board stoof
board_size = 800
board_start = (height - board_size)/2
square_size = int(board_size/8)

#cord to pos
def cord_pos(cord):
    return (cord[0]*square_size+square_size/2,
            board_start+cord[1]*square_size+square_size/2)

#pos to cord
def pos_cord(pos):
    return (int(pos[0]/square_size),
            int((pos[1]-board_start)/square_size))

def main():
    game = match()
    selected_piece = None
    #prep stuff
    white = 255, 255, 255
    dark_square =  160, 82, 45
    light_square =  240, 220, 210
    highlight = 240, 10, 7
    over = False

    screen = pygame.display.set_mode(size)

    while not over:
        if game.turn_n%2==0:
            color = "w"
            color_n = 1
        else:
            color = "b"
            color_n = -1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                if selected_piece == None:
                    pp = game.select(color, color_n, pos_cord(pygame.mouse.get_pos()))
                    if pp != None:
                        selected_piece = game.game.board.board[coord_trans_f(pos_cord(pygame.mouse.get_pos()))]
                else:
                    if pos_cord(pygame.mouse.get_pos()) == coord_trans_t(selected_piece.pos):
                        selected_piece.rect.center = cord_pos(coord_trans_t(selected_piece.pos))
                        selected_piece = None
                    else:
                        np_ = game.legal(color, color_n, pos_cord(pygame.mouse.get_pos()))
                        if np_ != None:
                            selected_piece.rect.center = cord_pos(pos_cord(pygame.mouse.get_pos()))
                            game.turn(np_)
                            game.turn_n += 1
                            selected_piece = None
                        else:
                            selected_piece.rect.center = cord_pos(coord_trans_t(selected_piece.pos))
                            selected_piece = None

        screen.fill(white)
        #drawing grid
        for x in range(8):
            for y in range(8):
                if (y % 2 == 0 and x % 2 == 0) or (y % 2 != 0 and x % 2 != 0):
                    pygame.draw.rect(screen, dark_square,
                                     [x*square_size,board_start+y*square_size,square_size,square_size])
                else:
                    pygame.draw.rect(screen, light_square,
                                     [x*square_size,board_start+y*square_size,square_size,square_size])

        #drawing pieces
        for piece in list(game.pieces):
            if game.pieces[piece].state:
                screen.blit(game.pieces[piece].image, game.pieces[piece].rect)
            else:
                if game.pieces[piece].pt == "k":
                    if game.pieces[piece].col == 1:
                        print("Black has Won")
                        over = True

                    if game.pieces[piece].col == -1:
                        print("White has Won")
                        over = True

        #highlighting possible moves
        if selected_piece != None:
            for x in range(8):
                for y in range(8):
                    if coord_trans_f((x, y)) in selected_piece.get_pos_moves(game.game.board):
                        rect = pygame.Surface((square_size, square_size))
                        rect.set_alpha(128)
                        rect.fill(highlight)
                        screen.blit(rect, (x*square_size,board_start+y*square_size,square_size,square_size))

        pygame.display.flip()

if __name__ == "__main__":
    main()
