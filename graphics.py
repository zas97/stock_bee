import math

import pygame


class Graphics:
    def __init__(self, board_array, flowers, flower_color, bee_count):
        pygame.font.init()
        self.width = 600
        self.height = 600
        self.width_square = self.width / len(board_array)
        self.width_square = self.height / len(board_array)
        self.board_array = board_array
        self.flowers = flowers
        self.flower_color = flower_color
        self.spacing = self.height / len(self.board_array) / 2
        self.r = self.spacing - 6
        self.bee_picture = pygame.transform.scale(pygame.image.load("img/bee.png"),
                                                       (self.r, self.r))
        self.bee_count = bee_count
        self.draw_board()

    def draw_board(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.screen.fill(pygame.Color("white"))

        for i in range(9):
            for j in range(9):
                if self.board_array[i][j] != -1:
                    self.draw_tile(i, j)
        self.draw_bees()
        self.draw_flowers()
        self.draw_nb_bees()
        pygame.display.flip()

    def draw_nb_bees(self):
        font = pygame.font.SysFont("Calibri", 48)
        img = font.render(str(self.bee_count[0]), True, "green")
        rect = img.get_rect()

        pygame.draw.rect(img, "green", rect, 1)
        self.screen.blit(img, (50, 450))
        self.rect_nb_1 = (50, 450, 50 + rect[2], 450+rect[3])

        img = font.render(str(self.bee_count[1]), True, "brown")
        rect = img.get_rect()
        pygame.draw.rect(img, "brown", rect, 1)
        self.screen.blit(img, (500, 450))
        self.rect_nb_2 = (500, 450, 500 + rect[2], 450+rect[3])

    def nb_bees_click(self, x, y):
        if self.rect_nb_1[0] <= x <= self.rect_nb_1[2]:
            return 0
        if self.rect_nb_1[1] <= x <= self.rect_nb_1[3]:
            return 1
        return -1

    def graphic2coord(self, x, y):
        return math.floor(y * len(self.board_array) / self.width), math.floor(x * len(self.board_array) / self.height)


    def coord2graphic(self, i, j):
        len_board = len(self.board_array)
        return j / len_board * self.height, (i / len_board) * self.width

    def draw_tile(self, i, j):
        g_i, g_j = self.coord2graphic(i, j)

        pygame.draw.circle(self.screen,
                           pygame.Color("black"),
                           (g_i + self.spacing, g_j + self.spacing), self.r, 1)

    def draw_flowers(self):
        flowers_drawn = [[0] * len(self.board_array) for el in range(len(self.board_array))]
        for color, g_f in zip(self.flower_color, self.flowers):
            prev_coord = None
            for coord in g_f:
                i, j = len(self.board_array) - coord[1] - 1, coord[0]
                g_i, g_j = self.coord2graphic(i, j)
                flowers_drawn[i][j] += 3
                pygame.draw.circle(self.screen,
                                   pygame.Color(color),
                                   (g_i + self.spacing, g_j + self.spacing), self.r + flowers_drawn[i][j], 3)
                if prev_coord is not None:
                    prev_i, prev_j = len(self.board_array) - prev_coord[1] - 1, prev_coord[0]
                    prev_g_i, prev_g_j = self.coord2graphic(prev_i, prev_j)
                    pygame.draw.line(self.screen,
                                     pygame.Color(color),
                                     (g_i + self.spacing, g_j + self.spacing),
                                     (prev_g_i + self.spacing, prev_g_j + self.spacing))
                prev_coord = coord

    def draw_bees(self):
        for i in range(len(self.board_array)):
            for j in range(len(self.board_array)):
                if self.board_array[i][j] > 0:
                    color = "green" if self.board_array[i][j] == 1 else "brown"
                    g_i, g_j = self.coord2graphic(i, j)

                    pygame.draw.circle(self.screen,
                                       color,
                                       (g_i + self.spacing, g_j + self.spacing), self.r - 6, 0
                                       )
                    self.screen.blit(self.bee_picture, (g_i + self.r/1.6, g_j + self.r/1.6))
