# python 3.12.1
import sys
import os
import pygame
from pygame.locals import *
from random import randint

class Menu(pygame.Surface):
    """Game menu"""
    def __init__(self, menu_width:int, menu_height:int) -> None:
        super().__init__((menu_width, menu_height))
        self.rect = self.get_rect()
    
    def center_window(self, screen_resolution:tuple) -> None:
        """Move menu rect to center of screen

        Args:
            screen_resolution (tuple): Size of game window
        """
        center_x = screen_resolution[0] // 2
        center_y = screen_resolution[1] // 2
        self.rect = (center_x - self.rect.centerx, center_y - self.rect.centery)

class Button(pygame.Surface):
    """Button class"""
    def __init__(self, x:int, y:int, width:int, height:int) -> None:
        """Create button rect

        Args:
            x (int): x-position
            y (int): y-position
            width (int): button width
            height (int): button height
        """
        super().__init__((width,height))
        self.rect = self.get_rect().move(x,y)


class Game:
    """Game class"""
    pygame.init() # initialize pygame

    def __init__(self, screen_width:int, screen_height:int, frame_rate:int=60) -> None:
        """Initialize instance of game

        Args:
            screen_width (int): Width of game window
            screen_height (int): Height of game window
            frame_rate (int, optional): Target framerate (FPS). Defaults to 60.
        """
        self.width = screen_width
        self.height = screen_height
        self.screen = pygame.display.set_mode((self.width, self.height))#, pygame.NOFRAME)
        self.clock = pygame.time.Clock()
        self.fps = frame_rate

    def run(self) -> None:
        """Run game"""
        self.screen.fill((10,10,10))
        menu = Menu(self.width/2-100,self.height-100)
        menu.center_window((self.width, self.height))
        menu.fill((randint(0,255),randint(0,255),randint(0,255)),menu.get_rect())
        button = Button(menu.get_width()//2-50,menu.get_height()//2-50,100,100)

        while 1:
            keys = pygame.key.get_pressed()

            if keys[K_ESCAPE]:
                menu.blit(button, button.rect)
                self.screen.blit(menu, menu.rect)


            if pygame.event.get(pygame.QUIT):
                pygame.quit()
                sys.exit()

            
            pygame.display.update()
            self.clock.tick(self.fps)


if __name__ == "__main__":
    Game(640,390).run()