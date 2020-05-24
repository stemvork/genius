import random
from board import Board


class Game:
    running = False
    drawing = False
    debugging = False

    turn = 0
    current_tile = None
    current_rot = 0

    tileset = []
    player_names = ["Jasper", "Joana"]
    scores = [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]
    score_inc = [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]

    default_font = None

    @staticmethod
    def draw(screen):
        screen.fill(Board.colors[0])
        Board.draw(screen)
        Board.draw_control(Game.default_font, Game.scores, Game.score_inc, Game.turn, Game.player_names, len(Game.tileset))

    @staticmethod
    def draw_cursor():
        Board.draw_pair((*Board.get_mouse_axial(), Game.current_rot), Game.current_tile)

    @staticmethod
    def draw_edge():
        Board.draw_ring((0, 0), 8, Board.colors[3])
        Board.draw_ring((0, 0), 7, Board.colors[3])

    @staticmethod
    def draw_placed_tiles():
        if len(Board.placed_tiles) > 0:
            for pt in Board.placed_tiles:
                Board.draw_pair(*pt)

    @staticmethod
    def next_tile():
        Game.current_tile = Game.tileset.pop(0)
        Game.current_rot = 0

    @staticmethod
    def populate_tileset():
        for c1 in range(6):
            for c2 in range(6):
                max_i = 0
                if c1 == c2:
                    max_i = 5
                elif c1 < c2:
                    max_i = 6
                for i in range(max_i):
                    Game.tileset.append((c1, c2))
        random.shuffle(Game.tileset)
        Game.next_tile()

    @staticmethod
    def play():
        if Board.place(Game.current_tile, Game.current_rot):
            score_inc = Board.score_tile()
            for i in range(6):
                Game.scores[Game.turn][i] += score_inc[i]
            Game.score_inc[Game.turn] = score_inc
            Game.update_turn()
            Game.current_tile = Board.get_next(Game.tileset)
            Game.current_rot = 0

    @staticmethod
    def rotate_current():
        if Game.current_rot < 5:
            Game.current_rot += 1
        else:
            Game.current_rot = 0

    @staticmethod
    def update_turn():
        # Game.turn = ~Game.turn
        Game.turn = 0 if Game.turn else 1

    @staticmethod
    def undo():
        if len(Board.placed_tiles) > 0:
            # TODO: undo score
            Game.tileset.insert(0, Game.current_tile)
            Game.current_tile = Board.placed_tiles.pop()[1]
            Board.blocked.pop()
            Board.blocked.pop()
            Game.current_rot = 0
            Game.update_turn()
            Board.arrows = []

