# General libraries
from random import choice
import pygame as pg
from math import sqrt, floor

# Project files
from hex import Hex
from shapes import Shapes


class Board:
    # Board sizes
    width = 800
    height = 800
    board_size = (width, height)
    board_center = (width/2, height/2)

    # Control sizes
    control_width = 200
    screen_size = (width + control_width, height)

    # Hex sizes
    size = 25
    line_width = 1

    # Colors
    tile_color = pg.Color('#555555')
    colors = [pg.Color(c) for c in ('#324B4B', '#D56CA5', '#69E1FA', '#5292BD', '#B3E08B', '#E25E3A')]
    screen = None

    # TODO: move to game logic
    blocked = []
    placed_tiles = []

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
        Board.draw_hexagon_axial(0, 0, Board.colors[3])
        for c in range(6):
            Board.draw_empty_primary(*Hex.axial_corners[c], c)

    @staticmethod
    def draw_control(font, scores, names, tileset_count):
        sz = floor(220/18)  # square size
        sm = max(1, floor(sz/10))
        sx = Board.width - 60
        sy = 45 - floor(sz / 4)
        py = 11 * sz
        for p in range(2):
            name_sprite = font.render(names[p], False, (255, 255, 255))
            name_coords = (Board.screen_size[0] - 26 - font.size(names[p])[0], 8 + p * py)
            Board.screen.blit(name_sprite, name_coords)
            for j in range(6):
                for i in range(18):
                    score_rect_dim = (sx + i * (sz + sm), sy + j * (sz + sm) + p * py, sz, sz)
                    pg.draw.rect(Board.screen, (100, 100, 100), score_rect_dim)
                score_token_dim = (sx + scores[p][j] * (sz + sm), sy + j * (sz + sm) + p * py, sz, sz)
                pg.draw.rect(Board.screen, Shapes.sprite_colors[j], score_token_dim)
        tileset_count_sprite = font.render(str(tileset_count+1), False, (255, 255, 255))
        Board.screen.blit(tileset_count_sprite, (30, 30))

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
            pg.draw.polygon(Board.screen, color, params)
        elif c == 1:
            Board.draw_hexagon(*params, color)
        elif c == 3:
            pg.draw.circle(Board.screen, color, *params)
        elif c == 5:
            pg.draw.circle(Board.screen, color, *params)

    @staticmethod
    def draw_empty_tile(q, r, k=0):
        (rq, rr) = Hex.axial_directions[k]
        Board.draw_hexagon_axial(q, r, Board.tile_color)
        Board.draw_hexagon_axial(q + rq, r + rr, Board.tile_color)

    @staticmethod
    def draw_hexagon(center, s, fill_color, hex_screen=None):
        if not hex_screen:
            hex_screen = Board.screen
        pg.draw.polygon(hex_screen, fill_color, [Hex.hex_corner(center, s, p) for p in range(6)])
        pg.draw.polygon(hex_screen, Board.colors[0],
                        [Hex.hex_corner(center, s, p) for p in range(6)], Board.line_width)

    @staticmethod
    def draw_hexagon_axial(q, r, fill_color, hex_screen=None):
        if not hex_screen:
            hex_screen = Board.screen
        position = (Board.width / 2 + q * Board.size * 6 / 4, Board.width / 2 + (r + q / 2) * Board.size * sqrt(3))
        Board.draw_hexagon(position, Board.size, fill_color, hex_screen)

    @staticmethod
    def draw_pair(coords, cols):
        (q, r, k) = coords
        (c1, c2) = cols
        Board.draw_empty_tile(q, r, k)
        # TODO: DRY for two tiles
        params1 = Shapes.plot_primary(Board.board_size, Board.size, q, r, c1)
        color1 = Shapes.get_sprite_color(c1)
        if c1 in [0, 2, 4]:
            pg.draw.polygon(Board.screen, color1, params1)
        elif c1 == 1:
            Board.draw_hexagon(*params1, color1)
        elif c1 == 3:
            pg.draw.circle(Board.screen, color1, *params1)
        elif c1 == 5:
            pg.draw.circle(Board.screen, color1, *params1)
        (nq, nr) = Hex.hex_neighbor((q, r), k)
        params2 = Shapes.plot_primary(Board.board_size, Board.size, nq, nr, c2)
        color2 = Shapes.get_sprite_color(c2)
        if c2 in [0, 2, 4]:
            pg.draw.polygon(Board.screen, color2, params2)
        elif c2 == 1:
            Board.draw_hexagon(*params2, color2)
        elif c2 == 3:
            pg.draw.circle(Board.screen, color2, *params2)
        elif c2 == 5:
            pg.draw.circle(Board.screen, color2, *params2)

    @staticmethod
    def draw_ring(center, n, fill_color):
        for p in Hex.hex_ring(center, n):
            Board.draw_hexagon_axial(p[0], p[1], fill_color)

    @staticmethod
    def get_mouse_axial():
        pos = pg.mouse.get_pos()
        q = (2. / 3 * (pos[0] - Board.width / 2)) / Board.size
        r = (-1. / 3 * (pos[0] - Board.width / 2) + sqrt(3) / 3 * (pos[1] - Board.height / 2)) / Board.size
        return Hex.hex_round((q, r))

    @staticmethod
    def get_clicked_distance():
        return Board.get_distance(Board.get_mouse_axial())

    @staticmethod
    def get_distance(h, s=(0, 0)):
        return Hex.hex_distance(s, h)

    @staticmethod
    def get_next(tileset):
        return tileset.pop(0)

    @staticmethod
    def is_legal(coords):
        (q, r, k) = coords
        distance = Board.get_distance((q, r))
        if distance <= 6:
            (nq, nr) = Hex.hex_neighbor((q, r), k)
            neighbor_distance = Board.get_distance((nq, nr))
            # Check if clicked on 2-player board => distance 6
            if neighbor_distance <= 6:
                # exit if square is non-empty
                if (q, r) in Board.blocked:
                    print("clicked in blocked")
                    return False
                elif (nq, nr) in Board.blocked:
                    print("neighbor in blocked")
                    return False
                else:
                    return True

    @staticmethod
    def is_on_board(coord):
        if Hex.hex_distance((0, 0), coord) > 7:
            return False
        else:
            return True

    @staticmethod
    def place(current_tile, current_rot):
        coord = Board.get_mouse_axial()
        if Board.is_legal((*coord, current_rot)):
            tile = ((*coord, current_rot), current_tile)
            neighbor = Hex.hex_neighbor(coord, current_rot)
            Board.blocked.append(coord)
            Board.blocked.append(neighbor)

            Board.placed_tiles.append(tile)

            return True
        else:
            return False

    @staticmethod
    def random_color():
        return choice(Board.colors)

    @ staticmethod
    def score(player):
        score_inc = []
        tile = Board.placed_tiles[len(Board.placed_tiles)-1]
        (q, r, k) = tile[0]
        (nq, nr) = Hex.hex_neighbor((q, r), k)
        for pt in Board.placed_tiles:
            ((pq, pr, pk), (p1, p2)) = pt
            for i in range(6):
                if i != pk:
                    (tq, tr) = Hex.hex_neighbor((pq, pr), i)
                    if (q, r) == (tq, tr) and tile[1][0] == p1:
                        score_inc.append((p1, 1))
                    if (nq, nr) == (tq, tr) and tile[1][1] == p2:
                        score_inc.append((p2, 1))
        return score_inc
