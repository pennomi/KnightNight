"""Knight Night
   A game by Thane and Stacey Brimhall
   This file is intended to be run as the main module of the program.
"""
# this is for py2exe
try:
    import pygame._view
except ImportError:
    pass
# the standard program
import sys
from game.smithy.graphics.screen import Screen
from game.smithy.input.gestures import Mouse
import pygame

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
# * cx_freeze packaging
# * Pyglet? 3D?


def main():
    """The main game loop. This should be automatically called on Android, and
    called by running the module on all other systems.
    """
    screen = Screen(800, 600)
    mouse = Mouse()
    pygame.mixer.music.load('resources/audio/caketown.mp3')
    pygame.mixer.music.play(-1)

    # INIT GAME OBJECTS
    # TODO: restructure so this imports at the top. Maybe use pyglet instead?
    from game.game import gamestates
    state = gamestates.Title()

    clock = pygame.time.Clock()

    # MAIN LOOP
    while True:
        # input
        mouse.update()
        if mouse.quit:
            sys.exit()
        # logic
        state.logic()
        if state.next:
            state = state.next
        # render
        screen.clear()
        state.render()
        screen.flip()

        clock.tick(30)

# This isn't run on Android.
if __name__ == "__main__":
    main()
