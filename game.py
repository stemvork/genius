import random
import json
from hex import Hex


# TODO: Minimize size of dict sent over network, updates only
class Game:
    def __init__(self, server=False, new_game_id=None, with_dict=None):
        self.placed_tiles = []
        if server:
            self.id = new_game_id
            self.populate_tileset()
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

    def populate_tileset(self):
        self.tileset = []
        for c1 in range(6):
            for c2 in range(6):
                max_i = 0
                if c1 == c2:
                    max_i = 5
                elif c1 < c2:
                    max_i = 6
                for i in range(max_i):
                    self.tileset.append((c1, c2))
        random.shuffle(self.tileset)

    def take_tile(self):
        return self.tileset.pop(0)

    def update_state(self, game_dict):
        print(game_dict)
        self.__dict__.update(game_dict)

    def get_state(self, network):
        response = network.send("get")
        self.update_state(json.loads(response))

    def send_state(self, network):
        game_json = json.dumps(self.__dict__)
        response = network.send(game_json)
        self.update_state(json.loads(response))
