# Imports, init, state variables, screen creation, colors
import json

# Initialize pygame and state
from board import Board
from cursor import Cursor
from game import Game
from networking import Network
from client import *


def request(n, request_string):  # returns game state
    game_json = n.send(request_string)
    game = json.loads(game_json)
    return game


# Start networking and receive Game object
n = Network()
player_id = n.get_player_id()
game_dict = request(n, "get")
game = Game(with_dict=game_dict)
running = True


# Client globals
cursor = Cursor(game.take_tile())


# Application loop
while running:
    # Get game state from the server
    game.get_state(n)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:  # continue game upon right arrow key
            if event.key == pygame.K_SPACE:
                cursor.replace(game.take_tile(0))
            elif event.key == pygame.K_RIGHT:  # press space to rotate tile
                cursor.rotate(-1)
            elif event.key == pygame.K_LEFT:
                cursor.rotate(1)
            elif event.key == pygame.K_n:
                n.send("reset")
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[2]:  # right mouse button for undo
                undo(game, cursor)
            elif pygame.mouse.get_pos()[0] < 800:  # press on board to play
                play(game, cursor)

        # Send game state to network n and update own dictionary with server state
        game.send_state(n)
        print("now to play: ", game.player_names[game.turn])

    draw(game)
    draw_cursor(cursor)
    draw_edge()

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
