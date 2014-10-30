"""A generic Panda3D class that handles all windowing, lifecycle management,
and input management, then passes the relevant triggers to a game state class.

Chances are in the future that this will also provide the game state switcher.
"""
from direct.filter.CommonFilters import CommonFilters
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from panda3d import core
from .controllers import ControllerInput
from pandac.PandaModules import loadPrcFileData

# Window config
from game import gamestates

loadPrcFileData("", "window-title Test Game")
loadPrcFileData("", "win-size 1200 900")


class MainApp(ShowBase):
    def __init__(self):
        # Normal init
        super(MainApp, self).__init__()
        self.controller_input = ControllerInput()
        self.taskMgr.add(self.update, "update")
        base.setFrameRateMeter(True)
        base.disableMouse()

        # Game-specific init
        #self.state = gamestates.Title()
        self.state = gamestates.Play('level2.lev')

        # Input
        self.accept('mouse1', self.state.handle_mouse)

        # TODO: Move this to the appropriate gamestate
        self.build_lighting()

    def build_lighting(self):
        # Fog
        exp_fog = core.Fog("scene-wide-fog")
        exp_fog.setColor(0.0, 0.0, 0.0)
        exp_fog.setExpDensity(0.004)
        self.render.setFog(exp_fog)
        self.setBackgroundColor(0, 0, 0)

        # Lights
        spotlight = core.Spotlight("spotlight")
        spotlight.setColor(core.Vec4(1, 1, 1, 1))
        spotlight.setLens(core.PerspectiveLens())
        spotlight.setShadowCaster(True, 4096, 4096)
        spotlightNode = self.render.attachNewNode(spotlight)
        spotlightNode.setPos(10, 60, 50)
        spotlightNode.lookAt(5, 10, 0)
        self.render.setLight(spotlightNode)

        ambient_light = core.AmbientLight("ambientLight")
        ambient_light.setColor(core.Vec4(.25, .25, .25, 1))
        self.render.setLight(self.render.attachNewNode(ambient_light))

        # Enable the shader generator for the receiving nodes
        self.render.setShaderAuto()

        # Cool filters
        #filters = CommonFilters(base.win, base.cam)
        #filters.setBloom()
        #filters.setCartoonInk()
        #filters.setVolumetricLighting(spotlightNode, )

    def update(self, task):
        self.controller_input.update()
        dt = self.taskMgr.globalClock.getDt()

        if self.state.next:
            self.state = self.state.next
        # render
        #self.state.render(dt)

        # Update camera
        kp = self.state.level.knight.pos
        base.cam.setPos(kp.x, kp.y, 15)
        base.cam.lookAt(self.state.level.knight.model)

        return Task.cont