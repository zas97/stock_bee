import time

from board import Board
from graphics import Graphics
import pygame
class HumanPlayer:
    def __init__(self, board: Board, graphics: Graphics, player_num):
        self.board = board
        self.graphics = graphics
        self.player_num = player_num

    def get_move(self):
        done = False
        move_from = -1
        posible_moves = self.board.get_list_posible_moves(self.player_num)

        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            if pygame.mouse.get_pressed()[0]:
                time.sleep(0.1)
                x, y = pygame.mouse.get_pos()
                i, j = self.graphics.graphic2coord(x, y)
                bee_click = self.graphics.nb_bees_click(x, y)
                if bee_click == self.player_num:
                    move_from = None
                elif move_from == -1:
                    if (i, j) in [m[0] for m in posible_moves]:
                        move_from = (i, j)
                else:
                    move_selected = [m for m in posible_moves if m[0] == move_from and m[1] == (i, j)]
                    if len(move_selected) == 0:
                        move_from = (i, j)
                    elif len(move_selected) == 1:
                        return move_selected[0]
                    else:
                        raise Exception("imposible to have this case")

