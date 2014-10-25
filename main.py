"""Knight Night
   A game by Thane and Stacey Brimhall
   This file is intended to be run as the main module of the program.
"""
import pygame
from game.screen import SCREEN
from game.gestures import Mouse
from game import gamestates


# TODO: ROADMAP DUE NOVEMBER 2ND
# * Clean up code
#   * Button needs _serious_ work
# * Animation Code & Art
#   * Knight idle animation
# * Sound
#   * Sound effects: win, lose, selection taps
# * New gameplay mechanics
#   * Teleporter squares?
# * Pyglet? 3D?
# * window title

def main():
    """Launches the game."""
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

if __name__ == "__main__":
    main()
