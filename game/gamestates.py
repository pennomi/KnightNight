"""Holds the logic for each of the game's states. These all inherit from a base
class.
"""
from panda3d.core import CollisionTraverser, CollisionHandlerQueue, \
    CollisionNode, GeomNode, CollisionRay
from game.renderable import Renderable
from game.screen import SCREEN
from game.utils import Point
from game.level import Level
from game.tileset import Tileset


class GameState(object):
    """Generic Base Class for all GameStates."""
    next = None

    def __init__(self):
        pass


class Play(GameState):
    """The GameState while actually playing a level."""
    def __init__(self, filepath):
        super(Play, self).__init__()
        self.filepath = filepath
        tileset = Tileset('resources/tileset/default.tset')
        self.level = Level(tileset, filepath)

        # Mouse Picking
        self.traverser = CollisionTraverser('Picker')
        base.cTrav = self.traverser
        self.collision_queue = CollisionHandlerQueue()

        picker_node = CollisionNode('mouseRay')
        picker_np = base.cam.attachNewNode(picker_node)
        picker_node.setFromCollideMask(GeomNode.getDefaultCollideMask())
        self.picker_ray = CollisionRay()
        picker_node.addSolid(self.picker_ray)
        self.traverser.addCollider(picker_np, self.collision_queue)

    def handle_mouse(self):
        # TODO: Why is this causing it to work one click behind?
        # First we check that the mouse is not outside the screen.
        if base.mouseWatcherNode.hasMouse():
            # This gives up the screen coordinates of the mouse.
            mpos = base.mouseWatcherNode.getMouse()

            # This makes the ray's origin the camera and makes the ray point
            # to the screen coordinates of the mouse.
            self.picker_ray.setFromLens(base.camNode, mpos.getX(), mpos.getY())

            # TODO: for some reason this happens on the NEXT click
            # only care about the closest hit
            self.collision_queue.sortEntries()
            if not self.collision_queue.getNumEntries():
                return

            # get collision tag
            obj = self.collision_queue.getEntry(0).getIntoNodePath()
            print(obj.getNetTag('myObjectTag'))
            self.level.tile_clicked(obj.getNetTag('myObjectTag'))


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
