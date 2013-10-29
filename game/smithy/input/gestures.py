"""An [Android|desktop]-compatible gesture recognizer layer."""
import pygame
from game.smithy.utils import Point, singleton
from game.smithy.graphics.screen import Screen
try:
    import android
except ImportError:
    android = None

MOUSE = pygame.mouse

# FUTURE: Total rewrite of this class to support many gesture types


@singleton
class Mouse:
    """Basic Input/Gesture Recognition Abstraction Class"""
    pos = Point(0, 0)
    down = False
    clicked = False
    quit = False

    def __init__(self):
        if android:
            android.init()
            android.map_key(android.KEYCODE_BACK, pygame.K_ESCAPE)

    def update(self):
        """This should be called every frame to recalculate input state."""
        andr_mouse = False

        # Android-specific:
        if android and android.check_pause():
            android.wait_for_resume()

        # check events
        for e in pygame.event.get():
            if (e.type == pygame.QUIT or
                    e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
                self.quit = True
            elif e.type == pygame.MOUSEBUTTONDOWN:
                andr_mouse = True

        # update position
        self.pos = Point(MOUSE.get_pos()[0] - Screen().camera.x,
                         MOUSE.get_pos()[1] - Screen().camera.y)

        if android:
            self.clicked = andr_mouse
        else:
            # reset click state
            self.clicked = False
            # update down and click state
            was_down = self.down
            self.down = MOUSE.get_pressed()[0] # MB1
            if not self.down and was_down:
                self.clicked = True
