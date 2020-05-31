import random
from hex import Hex


# TODO: Minimize size of dict sent over network, updates only
class Game:
    def __init__(self, server=False, new_game_id=None, with_dict=None):
        self.placed_tiles = []
        if server:
            self.id = new_game_id
            self.tileset = self.populate_tileset()
            self.populate_corners()
        else:
            self.id = -1
            self.tileset = []
        self.turn = 0
        self.scores = [[0 for i in range(6)] for p in range(2)]
        self.score_inc = [[0 for i in range(6)] for p in range(2)]
        self.player_names = ["Joana", "Jasper"]
        self.ready = False
        if with_dict:
            self.update_state(with_dict)

    def populate_corners(self):
        for c in range(6):
            corner_coord = Hex.axial_corners[c]
            self.placed_tiles.append(((*corner_coord, c), (c, c)))

    def place(self, tile):
        self.placed_tiles.append(tile)
        self.update_turn()

    def update_turn(self):
        self.turn = 1 if self.turn == 0 else 0

    @staticmethod
    def populate_tileset():
        tileset = []
        for c1 in range(6):
            for c2 in range(6):
                max_i = 0
                if c1 == c2:
                    max_i = 5
                elif c1 < c2:
                    max_i = 6
                for i in range(max_i):
                    tileset.append((c1, c2))
        random.shuffle(tileset)
        return tileset

    def take_tile(self):
        return self.tileset.pop(0)

    def update_state(self, game_dict):
        self.__dict__.update(game_dict)
