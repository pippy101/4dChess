import numpy as np
import sys, pygame
from engine import match, coord_trans_t, coord_trans_f
from pieces import size, width, height, board_size, board_start, square_size

#cord to pos
def cord_pos(cord):
    return (cord[0]*square_size+square_size/2,
            board_start+cord[1]*square_size+square_size/2)

#pos to cord
def pos_cord(pos):
    return (int(pos[0]/square_size),
            int((pos[1]-board_start)/square_size))

def main():
    print("Turn 1")
    #getting font
    pygame.font.init()
    font = pygame.font.SysFont('Arial', 30)

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
        b_surrender_hover = False
        w_surrender_hover = False
        mouse_pos = pygame.mouse.get_pos()
        if board_size+(width-board_size)/2-square_size*0.9<mouse_pos[0] and mouse_pos[0]<board_size+(width-board_size)/2-square_size*0.9+square_size*1.9:
            if board_size-square_size<mouse_pos[1] and mouse_pos[1]<board_size-square_size+square_size*0.6:
                w_surrender_hover = True
            if square_size<mouse_pos[1] and mouse_pos[1]<square_size+square_size*0.6:
                b_surrender_hover = True
        #points for each color [white,black]
        points = [0, 0]
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
                if w_surrender_hover or b_surrender_hover:
                    over = True
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
                            print("Turn "+str(game.turn_n+1))
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
                #adding points for taken pieces
                if game.pieces[piece].col == 1:
                    points[1] += game.pieces[piece].points
                elif game.pieces[piece].col == -1:
                    points[0] += game.pieces[piece].points

        #score rendering
        white_score = font.render("White Score: "+str(points[0]), False, (0, 0, 0))
        black_score = font.render("Black Score: "+str(points[1]), False, (0, 0, 0))

        screen.blit(white_score, (board_size, height-4*square_size))
        screen.blit(black_score, (board_size, height-4*square_size-40))

        #resign buttons
        if w_surrender_hover:
            pygame.draw.rect(screen, (120, 120, 120), (board_size+(width-board_size)/2-square_size*0.9, board_size-square_size, square_size*1.9, square_size*0.6))
        else:
            pygame.draw.rect(screen, (180, 180, 180), (board_size+(width-board_size)/2-square_size*0.9, board_size-square_size, square_size*1.9, square_size*0.6))
        screen.blit(font.render("White Resign", False, (255, 255, 255)), (board_size+(width-board_size)/2-square_size*0.9, board_size-square_size))

        if b_surrender_hover:
            pygame.draw.rect(screen, (120, 120, 120), (board_size+(width-board_size)/2-square_size*0.9, square_size, square_size*1.9, square_size*0.6))
        else:
            pygame.draw.rect(screen, (180, 180, 180), (board_size+(width-board_size)/2-square_size*0.9, square_size, square_size*1.9, square_size*0.6))
        screen.blit(font.render("Black Resign", False, (255, 255, 255)), (board_size+(width-board_size)/2-square_size*0.9, square_size))

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
