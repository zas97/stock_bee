import random

from board import Board


class MiniMaxPlayer:
    def __init__(self, player_num, board: Board, depth=4):
        self.player_num = player_num
        self.board = board
        self.depth = depth

    def negamax(self, depth, player_num):
        if depth == 0 or self.board.is_end():
            r = self.board.evaluate()
            if player_num == 0:
                return r
            else:
                return -r
        posible_moves = self.board.get_list_posible_moves(player_num)
        best_move = -500
        for m in posible_moves:
            self.board.do_move(m[0], m[1], player_num, m[2])
            aux = -self.negamax(depth - 1, (player_num + 1) % 2)
            best_move = max(aux, best_move)
            self.board.undo(m[0], m[1], player_num, m[2])
        return best_move

    def get_move(self):
        posible_moves = self.board.get_list_posible_moves(self.player_num)
        best_move_score = -500
        best_move = None
        for m in posible_moves:
            self.board.do_move(m[0], m[1], self.player_num, m[2])
            aux = -self.negamax(self.depth - 1, (self.player_num + 1) % 2)
            print(m, round(aux, 6))
            if (aux > best_move_score) or (aux == best_move_score and bool(random.getrandbits(1))):
                best_move = m
                best_move_score = aux
            self.board.undo(m[0], m[1], self.player_num, m[2])
        print()
        return best_move
