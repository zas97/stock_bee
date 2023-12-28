from typing import List, Tuple
import numpy as np

def pretty_print(board_array):
    for line in board_array:
        for i in line:
            print(str(i).rjust(3), end="")
        print()

def coord2board(x, y):
    return 8 - y, x


def init_board_array():
    board = [[0] * 9 for i in range(9)]
    for i in range(9):
        for j in range(9):
            if abs(i - 4) + abs(j - 4) > 4:
                board[i][j] = -1
    return board


class Board:
    def __init__(self, flowers: List[List[Tuple[int, int]]]):
        self.board_array = init_board_array()
        self.flowers = flowers
        self.flowers = [[coord2board(f[0], f[1]) for f in g] for g in flowers]
        self.nb_bees = [16, 16]
        self.pos_bees = [[], []]
        self.graphics = None
        self.nb_turns_bee_drop = 0

    def get_dest(self, from_c, way, d):
        coord = [from_c[0], from_c[1]]
        while True:
            coord[d] += way
            if coord[d] < 0 or coord[d] >= len(self.board_array) or self.board_array[coord[0]][coord[1]] != 0:
                coord[d] -= way
                break
        return coord[0], coord[1]

    def get_list_posible_moves(self, player_num):
        # skip move
        if self.nb_bees[player_num] == 0:
            return [(None, None, None)]

        list_moves = []
        ways = [-1, 1]
        directions = [0, 1]
        for way in ways:
            for d in directions:
                from_c = (4, 4)
                to = self.get_dest(from_c, way, d)
                if to != from_c:
                    list_moves.append((None, to, None))

        if self.board_array[4][5] > 0 and self.board_array[5][4] > 0 and self.board_array[3][4] > 0 and self.board_array[4][3] > 0:
            list_moves.append((None, (4, 4), None))

        for way in ways:
            for d in directions:
                for it, from_c in enumerate(self.pos_bees[player_num]):
                    to = self.get_dest(from_c, way, d)
                    if to != from_c and to != (4, 4):
                        list_moves.append((from_c, to, it))

        return list_moves

    def is_end(self):
        if self.board_array[4][4] > 0:
            return True
        if sum(self.nb_bees) == 0:
            return True
        return False

    def evaluate(self):
        if self.is_end():
            winner = self.get_winner()
            if winner == 0:
                return 200
            if winner == 1:
                return -200
            return 0
        r = 0
        for g_f in self.flowers:
            nb_captured = [0, 0]
            for i, j in g_f:
                if self.board_array[i][j] > 0:
                    nb_captured[self.board_array[i][j] - 1] += 1

            for p in range(2):
                sign = (-2*p +1)
                op_p = (p+1) % 2
                if nb_captured[p] == len(g_f):
                    r += len(g_f) * sign
                    # bigger values for longer
                    r += (10 ** (-6 + len(g_f)))
                if nb_captured[p] == (len(g_f) - 1) and nb_captured[op_p] == 0:
                    r += (len(g_f) - 1) / 10 * sign
        return r
    def get_points(self):
        count = [0, 0]
        sizes_g = [[], []]
        for g_f in self.flowers:
            prev_occupier = 0
            is_captured = True
            for i, j in g_f:
                if self.board_array[i][j] == 0:
                    is_captured = False
                    break
                if prev_occupier != 0 and prev_occupier != self.board_array[i][j]:
                    is_captured = False
                    break
                prev_occupier = self.board_array[i][j]
            if is_captured:
                count[prev_occupier - 1] += len(g_f)
                sizes_g[prev_occupier - 1].append(len(g_f))
        return count, sizes_g

    def get_winner(self):
        points, sizes = self.get_points()
        if points[0] > points[1]:
            return 0
        if points[1] > points[0]:
            return 1
        sizes[0].sort(reverse=True)
        sizes[1].sort(reverse=True)
        for s1, s2 in zip(*sizes):
            if s1 > s2:
                return 0
            if s2 > s1:
                return 1
        return None

    def do_move(self, from_c, to, player_num, it_bee):
        if from_c is None and to is None:
            return

        elif from_c is None:
            self.nb_bees[player_num] -= 1
            self.pos_bees[player_num].append(to)
        else:
            self.board_array[from_c[0]][from_c[1]] = 0
            self.pos_bees[player_num][it_bee] = to

        self.board_array[to[0]][to[1]] = player_num + 1

    def undo(self, from_c, to, player_num, it_bee):
        if from_c is None and to is None:
            return

        elif from_c is None:
            self.nb_bees[player_num] += 1
            self.pos_bees[player_num].pop()
        else:
            self.board_array[from_c[0]][from_c[1]] = player_num + 1
            self.pos_bees[player_num][it_bee] = from_c

        self.board_array[to[0]][to[1]] = 0

    def paint_board(self):
        for it, flow in enumerate(self.flowers):
            for x, y in flow:
                i, j = coord2board(x, y)
                self.board_array[i][j] = it + 1
        pretty_print(self.board_array)
