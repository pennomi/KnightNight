"""
Knight Night
A game by Thane and Stacey Brimhall
This file is intended to be run as the main module of the program.
"""
import pygame
from panda_utils.app import MainApp


def main():
    """Launches the game."""
    # pygame.mixer.music.load('resources/audio/caketown.mp3')
    # pygame.mixer.music.play(-1)  # play forever

    # INIT GAME OBJECTS
    # mouse = Mouse()

    app = MainApp()
    app.run()

    # clock = pygame.time.Clock()

    # MAIN LOOP
    # while True:
    #     # input
    #     mouse.update(SCREEN)
    #     # logic
    #     state.logic(mouse)
    #     if state.next:
    #         state = state.next
    #     # render
    #     SCREEN.clear()
    #     state.render(mouse)
    #     pygame.display.flip()
    #     # wait
    #     clock.tick(30)

if __name__ == "__main__":
    main()
