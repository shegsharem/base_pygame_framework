# python 3.12.1
import sys
import os
import pygame
from pygame.locals import *
import pygame._sdl2 as sdl2

class Game:
    """Game class"""
    pygame.init() # initialize pygame

    def __init__(self, screen_width:int, screen_height:int, frame_rate:int=60) -> None:
        """Initialize instance of game
        Args:
            screen_width (int): Width of game window
            screen_height (int): Height of game window
            frame_rate (int, optional): Target framerate (FPS) for game. Defaults to 60.
        """

        self.width = screen_width
        self.height = screen_height
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.fps = frame_rate

    def run(self) -> None:
        """Run game"""
        while 1:
            keys = pygame.key.get_pressed()

            if keys[K_ESCAPE]:
                pygame.quit()
                sys.exit()

            if pygame.event.get(pygame.QUIT):
                pygame.quit()
                sys.exit()

            self.screen.fill((10,10,10))
            pygame.display.update()
            self.clock.tick(self.fps)


if __name__ == "__main__":
    Game(640,390).run()
