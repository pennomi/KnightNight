"""An [Android|desktop]-compatible gesture recognizer layer."""
import sys
import pygame
from game.utils import Point


class Mouse(object):
    """Basic Input/Gesture Recognition Abstraction Class"""
    pos = Point(0, 0)
    down = False
    clicked = False

    def update(self, screen):
        """This should be called every frame to recalculate input state."""

        # check events
        for e in pygame.event.get():
            if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and
                                         e.key == pygame.K_ESCAPE):
                sys.exit()

        # update position
        m = Point(pygame.mouse.get_pos())
        self.pos = m - screen.camera

        # reset click state
        self.clicked = False
        # update down and click state
        was_down = self.down
        self.down = pygame.mouse.get_pressed()[0]  # MB1
        if not self.down and was_down:
            self.clicked = True
