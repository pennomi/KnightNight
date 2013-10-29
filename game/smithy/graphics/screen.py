"""Handles creation, clearing and blitting sprites on screen."""
import pygame
from game import smithy
from game.smithy.utils import Point, singleton
COLOR_BLACK = (0, 0, 0)


@singleton
class Screen():
    """The global screen object as the core object of Smithy."""
    _screen = None
    _camera = Point(0, 0)

    def __init__(self, w, h):
        """Creates a screen and inits pygame/android"""
        pygame.init()
        smithy.input.gestures.Mouse() # inits android and the mouse
        self._screen = pygame.display.set_mode((w, h))
        # save these vars for quick access later on
        self.center = Point(w / 2, h / 2)

    def clear(self):
        """Fills the screen with black"""
        self._screen.fill(COLOR_BLACK)

    def blit(self, renderable, point):
        """Draws the renderable on the screen"""
        self._screen.blit(renderable, point)

    def flip(self):
        """Handles the double buffer flip. Also handles tasks that must happen
        every frame.
        """
        pygame.display.flip()

    @property
    def camera(self):
        return self._camera

    @camera.setter
    def camera(self, point):
        self._camera.x, self._camera.y = point.x, point.y

