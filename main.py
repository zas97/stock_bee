from board import Board
import board_configuration
from random_player import RandomPlayer
from graphics import Graphics
import time
from game import Game
from human_player import HumanPlayer
from minimax_player import MiniMaxPlayer



b = Board(
    board_configuration.configuration
)
gf = Graphics(b.board_array, board_configuration.configuration, board_configuration.colors, b.nb_bees)
b.graphics = gf
p1 = HumanPlayer(b, gf, 0)
# p1 = MiniMaxPlayer(0, b, 3)
p2 = MiniMaxPlayer(1, b, 5)
g = Game(p1, p2, b, gf)
g.start()



