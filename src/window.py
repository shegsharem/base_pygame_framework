""" python 3.12.1 """
import pygame
from pygame.locals import *

class Window:
    """Window instance"""
    def __init__(self, screen_width:int, screen_height:int) -> None:
        """Initialize window instance

        Args:
            screen_width (int): Width of game window
            screen_height (int): Height of game window
            frame_rate (int, optional): Target framerate (FPS). Defaults to 60.
        """
        #pygame.init()
        self.width = screen_width
        self.height = screen_height

        self.screen = pygame.display.set_mode(
            (self.width,
             self.height),
             pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.NOFRAME
        )