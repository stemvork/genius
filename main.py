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

# Create the screen
control_width = 200
screen = pygame.display.set_mode((Board.width + control_width, Board.height))
board_center = (Board.width / 2, Board.height / 2)

# Title and icon
pygame.display.set_caption("Genius v0.1")
icon = pygame.image.load('genius_logo.png')
pygame.display.set_icon(icon)

# Prepare text
pygame.font.init()
default_font = pygame.font.SysFont('Arial', 30)

# Hexagon params (global)
size = 25
lineWidth = 1

# Tileset and shuffle
tileset = []
for c1 in range(6):
    for c2 in range(6):
        if c1 == c2:
            [tileset.append((c1, c2)) for i in range(5)]
        elif c1 < c2:
            [tileset.append((c1, c2)) for i in range(6)]
random.shuffle(tileset)

# State variables
current_tile = Board.get_next(tileset)
current_rot = 0
last_distance = 2

turn = 0
scores = [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]


def undo():
    if len(Board.placed_tiles) > 0:
        global current_tile
        tileset.insert(0, current_tile)
        current_tile = Board.placed_tiles.pop()[1]
        Board.blocked.pop()
        Board.blocked.pop()
        current_rot = 0


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
                # current_tile = Board.get_next(tileset)
                if current_rot < 5:
                    current_rot += 1
                else:
                    current_rot = 0
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[2]:
                undo()
            elif pygame.mouse.get_pos()[0] < 800:
                last_distance = Board.get_clicked_distance()
                if Board.place(current_tile, current_rot):
                    score_inc = Board.score(turn)
                    for i, s in score_inc:
                        scores[turn][i] += s
                    turn = ~turn
                    current_tile = Board.get_next(tileset)
                    current_rot = 0

    # Draw loop
    if drawing:
        screen.fill(Board.colors[0])
        Board.draw(screen)
        Board.draw_control(default_font, scores)
        if current_tile:
            args = ((12, -12, current_rot), current_tile)
            Board.draw_pair(*args)
        if len(Board.placed_tiles) > 0:
            for pt in Board.placed_tiles:
                Board.draw_pair(*pt)

        # Preview placement
        Board.draw_pair((*Board.get_clicked(), current_rot), current_tile)
        # Draw the distance to clicked hex
        # distance_text = default_font.render(str(last_distance), False, (255, 255, 255))
        # screen.blit(distance_text, (Board.width + 50, Board.height / 2))
        pygame.display.flip()
        if debugging:
            drawing = False

pygame.quit()
