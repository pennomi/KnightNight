"""Holds the logic for each of the game's states. These all inherit from a base
class.
"""
from direct.actor.Actor import Actor
from game.renderable import Renderable
from game.screen import SCREEN
from game.utils import Point
from game.level import Level
from game.tileset import Tileset, TILE_CENTER, IceTile, WallTile


class GameState(object):
    """Generic Base Class for all GameStates."""
    next = None

    def __init__(self):
        pass

    def logic(self, dt):
        """Called once a frame to handle logic."""
        raise NotImplementedError("GameState must implement method 'logic'")

    def render(self, dt):
        """Called once a frame to handle rendering."""
        raise NotImplementedError("GameState must implement method 'render'")


class Play(GameState):
    """The GameState while actually playing a level."""
    highlight = Renderable("resources/images/highlight.png", TILE_CENTER)
    win = Renderable("resources/images/cleared_screen.png",
                     Point(605/2, 455/2), ignore_cam=True)
    restart = Renderable("resources/images/restart_button.png",
                         Point(100, 0), ignore_cam=True)
    levels = Renderable("resources/images/levels_button.png",
                        Point(0, 0), ignore_cam=True)

    def __init__(self, filepath):
        super(Play, self).__init__()
        self.filepath = filepath
        tileset = Tileset('resources/tileset/default.tset')
        self.level = Level(tileset, filepath)

        # Panda Init

        # Load the level model from the tileset
        self.level_model = render.attachNewNode("Tile Supernode")
        self.level_model.setPos(0, 0, 0)

        # Load Tile Map
        # TODO: Move this stuff into the tileset and level files
        self.tile_models = []
        for y, row in enumerate(reversed(self.level._tiles)):
            for x, tile_id in enumerate(row):
                # TODO: tile instancing?
                # TODO: flatten_strong on zones
                # TODO: think of a nice data structure for this...
                #self.space.tiles.append(Tile(x, y, collision_type=int(tile_id)))
                tile_model = loader.loadModel("resources/models/SimpleTile.egg")
                tile_model.setPos(x, y, 0)
                # tile_model.setScale(1.)
                tile_model.reparentTo(self.level_model)
                self.tile_models.append(tile_model)
                # Handle Ice
                print(type(tile_id), tile_id)
                if isinstance(tile_id, WallTile):
                    tile_model.setZ(1)
                elif isinstance(tile_id, IceTile):
                    tile_model.setColorScale(0, 0, 1, 0.5)
        # Don't flatten because they move independently
        #self.level_model.flattenStrong()
        self.knight_model = Actor("resources/models/mini_knight", {
            'idle': 'resources/models/mini_knight-idle',
        })
        self.knight_model.loop('idle')
        self.knight_model.setScale(0.5)
        self.knight_model.reparentTo(self.level_model)
        self.knight_model.setPos(self.level.knight.pos.x, self.level.knight.pos.y, 0)

    def logic(self, dt):
        # if mouse.clicked:
        #     scr = SCREEN.center * 2
        #     # restart button
        #     if (scr.x - SCREEN.camera.x - mouse.pos.x <= 100 and
        #                 SCREEN.camera.y + mouse.pos.y <= 65):
        #         self.next = Play(self.filepath)
        #     # levels button
        #     elif (SCREEN.camera.x + mouse.pos.x <= 100 and
        #           SCREEN.camera.y + mouse.pos.y <= 65):
        #         self.next = LevelPicker()
        #     else:
        #         # pass the win dialogs
        #         if self.level.win():
        #             if (SCREEN.center - SCREEN.camera - mouse.pos).x > 0:
        #                 self.next = Title()
        #             else:
        #                 self.next = LevelPicker()
        #         # pass the click to the level
        #         tile = screen_to_iso(mouse.pos)
        #         self.level.tile_clicked(tile)
        self.level.knight.logic()

    def render(self, dt):
        self.level.render()
        # self.highlight.render(iso_to_screen(screen_to_iso(mouse.pos)))
        self.restart.render(Point((SCREEN.center * 2).x, 0))
        self.levels.render(Point(0, 0))
        if self.level.win():
            self.win.render(SCREEN.center)


class Title(GameState):
    """The GameState while viewing the main Title image."""
    start = Renderable("resources/images/start.png",
                       Point(605//2, 455//2), ignore_cam=True)

    def __init__(self):
        super().__init__()
        SCREEN.camera = Point(0, 0)

    def logic(self, dt):
        pass
        # if mouse.clicked:
        #     if mouse.pos.y < SCREEN.center.y:
        #         self.next = LevelPicker()
        #     else:
        #         self.next = Instructions()

    def render(self, dt):
        self.start.render(SCREEN.center)


class LevelPicker(GameState):
    """Lets you choose which level you want to play."""
    levels = Renderable("resources/images/levels_screen.png",
                        Point(605//2, 455//2), ignore_cam=True)

    def __init__(self):
        super().__init__()
        SCREEN.camera = Point(0, 0)

    def logic(self, dt):
        SCREEN.camera = Point(0, 0)
        left = Point(189, 137)
        # if mouse.clicked:
        #     normalized = mouse.pos - left
        #     if (0 < normalized.y < 66 * 5 and
        #             (0 < normalized.x < 56 or 136 < normalized.x < 136 + 56)):
        #         level = normalized.y // 66 + 1
        #         if normalized.x > 136:
        #             level += 5
        #         self.next = Play('level{n}.lev'.format(n=level))

    def render(self, dt):
        self.levels.render(SCREEN.center)


class Instructions(GameState):
    """The GameState that displays the help instructions."""
    instructions = Renderable("resources/images/instructions.png",
                              Point(605/2, 455/2), ignore_cam=True)

    def logic(self, dt):
        pass
        # if mouse.clicked:
        #     self.next = Title()

    def render(self, dt):
        self.instructions.render(SCREEN.center)
