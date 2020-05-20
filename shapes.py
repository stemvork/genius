from math import pi, sqrt, cos, sin
import pygame

# Sprites
# yellow 24 star,
# orange hexagon
# blue 6 star,
# green circle,
# red 11/12 star,
# purple circle stroked,


class Shapes:
    sprite_colors = [pygame.Color(c) for c in ('#ffff00', '#ffae19', '#1351d8', '#00ff00', '#ff0000', '#cc00cc')]

    def __constructor(self):
        pass

    @staticmethod
    def get_sprite_color(c):
        return Shapes.sprite_colors[c]

    @staticmethod
    def get_position(board_size, size, q, r):
        (w, h) = board_size
        return (w, h, size), (w / 2 + q * size * 6 / 4, w / 2 + (r + q / 2) * size * sqrt(3))

    @staticmethod
    def plot_shape(position, size, c):
        star_size = 0.7 * size
        other_size = 0.65 * size
        circle_thickness = 5
        if c == 0:
            return Shapes.plot_regular_star(position, (24, pi / 12, star_size), 2)
        elif c == 1:
            return position, other_size
        elif c == 2:
            return Shapes.plot_regular_star(position, (5, -pi / 10, star_size))
        elif c == 3:
            return position, other_size
        elif c == 4:
            return Shapes.plot_regular_star(position, (12, pi / 6, star_size), 1.5)
        elif c == 5:
            return position, other_size, circle_thickness

    @staticmethod
    def plot_primary(board_size, size, q, r, c=0):
        plotting = Shapes.get_position(board_size, size, q, r)
        (w, h, size) = plotting[0]
        position = plotting[1]
        return Shapes.plot_shape(position, size, c)

    # @staticmethod
    # def draw_secondary(board_size, size, q, r, c=0):  # expects neighbours q, r!
    #     plotting = Shapes.get_position(board_size, size, q, r)
    #     (w, h, size) = plotting[0]
    #     position = plotting[1]
    #     Shapes.plot_shape(position, size, c)
    #
    #     (q, r) = Hex.hex_neighbor((q, r), k)
    #     position = (width / 2 + q * size * 6 / 4, width / 2 + (r + q / 2) * size * sqrt(3))
    #     Shapes.plot_shape(position, size, c)

    @staticmethod
    def plot_regular_star(center: (), params: (), correction: float = 1):
        (x, y) = center
        (n, angle, r) = params
        pts = []
        phi = (1 + sqrt(5)) / 2
        for i in range(n):
            rx = x + r * cos(angle + pi * 2 * i / n)
            ry = y + r * sin(angle + pi * 2 * i / n)
            pts.append([int(rx), int(ry)])
            rx = x + correction * r / phi ** 2 * cos(angle + pi * 2 * i / n + pi / n)
            ry = y + correction * r / phi ** 2 * sin(angle + pi * 2 * i / n + pi / n)
            pts.append([int(rx), int(ry)])
        return pts
