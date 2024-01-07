# python 3.12.1
import sys
import os
import pygame
from pygame.locals import *
from random import randint

def clip(surface:pygame.Surface, x:int, y:int, width:int, height:int) -> pygame.Surface:
    """Clipping function for pygame surfaces

    Args:
        surface (pygame.Surface): Surface to clip from
        x (int): x-position of clip
        y (int): y-position of clip
        width (int): width of clip
        height (int): height of clip

    Returns:
        pygame.Surface: New clipped surface
    """
    surface_copy = surface.copy()
    surface_copy.set_clip(pygame.Rect(x,y,width,height))
    return surface.subsurface(surface_copy.get_clip()).copy()


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


class Font:
    """Custom font generator from a png image"""
    def __init__(self, font_path:str) -> None:
        self.character_spacing = 1
        current_character_width = 0
        character_clip_count = 0
        font_image = pygame.image.load(font_path).convert_alpha()
        self.characters = {}

        self.character_map = [
            "A","B","C","D","E","F","G","H","I",
            "J","K","L","M","N","O","P","Q","R",
            "S","T","U","V","W","X","Y","Z","a",
            "b","c","d","e","f","g","h","i","j",
            "k","l","m","n","o","p","q","r","s",
            "t","u","v","w","x","y","z","1","2",
            "3","4","5","6","7","8","9","0","?",
            "/","!",".",",",":",";","\"","(",")",
            "[","]","<",">","-","+","=","%","@",
            "#","_","$","'","&","*"
        ]

        for pixel in range(font_image.get_width()):
            pixel_color = font_image.get_at((pixel,0)) # Returns color of pixel
            if pixel_color == (255,0,0):
                clipped_character_image = clip(font_image, (pixel - current_character_width), 0,
                                               current_character_width, font_image.get_height())
                self.characters[self.character_map[character_clip_count]] = clipped_character_image
                character_clip_count += 1
                current_character_width = 0
            else:
                current_character_width += 1
        
        self.character_space_width = self.characters["A"].get_width()

    def render(self, surface:pygame.Surface, text:str, location:tuple=(0,0)) -> None:
        """Renders text onto pygame surface using loaded font

        Args:
            surface (pygame.Surface): Surface to render text onto
            text (str): Text to render
            location (tuple, optional): Location on surface to render text (x,y). Defaults to (0,0).
            size_factor (int, optional): Text size multiplier. Defaults to 1.
        """
        x_offset = 0

        for character in text:
            if character != " ":
                surface.blit(self.characters[character],(location[0] + x_offset, location[1]))
                x_offset += self.characters[character].get_width() + self.character_spacing
            else:
                x_offset += self.character_space_width - self.character_spacing*2


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
        
        font = Font("font.png")
        menu = Menu(self.width/2-200,self.height-200)
        menu.center_window((self.width, self.height))
        menu.fill((randint(0,255),randint(0,255),randint(0,255)),menu.get_rect())
        button = Button(menu.get_width()//2-50,menu.get_height()//2-50,100,100)
        font.render(menu,"Hello Kennedy",location=(20,20))

        while 1:
            keys = pygame.key.get_pressed()
            self.screen.fill((255,255,255))

            if keys[K_ESCAPE]:
                menu.blit(button, button.rect)
            self.screen.blit(menu, menu.get_rect())


            if pygame.event.get(pygame.QUIT):
                pygame.quit()
                sys.exit()

            
            pygame.display.update()
            self.clock.tick(self.fps)


if __name__ == "__main__":
    Game(640,390).run()