from board import Board
import board_configuration
from random_player import RandomPlayer
from graphics import Graphics
import time
from game import Game



b = Board(
    board_configuration.configuration
)
gf = Graphics(b.board_array, board_configuration.configuration, board_configuration.colors, b.nb_bees)
p1 = RandomPlayer(b, 0)
p2 = RandomPlayer(b, 1)
g = Game(p1, p2, b, gf)

