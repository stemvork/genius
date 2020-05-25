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

    # ???? TODO: move to game logic
    blocked = []
    placed_tiles = []
    arrows = []
    color_map = []

    @staticmethod
    def draw(screen):
        Board.screen = screen
        for k in range(1+6):
            Board.draw_ring((0, 0), k, Board.colors[2])
        Board.draw_hexagon_axial(0, 0, Board.colors[3])

    # noinspection PyUnusedLocal
    @staticmethod
    def draw_control(font, scores, inc, turn, names, tileset_count):
        # TODO: huge method
        sz = floor(220/19)  # square size
        sm = max(1, floor(sz/10))
        sx = Board.width - 60
        sy = 45 - floor(sz / 4)
        py = 11 * sz
        for p in range(2):
            name_color = (255, 255, 255) if (p == turn) else (0, 0, 0)
            name_sprite = font.render(names[p], False, name_color)
            name_coords = (Board.screen_size[0] - 26 - font.size(names[p])[0], 8 + p * py)
            Board.screen.blit(name_sprite, name_coords)
            for j in range(6):
                for i in range(19):
                    score_rect_dim = (sx + i * (sz + sm), sy + j * (sz + sm) + p * py, sz, sz)
                    score_rect_color = (100, 100, 100) if i < 10 else (170, 170, 170)
                    pg.draw.rect(Board.screen, score_rect_color, score_rect_dim)

                ac = (120, 120, 120) if p == turn else (255, 255, 170)
                aw = inc[p][j] * sz
                ax = sx + sm + scores[p][j] * (sz + sm) - aw
                pg.draw.rect(Board.screen, ac, (ax, sy + 4 + j * (sz + sm) + p * py, aw, 4))

                score_token_dim = (sx + scores[p][j] * (sz + sm), sy + j * (sz + sm) + p * py, sz, sz)
                pg.draw.rect(Board.screen, Shapes.sprite_colors[j], score_token_dim)

        # tileset_count_sprite = font.render(str(tileset_count+1), False, (255, 255, 255))
        # Board.screen.blit(tileset_count_sprite, (30, 30))

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
    def draw_line(s, k):
        line = Board.get_line(s, k)
        [Board.add_arrow(line[i], line[i+1], 0) for i in range(len(line)-1)]

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
    def get_color_coords(c):
        coords = []
        for pt in Board.placed_tiles:
            if Board.is_on_board(pt[0][0:2]):
                if pt[1][0] == c:
                    coords.append(pt[0][0:2])
            if Board.is_on_board(Board.get_other_coord(pt)):
                if pt[1][1] == c:
                    coords.append(Board.get_other_coord(pt))
        return coords

    @staticmethod
    def get_color_map():
        color_map = []
        for i in range(6):
            color_map.append(Board.get_color_coords(i))
        return color_map

    @staticmethod
    def get_distance(h, s=(0, 0)):
        return Hex.hex_distance(s, h)

    @staticmethod
    def get_line(start, k):
        tiles = []
        coord = Hex.hex_neighbor(start, k)
        if Board.is_on_board(coord):
            tiles.append(coord)
            Board.get_line_step(coord, k, tiles)
        return tiles

    @staticmethod
    def get_line_step(coord, k, tiles):
        coord = Hex.hex_neighbor(coord, k)
        if Board.is_on_board(coord):
            tiles.append(coord)
            Board.get_line_step(coord, k, tiles)

    @staticmethod
    def get_next(tileset):
        return tileset.pop(0)

    @staticmethod
    def get_other_coord(tile):
        return tuple(Hex.hex_neighbor(tile[0][0:2], tile[0][2]))

    @staticmethod
    def axial_to_screen(pos):
        (q, r) = pos
        return Board.width / 2 + q * Board.size * 6 / 4, Board.width / 2 + (r + q / 2) * Board.size * sqrt(3)

    @staticmethod
    def is_on_board(coord):
        if Hex.hex_distance((0, 0), coord) > 6:
            return False
        else:
            return True

    @staticmethod
    def is_legal(coords):
        (q, r, k) = coords
        tile = (q, r)
        if Board.is_on_board((q, r)):
            neighbor = Hex.hex_neighbor((q, r), k)
            # Check if clicked on 2-player board => distance 6
            if Board.is_on_board(neighbor):
                # exit if square is non-empty
                if tile in Board.blocked:
                    print("clicked in blocked")
                    return False
                elif neighbor in Board.blocked:
                    print("neighbor in blocked")
                    return False
                else:
                    distances_tile = [Hex.hex_distance(tile, pt[0][0:2]) for pt in Board.placed_tiles]
                    distances_other = [Hex.hex_distance(tile, Board.get_other_coord(pt)) for pt in Board.placed_tiles]
                    neighbor_tile = [Hex.hex_distance(neighbor, pt[0][0:2]) for pt in Board.placed_tiles]
                    neighbor_other = [Hex.hex_distance(neighbor, Board.get_other_coord(pt)) for pt in Board.placed_tiles]
                    distances = distances_tile + distances_other + neighbor_tile + neighbor_other
                    if min(distances) > 1:
                        return False
                    else:
                        return True

    @staticmethod
    def is_touching(a, b):
        return Hex.hex_distance(a, b) == 1

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

    @staticmethod
    def add_arrow(a, b, c, s=1):
        Board.arrows.append((a, b, c, s))

    @staticmethod
    def draw_arrow(a, b, c, s=1):
        from_pos = Board.axial_to_screen(a)
        to_pos = Board.axial_to_screen(b)
        if c == 0:
            pg.draw.line(Board.screen, Shapes.sprite_colors[c], from_pos, to_pos, 3*s)
            pg.draw.circle(Board.screen, Shapes.sprite_colors[c], to_pos, 5*s)
        else:
            pg.draw.circle(Board.screen, Shapes.sprite_colors[c], to_pos, 3*s)

    @staticmethod
    def score_line(tile):
        Board.update_color_map()
        score_inc = [0, 0, 0, 0, 0, 0]  # prepare scoring
        t_coord = tile[0][0:2]
        tk = tile[0][2]
        tc = tile[1][0]

        for k in range(6):
            if k != tk:
                line = Board.get_line(t_coord, k)
                if len(line) > 0:
                    for s in line:
                        if tuple(s) in Board.color_map[tc]:
                            Board.add_arrow(t_coord, s, 0, 2)
                            score_inc[tc] += 1
                        else:
                            Board.add_arrow(t_coord, s, 5)
                            break
        return score_inc

    @staticmethod
    def score_tile():
        Board.arrows = []  # reset board arrows

        tile = Board.placed_tiles[len(Board.placed_tiles)-1]  # get newest tile
        tk = tile[0][2]

        q_coord = Board.get_other_coord(tile)
        qk = (tk + 3) % 6
        q_tile = ((*q_coord, qk), (tile[1][1], tile[1][0]))

        score_tile = Board.score_line(tile)
        score_q_tile = Board.score_line(q_tile)
        score_inc = [a + b for a, b in zip(score_tile, score_q_tile)]

        return score_inc

    @staticmethod
    def update_color_map():
        Board.color_map = Board.get_color_map()

    @staticmethod
    def populate_corners():
        Board.placed_tiles = []
        for c in range(6):
            corner_coord = Hex.axial_corners[c]
            corner_tile = ((*corner_coord, c), (c, c))
            Board.placed_tiles.append(corner_tile)
