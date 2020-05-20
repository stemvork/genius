from math import sqrt
import random
import pygame
from hex import Hex
from shapes import Shapes

class Board:
    width = 800
    height = 800
    board_size = (width, height)
    size = 25
    line_width = 1
    tile_color = pygame.Color('#555555')
    colors = [pygame.Color(c) for c in ('#324B4B', '#D56CA5', '#69E1FA', '#5292BD', '#B3E08B', '#E25E3A')]

    # Coolors.co dark slate, champagne, copper, mulberry, purple, green
    # colors = ('#324B4B', '#E1D89F', '#CD8B76', '#C45BAA', '#7D387D', '#749C75')

    def __constructor__(self):
        pass

    @staticmethod
    def draw(screen):
        Board.screen = screen
        for k in range(1+6):
            Board.draw_ring((0, 0), k, Board.colors[2])
        Board.draw_ring((0, 0), 7, Board.colors[3])
        Board.draw_ring((0, 0), 8, Board.colors[3])
        Board.draw_hexagon_axial(0, 0,Board.colors[3])
        for c in range(6):
            Board.draw_empty_primary(*Hex.axial_corners[c], c)

    @staticmethod
    def draw_empty_hex(q, r):
        Board.draw_hexagon_axial(q, r, Board.tile_color)

    @staticmethod
    def draw_empty_primary(q: int, r: int, c: int):
        Board.draw_empty_hex(q, r)
        Shapes.plot_primary(Board.board_size, Board.size, r, c)
        params = Shapes.plot_primary(Board.board_size, Board.size, q, r, c)
        color = Shapes.get_sprite_color(c)
        if c in [0, 2, 4]:
            pygame.draw.polygon(Board.screen, color, params)
        elif c == 1:
            Board.draw_hexagon(*params, color)
        elif c == 3:
            pygame.draw.circle(Board.screen, color, *params)
        elif c == 5:
            pygame.draw.circle(Board.screen, color, *params)

    @staticmethod
    def draw_empty_tile(q, r, k=0):
        (rq, rr) = Hex.axial_directions[k]
        Board.draw_hexagon_axial(q, r, Board.tile_color)
        Board.draw_hexagon_axial(q + rq, r + rr, Board.tile_color)

    @staticmethod
    def draw_hexagon(center, s, fill_color):
        pygame.draw.polygon(Board.screen, fill_color, [Hex.hex_corner(center, s, p) for p in range(6)])
        pygame.draw.polygon(Board.screen, Board.colors[0], [Hex.hex_corner(center, s, p) for p in range(6)], Board.line_width)

    @staticmethod
    def draw_hexagon_axial(q, r, fill_color):
        position = (Board.width / 2 + q * Board.size * 6 / 4, Board.width / 2 + (r + q / 2) * Board.size * sqrt(3))
        Board.draw_hexagon(position, Board.size, fill_color)

    @staticmethod
    def draw_pair(q, r, k=0, c=0):
        Board.draw_empty_tile(q, r, k)
        params = Shapes.plot_primary(Board.board_size, Board.size, q, r, c)
        color = Shapes.get_sprite_color(c)
        if c in [0, 2, 4]:
            pygame.draw.polygon(Board.screen, color, params)
        elif c == 1:
            Board.draw_hexagon(*params, color)
        elif c == 3:
            pygame.draw.circle(Board.screen, color, *params)
        elif c == 5:
            pygame.draw.circle(Board.screen, color, *params)
        (nq, nr) = Hex.hex_neighbor((q,r),k)
        params = Shapes.plot_primary(Board.board_size, Board.size, nq, nr, c)
        if c in [0, 2, 4]:
            pygame.draw.polygon(Board.screen, color, params)
        elif c == 1:
            Board.draw_hexagon(*params, color)
        elif c == 3:
            pygame.draw.circle(Board.screen, color, *params)
        elif c == 5:
            pygame.draw.circle(Board.screen, color, *params)

    @staticmethod
    def draw_ring(center, n, fill_color):
        for p in Hex.hex_ring(center, n):
            Board.draw_hexagon_axial(p[0], p[1], fill_color)

    @staticmethod
    def get_clicked():
        pos = pygame.mouse.get_pos()
        q = (2. / 3 * (pos[0] - Board.width / 2)) / Board.size
        r = (-1. / 3 * (pos[0] - Board.width / 2) + sqrt(3) / 3 * (pos[1] - Board.height / 2)) / Board.size
        return Hex.hex_round((q, r))

    @staticmethod
    def random_color():
        return random.choice(Board.colors)