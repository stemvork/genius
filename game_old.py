import random
from board import Board

# TODO: move client logic to main.py or client.py
# TODO: move game variables and logic to server.py version


class Game:
    @staticmethod
    @staticmethod
    def update_turn():
        # Game.turn = ~Game.turn
        Game.turn = 0 if Game.turn else 1

    @staticmethod
    @staticmethod
    def check_end_game():
        Board.count_available()
        Board.count_available_pairs()

    # noinspection PyUnusedLocal
    @staticmethod
    def start():
        Game.running = True
        Game.drawing = True
        Game.debugging = False

        Game.turn = 0
        Game.current_tile = None
        Game.current_rot = 0

        Game.tileset = []
        Game.populate_tileset()

        Game.scores = [[0 for i in range(6)] for p in range(2)]
        # noinspection PyUnusedLocal
        Game.score_inc = [[0 for i in range(6)] for p in range(2)]
        Game.color_just_finished = [[False for i in range(6)] for p in range(2)]

        Board.blocked = set([])
        Board.arrows = []
        Board.color_map = []
        Board.populate_corners()
        Board.count_available()
        Board.count_available_pairs()
