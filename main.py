# Imports, init, state variables, screen creation, colors

import random

import pygame

# Initialize pygame and state
from board import Board

pygame.init()
running = True
drawing = True
debugging = False
placed_tiles = []
current_tile = (0, 0)

# Create the screen
control_width = 200
screen = pygame.display.set_mode((Board.width + control_width, Board.height))
board_center = (Board.width / 2, Board.height / 2)

# Title and icon
pygame.display.set_caption("Genius v0.1")
icon = pygame.image.load('genius_logo.png')
pygame.display.set_icon(icon)


# Hexagon params (global)
size = 25
lineWidth = 1

# Application loop
while running:
    # Event checks
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT and debugging is True:
                drawing = True
            elif event.key == pygame.K_SPACE:
                if current_tile[0] < 5 :
                    current_tile = (current_tile[0]+1, current_tile[1])
                else:
                    current_tile = (0, current_tile[1])
        if event.type == pygame.MOUSEBUTTONDOWN:
            if current_tile[1] < 5:
                current_tile = [current_tile[0], current_tile[1] + 1]
            else:
                current_tile = [current_tile[0], 0]
            if pygame.mouse.get_pos()[0] < 800:
                placed_tiles.append((Board.get_clicked(), current_tile[0], current_tile[1] - 1))
                current_tile = (0, 0)
                # TODO: get new tile

    # Draw loop
    if drawing:
        screen.fill(Board.colors[0])
        Board.draw(screen)
        if current_tile:
            args = (12, -12, current_tile[1], current_tile[0])
            Board.draw_pair(*args)
        if len(placed_tiles) > 0:
            for pt in placed_tiles:
                args = (pt[0][0], pt[0][1], pt[2], pt[1])
                Board.draw_pair(*args)
        pygame.display.flip()
        if debugging:
            drawing = False

pygame.quit()
