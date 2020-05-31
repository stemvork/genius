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
    scores = []
    score_inc = []
    color_just_finished = []

    default_font = None
    small_font = None

    @staticmethod
    def draw(screen):
        screen.fill(Board.colors[0])
        Board.draw(screen)
        Board.draw_control(Game.default_font, Game.small_font, Game.scores, Game.score_inc,
                           Game.turn, Game.player_names, len(Game.tileset))

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
        Board.draw_overlays()

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
                if score_inc[i] >= 18 - Game.scores[Game.turn][i]:
                    Game.color_just_finished[Game.turn][i] = True
                    score_inc[i] = 18 - Game.scores[Game.turn][i]
                    # TODO: implement bonus turn function
                    # print("Give bonus for color ", i)
                Game.scores[Game.turn][i] += score_inc[i]
            Game.score_inc[Game.turn] = score_inc
            Game.update_turn()
            Game.current_tile = Board.get_next(Game.tileset)
            Game.current_rot = 0
            Game.check_end_game()
            # TODO: write check_end_game function
            # TODO: present score overview if ended

    @staticmethod
    def rotate_current(rot=1):
        if rot > 0:
            if Game.current_rot < 5:
                Game.current_rot += rot
            else:
                Game.current_rot = 0
        else:
            if Game.current_rot > 0:
                Game.current_rot += rot
            else:
                Game.current_rot = 5

    @staticmethod
    def update_turn():
        # Game.turn = ~Game.turn
        Game.turn = 0 if Game.turn else 1

    @staticmethod
    def undo():
        if len(Board.placed_tiles) > 0:
            Game.tileset.insert(0, Game.current_tile)
            Game.current_tile = Board.placed_tiles.pop()[1]
            Board.blocked.pop()
            Board.blocked.pop()
            Game.current_rot = 0
            Game.update_turn()
            for i in range(6):
                Game.scores[Game.turn][i] -= Game.score_inc[Game.turn][i]
                Game.score_inc[Game.turn][i] = 0
            Board.arrows = []

    @staticmethod
    def check_end_game():
        Board.count_available()
        Board.count_available_pairs()

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

        Game.scores = [[16 for i in range(6)] for p in range(2)]
        Game.score_inc = [[0 for i in range(6)] for p in range(2)]
        Game.color_just_finished = [[False for i in range(6)] for p in range(2)]

        Board.blocked = set([])
        Board.arrows = []
        Board.color_map = []
        Board.populate_corners()
        Board.count_available()
        Board.count_available_pairs()
