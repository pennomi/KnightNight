"""Knight Night
   A game by Thane and Stacey Brimhall
   This file is intended to be run as the main module of the program.
"""
# for py2exe
try:
    import pygame._view
except ImportError:
    pass
# the standard program
import sys

import pygame

from game.screen import SCREEN
from game.gestures import Mouse
from game import gamestates


# TODO: ROADMAP DUE NOVEMBER 2ND
# * Clean up code
#   * Levels should be entirely loaded from JSON
#   * Font rendered FPS and averaged over last second
#   * Button needs _serious_ work
# * Animation Code
#   * Knight idle animation
# * Sound
#   * Sound effects: walk, win, lose, selection taps
# * New gameplay mechanic
#   * Teleporter squares?
# * Remove Android? (Probably)
# * cx_freeze packaging instead of py2exe
# * Pyglet? 3D?
# * Remove smithy; maybe pluggable pygame/pyglet backends.


def main():
    """The main game loop. This should be automatically called on Android, and
    called by running the module on all other systems.
    """
    pygame.mixer.music.load('resources/audio/caketown.mp3')
    pygame.mixer.music.play(-1)  # play forever

    # INIT GAME OBJECTS
    mouse = Mouse()
    state = gamestates.Title()
    clock = pygame.time.Clock()

    # MAIN LOOP
    while True:
        # input
        mouse.update(SCREEN)
        if mouse.quit:
            sys.exit()
        # logic
        state.logic(mouse)
        if state.next:
            state = state.next
        # render
        SCREEN.clear()
        state.render(mouse)
        pygame.display.flip()
        # wait
        clock.tick(30)

# This isn't run on Android.
if __name__ == "__main__":
    main()
