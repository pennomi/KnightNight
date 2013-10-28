"""This module holds a simple globally accessible Camera object."""

from game.smithy.utils import Point, singleton

@singleton
class Camera(Point):
    """A singleton Camera object as a Point. When setting the camera, you MUST
    use the `set` function.
    """

    def __init__(self):
        """This is overriden so the camera is invoked without arguments. It
        can't be supered because it's using the singleton decorator.
        """
        self.x, self.y = 0, 0

    def set(self, p):
        """Sets the camera's location. It's important to use this rather than
        setting the camera manually!
        """
        self.x, self.y = p.x, p.y
