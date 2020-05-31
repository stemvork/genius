class Cursor:
    def __init__(self, tile):
        self.tile = tile
        self.rot = 0

    def rotate(self, rot):
        self.rot += rot
        self.rot = self.rot % 6

    def replace(self, tile):
        self.tile = tile
        self.rot = 0

    def get_tile_rot(self):
        return self.tile, self.rot
