import pygame
from board import Board

pygame.init()
screen = pygame.display.set_mode(Board.screen_size)
# display = pygame.display.setmode((0, 0), pygame.FULLSCREEN)
# screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Genius v0.5")
icon = pygame.image.load('genius_logo.png')
pygame.display.set_icon(icon)
clock = pygame.time.Clock()
FPS = 10

color_just_finished = []

# Prepare text
pygame.font.init()
default_font = pygame.font.SysFont("Arial", 30)
small_font = pygame.font.SysFont("Arial", 10)


def draw(game):
    screen.fill(Board.colors[0])
    Board.draw(screen)
    Board.draw_control(default_font, small_font, game.scores, game.score_inc,
                       game.turn, game.player_names, len(game.tileset))

    draw_placed_tiles(game)
    [Board.draw_arrow(*x) for x in Board.arrows]  # if Game.debugging else False


def draw_cursor(cursor):
    if Board.is_on_board(Board.get_mouse_axial()):
        tile, rot = cursor.get_tile_rot()
        coords = (*Board.get_mouse_axial(), rot)
        cols = tile
        Board.draw_pair(coords, cols)


def draw_edge():
    Board.draw_ring((0, 0), 8, Board.colors[3])
    Board.draw_ring((0, 0), 7, Board.colors[3])


def draw_placed_tiles(game):
    if len(game.placed_tiles) > 0:
        for pt in game.placed_tiles:
            Board.draw_pair(*pt)
    Board.draw_overlays()


def undo(game, cursor):
    if len(Board.placed_tiles) > 0:
        game.tileset.insert(0, cursor.tile)
        cursor.replace(Board.placed_tiles.pop()[1])
        Board.blocked.pop()
        Board.blocked.pop()
        cursor.set_rot(0)
        game.update_turn()
        for i in range(6):
            game.scores[game.turn][i] -= game.score_inc[game.turn][i]
            game.score_inc[game.turn][i] = 0
        Board.arrows = []


def play(game, cursor):
    if Board.place(game, *cursor.get_tile_rot()):
        score_inc = Board.score_tile(game)
        for i in range(6):
            if score_inc[i] >= 18 - game.scores[game.turn][i]:
                color_just_finished[game.turn][i] = True
                score_inc[i] = 18 - game.scores[game.turn][i]
                # TODO: implement bonus turn function
                # print("Give bonus for color ", i)
            game.scores[game.turn][i] += score_inc[i]
        game.score_inc[game.turn] = score_inc
        game.update_turn()
        cursor.replace(game.take_tile())
        check_end_game()
        # TODO: write check_end_game function
        # TODO: present score overview if ended


def check_end_game():
    pass
