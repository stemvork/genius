import random
from hex import Hex


# TODO: Minimize size of dict sent over network, updates only
class Game:
    # TODO: Rewrite constructor of Game()
    # None --> If server logic, populate the game state
    # None --> If client logic, do not populate, game state will be requested
    # NB: Client does add the player to the dict.
    def __init__(self, player=None, new_game_id=None, player_num=2, server=False):
        self.id = -1
        self.placed_tiles = []
        self.tileset = []
        self.scores = []
        self.score_inc = []
        self.turn = 0
        self.players = {}
        self.ready = False
        if server:
            self.id = new_game_id
            self.tileset = self.populate_tileset()
            self.populate_corners()
            self.scores = []
            for p in range(player_num):
                self.scores.append([0] * 6)
            self.score_inc = []
            for p in range(player_num):
                self.score_inc.append([0] * 6)
        else:
            if player:
                self.players[player[0]] = player[1]

    def populate_corners(self):
        for c in range(6):
            corner_coord = Hex.axial_corners[c]
            self.placed_tiles.append(((*corner_coord, c), (c, c)))

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

    def update(self, state):
        self.__dict__.update(state)
