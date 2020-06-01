# General libraries
from random import choice
import pygame
from math import sqrt, floor

# Project files
from hex import Hex
from shapes import Shapes

# Prepare text
pygame.font.init()


class Board:
    # Board sizes
    screen = None

    def __init__(self, mini=False):
        Board.blocked = set([])
        Board.arrows = []
        Board.color_map = []
        Board.overlays = []
        Board.count_available()
        Board.count_available_pairs()

        Board.width = 800
        Board.height = 800
        Board.board_size = (Board.width, Board.height)
        Board.board_center = (Board.width / 2, Board.height / 2)

        # Control sizes
        Board.control_width = 300
        Board.screen_size = (Board.width + Board.control_width, Board.height)

        # Hex sizes
        Board.size = 25
        Board.line_width = 1

        Board.mini = mini
        if mini:
            Board.width = Board.width // 2
            Board.height = Board.height // 2
            Board.board_size = tuple([x // 2 for x in list(Board.board_size)])
            Board.board_center = tuple([x // 2 for x in list(Board.board_center)])
            Board.control_width = Board.control_width // 2
            Board.screen_size = tuple([x // 2 for x in list(Board.screen_size)])
            Board.size = Board.size / 2
            # Board.line_width = 1

        # Colors
        Board.tile_color = pygame.Color('#555555')
        Board.colors = [pygame.Color(c) for c in ('#324B4B', '#D56CA5', '#69E1FA', '#5292BD', '#B3E08B', '#E25E3A')]

        # Fonts
        if mini:
            Board.default_font = pygame.font.SysFont("Arial", 30 // 2)
            Board.small_font = pygame.font.SysFont("Arial", 10 // 2)
        else:
            Board.default_font = pygame.font.SysFont("Arial", 30)
            Board.small_font = pygame.font.SysFont("Arial", 10)

    @staticmethod  # draw parent
    def draw(screen):
        Board.screen = screen
        for k in range(1 + 6):
            Board.draw_ring((0, 0), k, Board.colors[2])
        Board.draw_hexagon_axial(0, 0, Board.colors[3])

    # noinspection PyUnusedLocal
    @staticmethod  # draw control
    def draw_control(game):
        scores = game.scores
        inc = game.score_inc
        turn = game.turn
        names = game.players
        tileset_count = len(game.tileset)
        # Set convenient dimensions
        square_count = 19
        sz = floor(Board.control_width / square_count)
        sm = max(1, floor(sz / 10))
        ss = sz + sm
        sx = Board.width - ss
        sy = 3 * ss - floor(sz / 4)
        py = 10 * ss
        # (sz, sm, ss, sx, sy, py)
        control_dims = (sz, sm, ss, sx, sy, py)

        # Indicate current player with bg-color and alternate fg-color
        for p in range(2):
            current_player = p == turn
            bg_color = Board.colors[0].lerp(pygame.Color(0, 0, 0), 0.4)
            Board.draw_control_names(control_dims, names, bg_color, current_player, p)

            # Draw the actual scoring squares
            Board.draw_control_squares(control_dims, scores, inc, current_player, p)

    @staticmethod  # draw control helper
    def draw_control_names(control_dims, names, bg_color, current_player, p):
        (sz, sm, ss, sx, sy, py) = control_dims
        if current_player:
            name_color = Board.colors[2]
            pygame.draw.rect(Board.screen, bg_color, (sx - ss, sy - 3 * ss + p * py, 21 * ss, 10 * ss))
        else:
            name_color = (0, 0, 0)

        if p >= len(names):
            current_name = "Jasper"
        else:
            current_name = names[str(p)]
        name_sprite = Board.default_font.render(current_name, False, name_color)
        name_coords = (Board.screen_size[0] - ss - Board.default_font.size(current_name)[0], 8 + p * py)
        Board.screen.blit(name_sprite, name_coords)

    @staticmethod  # draw control squares and arrows and text
    def draw_control_squares(control_dims, scores, inc, current_player, p):
        (sz, sm, ss, sx, sy, py) = control_dims

        for j in range(6):
            for i in range(19):
                # Draw blank rectangles
                score_rect_dim = (sx + i * ss, sy + j * ss + p * py, sz, sz)
                score_rect_color = (100, 100, 100) if i < 10 else (170, 170, 170)
                pygame.draw.rect(Board.screen, score_rect_color, score_rect_dim)

                # Draw the score text underneath
                if j == 0:
                    score_text_dim = pygame.Rect((sx + i * ss, sy + 6 * ss + p * py, sz, sz))
                    score_text = Board.small_font.render(str(i), False, (255, 255, 255))
                    score_text_rect = score_text.get_rect(center=score_text_dim.center)
                    Board.screen.blit(score_text, score_text_rect)

            # Increments in score
            ac = Board.colors[0] if current_player else Board.colors[2]
            aw = inc[p][j] * sz
            ax = sx + sm + scores[p][j] * ss - aw
            pygame.draw.rect(Board.screen, ac, (ax, sy + sz / 2 - 2 + j * ss + p * py, aw, 4))

            # Draw the score token
            score_token_dim = (sx + scores[p][j] * ss, sy + j * ss + p * py, sz, sz)
            pygame.draw.rect(Board.screen, Shapes.sprite_colors[j], score_token_dim)

    @staticmethod  # abbreviation
    def draw_empty_hex(q, r):
        Board.draw_hexagon_axial(q, r, Board.tile_color)

    @staticmethod
    def draw_empty_tile(q, r, k=0):
        (rq, rr) = Hex.axial_directions[k]
        Board.draw_hexagon_axial(q, r, Board.tile_color)
        Board.draw_hexagon_axial(q + rq, r + rr, Board.tile_color)

    @staticmethod
    def draw_hexagon(center, s, fill_color, hex_screen=None):
        if not hex_screen:
            hex_screen = Board.screen
        pygame.draw.polygon(hex_screen, fill_color, [Hex.hex_corner(center, s, p) for p in range(6)])
        pygame.draw.polygon(hex_screen, Board.colors[0], [Hex.hex_corner(center, s, p) for p in range(6)],
                            Board.line_width)

    @staticmethod
    def draw_hexagon_axial(q, r, fill_color, hex_screen=None):
        if not hex_screen:
            hex_screen = Board.screen
        position = (Board.width / 2 + q * Board.size * 6 / 4, Board.width / 2 + (r + q / 2) * Board.size * sqrt(3))
        Board.draw_hexagon(position, Board.size, fill_color, hex_screen)

    @staticmethod
    def draw_line(s, k):
        line = Board.get_line(s, k)
        [Board.add_arrow(line[i], line[i + 1], 0) for i in range(len(line) - 1)]

    @staticmethod  # draw tile
    def draw_pair(coords, cols):
        # Draw under-layer
        (q, r, k) = coords
        (c1, c2) = cols
        Board.draw_empty_tile(q, r, k)

        # Draw coloured shapes
        primary_points = Shapes.plot_primary(Board.board_size, Board.size, q, r, c1)
        Board.draw_shape(c1, primary_points)
        (nq, nr) = Hex.hex_neighbor((q, r), k)
        secondary_points = Shapes.plot_primary(Board.board_size, Board.size, nq, nr, c2)
        Board.draw_shape(c2, secondary_points)

    @staticmethod
    def draw_overlays():
        overlay_surface = pygame.Surface(Board.screen.get_size())
        overlay_surface.set_colorkey((0, 0, 0))
        overlay_surface.set_alpha(100)
        for o in Board.overlays:
            (q, r, k) = o
            (rq, rr) = Hex.axial_directions[k]
            Board.draw_hexagon_axial(q, r, (255, 0, 0), overlay_surface)
            Board.draw_hexagon_axial(q + rq, r + rr, (255, 0, 0), overlay_surface)
        Board.screen.blit(overlay_surface, (0, 0))

    @staticmethod
    def draw_shape(shape_color, ppts):
        color1 = Shapes.get_sprite_color(shape_color)
        if shape_color in [0, 2, 4]:
            pygame.draw.polygon(Board.screen, color1, ppts)
        elif shape_color == 1:
            Board.draw_hexagon(*ppts, color1)
        elif shape_color == 3:
            pygame.draw.circle(Board.screen, color1, *ppts)
        elif shape_color == 5:
            pygame.draw.circle(Board.screen, color1, *ppts)

    @staticmethod
    def draw_ring(center, n, fill_color):
        for p in Hex.hex_ring(center, n):
            Board.draw_hexagon_axial(p[0], p[1], fill_color)

    @staticmethod
    def get_mouse_axial():
        pos = pygame.mouse.get_pos()
        q = (2. / 3 * (pos[0] - Board.width / 2)) / Board.size
        r = (-1. / 3 * (pos[0] - Board.width / 2) + sqrt(3) / 3 * (pos[1] - Board.height / 2)) / Board.size
        return Hex.hex_round((q, r))

    @staticmethod  # abbreviation
    def get_clicked_distance():
        return Board.get_distance(Board.get_mouse_axial())

    @staticmethod
    def get_color_map(game):
        color_map = []
        for i in range(6):  # loop over colors
            color_map.append(Board.get_color_coord_list(game, i))
        return color_map

    @staticmethod
    def get_color_coord_list(game, color):
        coords = []
        for pt in game.placed_tiles:
            if Board.is_on_board(pt[0][0:2]):
                if pt[1][0] == color:
                    coords.append(pt[0][0:2])
            if Board.is_on_board(Board.get_other_coord(pt)):
                if pt[1][1] == color:
                    coords.append(Board.get_other_coord(pt))
        return coords

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
        return Hex.hex_neighbor(tile[0][0:2], tile[0][2])

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
    def is_touching(a, b):
        return Hex.hex_distance(a, b) == 1

    @staticmethod
    def is_free(coord):
        # print("testing coord ", coord)
        if coord in Board.blocked:
            return False
        if not Board.is_on_board(coord):
            return False
        return True

    @staticmethod
    def is_free_pair(coord, k, free=False):
        # print("testing coord ", coord)
        if coord in Board.blocked:
            return False
        if not free and not Board.is_on_board(coord):
            return False
        neighbor = Hex.hex_neighbor(coord, k)
        # print("testing neighbor ", neighbor)
        if neighbor in Board.blocked:
            return False
        if not free and not Board.is_on_board(neighbor):
            return False
        return True

    @staticmethod
    def is_free_pair_overlay(coord, k, overlay_blocked):
        if coord in overlay_blocked:
            return False
        if not Board.is_on_board(coord):
            return False
        neighbor = Hex.hex_neighbor(coord, k)
        # print("testing neighbor ", neighbor)
        if neighbor in overlay_blocked:
            return False
        if not Board.is_on_board(neighbor):
            return False
        return True

    @staticmethod
    def update_blocked(game):
        for pt in game.placed_tiles:
            (q, r, k) = pt[0]
            coord = (q, r)
            if Board.is_on_board(coord):
                Board.blocked.add(coord)
            neigh = Hex.hex_neighbor(coord, k)
            if Board.is_on_board(neigh):
                Board.blocked.add(neigh)

    @staticmethod
    def has_neighbor(game, coord, current_rot):
        Board.update_blocked(game)
        coord_neighs = []
        for k in range(6):
            if k != current_rot:
                coord_neighs.append(Hex.hex_neighbor(coord, k))
        par_rot = (current_rot + 3) % 6
        neigh_coord = Hex.hex_neighbor(coord, current_rot)
        for k in range(6):
            if k != par_rot:
                coord_neighs.append(Hex.hex_neighbor(neigh_coord, k))
        # print(coord_neighs)
        for cn in coord_neighs:
            if cn in Board.blocked:
                return True
        return False

    @staticmethod
    def place(game, current_tile, current_rot, coord=None):
        if not coord:
            coord = Board.get_mouse_axial()
            if not Board.has_neighbor(game, coord, current_rot):
                return False
        tile = ((*coord, current_rot), current_tile)
        game.placed_tiles.append(tile)
        return True

    @staticmethod
    def random_color():
        return choice(Board.colors)

    @staticmethod
    def add_arrow(a, b, c, s=1):
        Board.arrows.append((a, b, c, s))

    @staticmethod
    def draw_arrow(a, b, c, s=1):
        if Board.mini:
            s = s / 2
        from_pos = Board.axial_to_screen(a)
        to_pos = Board.axial_to_screen(b)
        if c == 0:
            pygame.draw.line(Board.screen, Shapes.sprite_colors[c], from_pos, to_pos, 3 * s)
            pygame.draw.circle(Board.screen, Shapes.sprite_colors[c], to_pos, 5 * s)
        else:
            pygame.draw.circle(Board.screen, Shapes.sprite_colors[c], to_pos, 3 * s)

    @staticmethod
    def count_available():
        count = 0
        for q in range(-6, 7):
            for r in range(-6, 7):
                if Board.is_free((q, r)):
                    count += 1
        # print("Available (hex): ", count)
        return count

    @staticmethod
    def count_available_pairs():
        count = 0
        overlay_blocked = set(Board.blocked)
        for k in range(0, 3):
            for r in range(-6, 7):
                for q in range(-6, 7):
                    if Board.is_free_pair_overlay((q, r), k, overlay_blocked):
                        Board.overlays.append((q, r, k))
                        overlay_blocked.add((q, r))
                        overlay_blocked.add(Hex.hex_neighbor((q, r), k))
                        count += 1

        # Prevent drawing the overlays
        Board.overlays = []
        # print(f'Available pairs: {count} ({Board.count_available()})')
        return count

    @staticmethod
    def score_line(game, tile):
        Board.update_color_map(game)
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
    def score_tile(game):
        Board.arrows = []  # reset board arrows

        tile = game.placed_tiles[len(game.placed_tiles) - 1]  # get newest tile
        tk = tile[0][2]

        q_coord = Board.get_other_coord(tile)
        qk = (tk + 3) % 6
        q_tile = ((*q_coord, qk), (tile[1][1], tile[1][0]))

        score_tile = Board.score_line(game, tile)
        score_q_tile = Board.score_line(game, q_tile)
        score_inc = [a + b for a, b in zip(score_tile, score_q_tile)]

        return score_inc

    @staticmethod
    def update_color_map(game):
        Board.color_map = Board.get_color_map(game)
