import time
import pygame
from sys import exit


class Game:

    def __init__(self, player1, player2, board, graphics):
        self.players = [player1, player2]
        self.board = board
        self.graphics = graphics
        self.start()

    def check_quit(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

    def start(self):
        p_turn = 0

        while not self.board.is_end():
            self.check_quit()
            from_c, to, it_bee = self.players[p_turn].get_move()
            self.board.do_move(from_c, to, p_turn, it_bee)
            p_turn = (p_turn + 1) % 2
            self.graphics.draw_board()
            time.sleep(0.5)

