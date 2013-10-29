"""Handles creation, clearing and blitting sprites on screen."""
import pygame
from game.utils import Point
COLOR_BLACK = (0, 0, 0)


class Screen(object):
    """The global screen object."""
    pygame.init()
    _screen = pygame.display.set_mode((800, 600))
    _camera = Point(0, 0)
    center = Point(800 / 2, 600 / 2)

    def clear(self):
        """Fills the screen with black"""
        self._screen.fill(COLOR_BLACK)

    def blit(self, renderable, point):
        """Draws the renderable on the screen"""
        self._screen.blit(renderable, point)

    @property
    def camera(self):
        return self._camera

    @camera.setter
    def camera(self, point):
        self._camera.x, self._camera.y = point.x, point.y


SCREEN = Screen()