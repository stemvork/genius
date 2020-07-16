# Imports, init, state variables, screen creation, colors
import json

# Initialize pygame and state
from board import Board
from cursor import Cursor
from game import Game
from client import *
from networking import Network


# TODO: Can merge with master if
# both networked or single player work
# from the same main.py file
# for example with a menu

# Start networking and receive Game object
player_id = 0
game = Game()
game.populate_tileset()
game.populate_corners()
running = True
print(game.tileset)


# Client globals
cursor = Cursor(game.take_tile())


# Application loop
while running:
    # Get game state from the server
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
                game = Game()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[2]:  # right mouse button for undo
                undo(game, cursor)
            elif pygame.mouse.get_pos()[0] < 800:  # press on board to play
                play(game, cursor)

        # Send game state to network n and update own dictionary with server state
        print("now to play: ", game.player_names[game.turn])

    draw(game)
    draw_cursor(cursor)
    draw_edge()

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
