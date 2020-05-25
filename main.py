# Imports, init, state variables, screen creation, colors
import pygame

# Initialize pygame and state
from board import Board
from game import Game

pygame.init()
screen = pygame.display.set_mode(Board.screen_size)
# display = pygame.display.setmode((0, 0), pygame.FULLSCREEN)
# screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Genius v0.3")
icon = pygame.image.load('genius_logo.png')
pygame.display.set_icon(icon)

# Prepare text
pygame.font.init()
Game.default_font = pygame.font.SysFont('Arial', 30)
Game.start()

# Application loop
while Game.running:
    # Event checks
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Game.running = False
        if event.type == pygame.KEYDOWN:  # continue game upon right arrow key
            if event.key == pygame.K_SPACE:
                Game.next_tile()
            elif event.key == pygame.K_RIGHT:  # press space to rotate tile
                Game.rotate_current(-1)
            elif event.key == pygame.K_LEFT:
                Game.rotate_current()
            elif event.key == pygame.K_n:
                Game.start()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[2]:  # right mouse button for undo
                Game.undo()
            elif pygame.mouse.get_pos()[0] < 800:  # press on board to play
                Game.play()

    # Draw loop
    if Game.drawing:
        Game.draw(screen)
        Game.draw_placed_tiles()
        [Board.draw_arrow(*x) for x in Board.arrows]  # if Game.debugging else False
        if Board.is_on_board(Board.get_mouse_axial()):
            Game.draw_cursor()
        Game.draw_edge()

        pygame.display.flip()
        if Game.debugging:
            Game.drawing = False

pygame.quit()
