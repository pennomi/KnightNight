"""This module holds all the classes that deal with the level."""

from copy import copy
import weakref

from game.utils import Point
from game.renderable import Renderable
from game.screen import SCREEN
from game.tileset import iso_to_screen


TILE_STEPS = 5


class Knight:
    """Contains the Knight entity that moves around to complete the puzzle.
    """
    # _ne = Renderable("resources/images/knight_ne.png", Point(64, 110), frames=8)
    # _se = Renderable("resources/images/knight_se.png", Point(64, 110), frames=8)
    # _nw = Renderable("resources/images/knight_nw.png", Point(64, 110), frames=8)
    # _sw = Renderable("resources/images/knight_sw.png", Point(64, 110), frames=8)
    # _renderable = _ne
    prev = Point(0, 0)
    target = Point(0, 0)
    move_counter = 0

    def __init__(self, level, start_point):
        self.level = weakref.ref(level)
        self.pos = start_point
        self.target = start_point
        level._tiles[self.target.x][self.target.y].on_enter(self)

    def move(self, point):
        point = point.round()
        # perform the move
        level = self.level()
        if not self.move_counter and level.is_legal(point):
            self.prev = self.pos.round()
            level._tiles[self.prev.x][self.prev.y].on_leave()
            self.target = point.round()
            self.move_counter = TILE_STEPS
            # reset animation direction
            vector = self.target - self.prev
            # if vector.x == 1:
            #     self._renderable = self._sw
            # elif vector.x == -1:
            #     self._renderable = self._ne
            # elif vector.y == 1:
            #     self._renderable = self._se
            # elif vector.y == -1:
            #     self._renderable = self._nw

    def slide(self):
        self.move(self.pos + (self.pos - self.prev))

    def teleport(self, target):
        # TODO: Animate
        self.pos = target
        self.target = target

    def logic(self):
        if self.move_counter:
            self.move_counter -= 1
            self.pos += ((self.target - self.prev) * (1.0 / TILE_STEPS))
            if not self.move_counter:
                self.level()._tiles[self.target.x][self.target.y].on_enter(self)
        pos = iso_to_screen(self.pos)
        SCREEN.camera = SCREEN.center - pos


class Level:
    """This stores the level data, such as Tileset, Tiles, and Renderable
    Entities. It also checks to see if the player has won or lost."""

    def __init__(self, tileset, filename):
        # tileset
        self.tileset = tileset
        # layer data
        with open('resources/levels/' + filename) as f:
            lines = f.readlines()
        self._tiles = [[copy(self.tileset[int(tile)])
                        for tile in row.strip(' \r\n,').split(',')]
                       for row in lines]
        # find start point
        for i, row in enumerate(lines):
            for j, tile in enumerate(row.strip(' \r\n,').split(',')):
                if tile == '0':
                    start_point = Point(i, j)
        # player
        self.knight = Knight(self, start_point)
        SCREEN.camera = SCREEN.center - iso_to_screen(start_point)

    def tile_clicked(self, tile):
        """The logic that handles what happens when a tile is clicked."""
        self.knight.move(tile)

    def is_legal(self, point):
        """True if the tile at point is possible for the knight to move into.
        """
        p = point.round()
        try:
            return (abs(p.x - self.knight.target.x) +
                    abs(p.y - self.knight.target.y) == 1 and
                    self._tiles[p.x][p.y].walkable)
        except IndexError:
            return False

    def win(self):
        """True if the knight has successfully completed the puzzle."""
        if self.knight.move_counter:
            return False
        # TODO: change this to an all(generator)
        for row in self._tiles:
            for tile in row:
                if tile.prevents_win:
                    return False
        return True
    #
    # def render(self):
    #     """Render the whole array of tiles and entities."""
    #     for i, row in enumerate(self._tiles):
    #         for j, tile in enumerate(row):
    #             tile.render(iso_to_screen(Point(i, j)))
    #             if self.knight.pos.round() == Point(i, j):
    #                 self.knight.render()
