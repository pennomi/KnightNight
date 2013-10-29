"""Handles advanced renderables, similar to the Pygame Sprite class, but with
more flair, such as animated renderables.
"""
import pygame
from game.smithy.graphics.screen import Screen


def memoize_renderable(cls):
    """Decorator. A class factory that ensures only one of each image is loaded.
    """
    instances = {}

    def getinstance(filepath, *args, **kwargs):
        """Return or create the Renderable"""
        key = filepath
        if key not in instances:
            instances[key] = cls(filepath, *args, **kwargs)
        return instances[key]
    return getinstance


@memoize_renderable
class Renderable:
    """A basic sprite class that handles rendering an image to the screen."""
    def __init__(self, filepath, offset, ignore_cam=False, frames=1,
                 frame_duration=2):
        self._image = pygame.image.load(filepath).convert_alpha()
        self.offset = offset
        self.ignore_cam = ignore_cam
        self._screen = Screen()
        self._frames = frames
        self.frame_duration = frame_duration
        self.frame_counter = 0
        self.current_frame = 0

    def render(self, p):
        """Draw the renderable to screen at a point position."""
        # animations
        if self._frames > 1:
            self.frame_counter += 1
            if self.frame_counter > self.frame_duration:
                self.frame_counter = 0
                self.current_frame += 1
                if self.current_frame == self._frames:
                    self.current_frame = 0
        # render
        target = p - self.offset
        if not self.ignore_cam:
            target += Screen().camera
        frame_w = self._image.get_width() / self._frames
        self._screen.blit(self._image.subsurface(
            (self.current_frame * frame_w, 0,
             frame_w, self._image.get_height())), (target.x, target.y))
