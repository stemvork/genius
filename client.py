import pygame
import json

from networking import Network
from board import Board
from game import Game
from cursor import Cursor

# ---------------------------
# ------ START OF PHASE 0 ---
# ---------------------------
pygame.init()
# print("start of phase 0: setup window and client states.")
Board()
# set up the display
screen = pygame.display.set_mode(Board.screen_size)
pygame.display.set_caption("genius v0.5")
icon = pygame.image.load('genius_logo.png')
pygame.display.set_icon(icon)

# Set up clock for the game loop
clock = pygame.time.Clock()
FPS = 10

# TODO: move to game object for now
color_just_finished = []

# Client states
running = True


# print("End of phase 0, client running: ", running)
# ------ END OF PHASE 0 ------


# ------------------------------
# ------ START OF PHASE 1 ------
# ------------------------------
def connect_to(addr):
    return Network(addr)


# print("Start of phase 1: connecting to server, ")

# Use the networking interface to get a game state
n = connect_to("192.168.0.103")  # Server IP

# TODO: menu screen that asks for player name.

player = (n.player_id, "Jasper")
game = Game(player)
# print("End of phase 1: connected with id", player[0], " and name ", player[1], ". There are ",
#       len(game.placed_tiles), " tiles placed.")
game.update(json.loads(n.send(json.dumps(player))))
print("After updating player", game.players)


# ------ END OF PHASE 1 ------


# ------------------------------
# ------ START OF PHASE 2 ------
# ------------------------------
# Client logic functions
def get_server_state():
    global n

    response = n.send("get")
    return json.loads(response)


def process_event(events):
    global running
    global game
    global cursor
    global Board

    # If my turn, draw the cursor
    if cursor == -1:
        if int(n.player_id) == game.turn:
            cursor = Cursor(game.take_tile())

    for event in events:
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:  # continue game upon right arrow key
            if event.key == pygame.K_RIGHT:  # press space to rotate tile
                cursor.rotate(-1)
            elif event.key == pygame.K_LEFT:
                cursor.rotate(1)
            elif event.key == pygame.K_m:
                Board.mini = True if Board.mini is False else False
                Board(Board.mini)
                pygame.display.set_mode(Board.screen_size)

            elif event.key == pygame.K_n:
                n.send("reset")
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[2]:  # right mouse button for undo
                undo()
            elif pygame.mouse.get_pos()[0] < 800:  # press on board to play
                play()


def send_to_server():
    global n
    global game

    game_json = json.dumps(game.__dict__)
    response = n.send(game_json)
    return json.loads(response)


# Draw functions
def draw_placed_tiles():
    global game

    if len(game.placed_tiles) > 0:
        for pt in game.placed_tiles:
            Board.draw_pair(*pt)
    Board.draw_overlays()


def draw_edge():
    Board.draw_ring((0, 0), 8, Board.colors[3])
    Board.draw_ring((0, 0), 7, Board.colors[3])


def draw_cursor():
    global cursor
    if Board.is_on_board(Board.get_mouse_axial()):
        # noinspection PyUnresolvedReferences
        tile, rot = cursor.get_tile_rot()
        coords = (*Board.get_mouse_axial(), rot)
        cols = tile
        Board.draw_pair(coords, cols)


def draw():
    global game
    global screen
    global cursor

    screen.fill(Board.colors[0])

    Board.draw(screen)
    Board.draw_control(game)

    draw_placed_tiles()
    [Board.draw_arrow(*x) for x in Board.arrows]  # if Game.debugging else False

    if cursor != -1:
        draw_cursor()

    draw_edge()

    pygame.display.flip()
    clock.tick(FPS)


# Game logic functions
# noinspection PyUnresolvedReferences
def play():
    global game
    global cursor

    if cursor == -1:
        return False

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
        cursor = -1
        check_end_game()
        # TODO: write check_end_game function
        # TODO: present score overview if ended


def check_end_game():
    pass


def undo():
    global game
    global cursor

    if len(game.placed_tiles) > 0:
        undo_tile = game.placed_tiles.pop()[1]
        game.tileset.insert(0, undo_tile)
        cursor = Cursor(undo_tile)
        Board.blocked.pop()
        Board.blocked.pop()
        game.update_turn()
        for i in range(6):
            game.scores[game.turn][i] -= game.score_inc[game.turn][i]
            game.score_inc[game.turn][i] = 0
            Board.arrows = []


cursor = -1

while running:
    try:
        game.update(get_server_state())
    except Exception as e:
        print("updating excepted: ", e)
    process_event(pygame.event.get())
    game.update(send_to_server())
    draw()

pygame.quit()
