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
    screen = None

    blocked = []
    placed_tiles = []

    # Coolors.co dark slate, champagne, copper, mulberry, purple, green
    # colors = ('#324B4B', '#E1D89F', '#CD8B76', '#C45BAA', '#7D387D', '#749C75')

    def __constructor__(self):
        pass

    # @staticmethod
    # def cursor(k):
    #     mouse_pos = Board.get_clicked()
    #     neighbor_pos = Hex.hex_neighbor(mouse_pos, k)
    #     Board.cursor_axial(*mouse_pos)
    #     Board.cursor_axial(*neighbor_pos)
    #
    # @staticmethod
    # def cursor_axial(q, r):
    #     surface_rect = Board.screen.get_rect()
    #     surface_size = (surface_rect.width, surface_rect.height)
    #     mouse_surface = pygame.Surface(surface_size)
    #     mouse_surface.set_alpha(100)
    #     mouse_surface.set_colorkey(0)
    #     Board.draw_hexagon_axial(q, r, (255, 255, 255), mouse_surface)
    #     Board.screen.blit(mouse_surface, (0, 0))

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
    def draw_control(font, scores, text=True):
        if text:
            letters = ("Y", "O", "B", "G", "P", "R")
            for j in range(2):
                for i in range(6):
                    letter_sprite = font.render(letters[i] + ": ", False, Shapes.sprite_colors[i])
                    Board.screen.blit(letter_sprite, (Board.width - 50, Board.height/3 * (j+1) + 30 * i))
                    score_sprite = font.render(str(scores[j][i]), False, Shapes.sprite_colors[i])
                    Board.screen.blit(score_sprite, (Board.width, Board.height/3 * (j+1) + 30 * i))

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
    def draw_hexagon(center, s, fill_color, hex_screen=None):
        if not hex_screen:
            hex_screen = Board.screen
        pygame.draw.polygon(hex_screen, fill_color, [Hex.hex_corner(center, s, p) for p in range(6)])
        pygame.draw.polygon(hex_screen, Board.colors[0],
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
            pygame.draw.polygon(Board.screen, color1, params1)
        elif c1 == 1:
            Board.draw_hexagon(*params1, color1)
        elif c1 == 3:
            pygame.draw.circle(Board.screen, color1, *params1)
        elif c1 == 5:
            pygame.draw.circle(Board.screen, color1, *params1)
        (nq, nr) = Hex.hex_neighbor((q, r), k)
        params2 = Shapes.plot_primary(Board.board_size, Board.size, nq, nr, c2)
        color2 = Shapes.get_sprite_color(c2)
        if c2 in [0, 2, 4]:
            pygame.draw.polygon(Board.screen, color2, params2)
        elif c2 == 1:
            Board.draw_hexagon(*params2, color2)
        elif c2 == 3:
            pygame.draw.circle(Board.screen, color2, *params2)
        elif c2 == 5:
            pygame.draw.circle(Board.screen, color2, *params2)

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
    def get_clicked_distance():
        return Board.get_distance(Board.get_clicked())

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
    def place(current_tile, current_rot):
        (q, r) = Board.get_clicked()
        if Board.is_legal((q, r, current_rot)):
            tile = ((q, r, current_rot), current_tile)
            neighbor = Hex.hex_neighbor((q, r), current_rot)
            (nq, nr) = neighbor
            neighbor_tile = ((nq, nr), current_rot)
            Board.blocked.append((q, r))
            Board.blocked.append((nq, nr))

            Board.placed_tiles.append(tile)

            return True
        else:
            return False

    @staticmethod
    def random_color():
        return random.choice(Board.colors)

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
