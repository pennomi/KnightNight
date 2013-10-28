"""This module holds the Tile and Tileset classes, as well as utility methods
iso_to_screen and screen_to_iso"""

import json
from game.smithy.utils import Point
from game.smithy.graphics.renderable import Renderable
from game.smithy.graphics.screen import Screen
from random import randint

TILE_WIDTH = 128
TILE_HEIGHT = 64
TILE_CENTER = Point(TILE_WIDTH/2, TILE_HEIGHT/2)

# constants for quickly calculating screen_to_iso
TILE_AREA = TILE_HEIGHT * TILE_WIDTH
S2I_CONST_X = -Screen().center.y * TILE_WIDTH + Screen().center.x * TILE_HEIGHT
S2I_CONST_Y = -Screen().center.y * TILE_WIDTH - Screen().center.x * TILE_HEIGHT


def screen_to_iso(p):
    """Converts a screen point (px) into a level point (tile)"""
    # the "y + TILE_HEIGHT/2" is because we anchor tiles by center, not bottom
    p = Point(p.x * TILE_HEIGHT, (p.y + TILE_HEIGHT/2) * TILE_WIDTH)
    return Point(int((p.y - p.x + S2I_CONST_X) / TILE_AREA),
                 int((p.y + p.x + S2I_CONST_Y) / TILE_AREA))


def iso_to_screen(p):
    """Converts a level point (tile) into a screen point (px)"""
    return Screen().center + Point((p.y - p.x) * TILE_WIDTH / 2,
                                   (p.y + p.x) * TILE_HEIGHT / 2)


class Tile(object):
    """One tile in a tileset. Contains collision information and triggers
    for level events."""
    _sprite = None
    walkable = True
    prevents_win = False

    def __init__(self, renderable):
        self._sprite = renderable

    def on_enter(self, knight):
        """Trigger that is called when the Tile is entered."""
        pass

    def on_leave(self):
        """Trigger that is called when the Tile is exited."""
        pass

    def render(self, point):
        """Render the tile at the given point (screen coordinates)"""
        self._sprite.render(point)


class WallTile(Tile):
    """A Tile that can't be walked through."""
    walkable = False


class IceTile(Tile):
    """A Tile that makes you slide through it."""

    def on_enter(self, knight):
        super(IceTile, self).on_enter(knight)
        knight.slide()


class FloorTile(Tile):
    """A Tile that must be walked through exactly ONCE to win the game."""
    walkable = True
    prevents_win = True
    fall_pos = -1
    vibrate_counter = -1
    vibrate_amount = 3

    def __init__(self, renderable, walked_renderable=None):
        super(FloorTile, self).__init__(renderable)
        self._alternate = Renderable('resources/images/' +
                                     walked_renderable, self._sprite.offset)

    def on_enter(self, knight):
        super(FloorTile, self).on_enter(knight)
        self.walkable = False
        self.prevents_win = False

    def on_leave(self):
        super(FloorTile, self).on_leave()
        self.vibrate_counter = 0

    def render(self, point):
        v = self.vibrate_amount
        if 0 <= self.vibrate_counter <= 10:
            self.vibrate_counter += 1
            point += Point(0 + randint(-2*v, 2*v), self.fall_pos + randint(-v, v))
            if self.vibrate_counter == 10:
                self.fall_pos = 0
        if 0 <= self.fall_pos <= 100:
            self.fall_pos += 5
            point += Point(0 + randint(-2*v, 2*v), self.fall_pos + randint(-v, v))
        if self.fall_pos == 100:
            self._sprite = self._alternate
        super(FloorTile, self).render(point)


class Tileset:
    """The Tileset class is responsible for managing a collection of Renderable
    Tile objects by id.
    """
    _tiles = []

    def __init__(self, filename):
        with open(filename) as f:
            data = json.loads(f.read())
        for tile in data:
            offset = Point(tile['offset'])
            r = Renderable('resources/images/' + tile['file'], offset)
            cls = globals()[tile['class']]
            kwargs = tile.get('kwargs', {})
            self._tiles.append(cls(r, **kwargs))

    def __getitem__(self, i):
        return self._tiles[i]
