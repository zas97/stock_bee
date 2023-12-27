import random


class RandomPlayer:
    def __init__(self, board, player_num):
        self.board = board
        self.player_num = player_num

    def get_move(self):
        p_moves = self.board.get_list_posible_moves(self.player_num)
        for m in p_moves:
            if random.random() > 0.5:
                return m
        return p_moves[0]
