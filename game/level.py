"""This module holds all the classes that deal with the level."""

from copy import copy
import weakref
from direct.actor.Actor import Actor
from panda3d.core import CollisionTraverser, CollisionHandlerQueue, \
    CollisionNode, GeomNode, CollisionRay

from game.utils import Point
from game.screen import SCREEN
from game.tileset import iso_to_screen, WallTile, IceTile


TILE_STEPS = 5


class Knight:
    """The player's avatar, which moves around to complete the puzzle.
    """
    prev = Point(0, 0)
    move_counter = 0

    def __init__(self, level, start_point):
        self.level = weakref.proxy(level)
        self.pos = start_point

        self.level._tiles[self.pos.x][self.pos.y].on_enter(self)

        self.model = Actor("resources/models/mini_knight", {
            'idle': 'resources/models/mini_knight-idle',
        })
        self.model.loop('idle')
        self.model.setScale(0.5)
        self.model.reparentTo(self.level.model)
        self.model.setPos(self.pos.x, self.pos.y, 0)

    def move(self, point):
        # perform the move
        if self.level.is_legal(point):
            self.prev = self.pos.round()
            self.level._tiles[self.prev.x][self.prev.y].on_leave()
            self.pos = point.round()
            self.model.setPos(self.pos.x, self.pos.y, 0)
            self.level._tiles[self.pos.x][self.pos.y].on_enter(self)

    def slide(self):
        self.move(self.pos + (self.pos - self.prev))

    def teleport(self, target):
        # TODO: Animate
        self.pos = target
        self.model.setPos(self.pos.x, self.pos.y, 0)


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


        # Panda Stuff
        # Load the level model from the tileset
        self.model = render.attachNewNode("Tile Supernode")
        self.model.setPos(0, 0, 0)

        # Load Tile Map
        # TODO: Move this stuff into the tileset and level files
        for x, row in enumerate(self._tiles):
            for y, tile in enumerate(row):
                # TODO: tile instancing?
                # TODO: flatten_strong on zones
                # TODO: think of a nice data structure for this...
                print(tile)

                tile.model = loader.loadModel("resources/models/SimpleTile.egg")
                tile.model.setPos(x, y, 0)

                # Cheating, but whatever
                tile.model.setTag('myObjectTag', str(x*100 + y))

                # tile.model.setScale(1.)
                tile.model.reparentTo(self.model)

                # Handle Walls and Ice
                if isinstance(tile, WallTile):
                    tile.model.setZ(1)
                elif isinstance(tile, IceTile):
                    tile.model.setColorScale(0, 0, 1, 0.5)
        # Don't flatten because they move independently
        #self.model.flattenStrong()

        # Initialize the player
        self.knight = Knight(self, start_point)
        SCREEN.camera = SCREEN.center - iso_to_screen(start_point)

    def tile_clicked(self, coordinates):
        """The logic that handles what happens when a tile is clicked."""
        try:
            coordinates = int(coordinates)
            coordinates = Point(coordinates // 100,
                                coordinates - coordinates // 100 * 100)
            self.knight.move(coordinates)
        except ValueError:
            print("What you clicked on wasn't a tile.")

    def is_legal(self, point):
        """True if the tile at point is possible for the knight to move into.
        """
        p = point.round()
        try:
            return (abs(p.x - self.knight.pos.x) +
                    abs(p.y - self.knight.pos.y) == 1 and
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

    def update(self, dt):
        for row in self._tiles:
            for tile in row:
                tile.update(dt)