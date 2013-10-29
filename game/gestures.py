"""An [Android|desktop]-compatible gesture recognizer layer."""
import pygame
from game.utils import Point

MOUSE = pygame.mouse

# FUTURE: Total rewrite of this class to support many gesture types


class Mouse(object):
    """Basic Input/Gesture Recognition Abstraction Class"""
    pos = Point(0, 0)
    down = False
    clicked = False
    quit = False

    def update(self, screen):
        """This should be called every frame to recalculate input state."""

        # check events
        for e in pygame.event.get():
            if (e.type == pygame.QUIT or
                    e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
                self.quit = True

        # update position
        self.pos = Point(MOUSE.get_pos()[0] - screen.camera.x,
                         MOUSE.get_pos()[1] - screen.camera.y)

        # reset click state
        self.clicked = False
        # update down and click state
        was_down = self.down
        self.down = MOUSE.get_pressed()[0]  # MB1
        if not self.down and was_down:
            self.clicked = True
