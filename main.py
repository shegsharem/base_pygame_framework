# python 3.12.1
import sys
import os
import pygame
from pygame.locals import *
from random import randint
import time

def swap_color(surface:pygame.Surface, old_color:pygame.Color,
               new_color:pygame.Color) -> pygame.Surface:
    """Takes a pygame surface and swaps a new color with an old color

    Args:
        surface (pygame.Surface): The target surface
        old_color (pygame.Color): The old color
        new_color (pygame.Color): The color to replace the old color

    Returns:
        pygame.Surface: The original surface with swapped colors
    """
    surface_copy = pygame.Surface(surface.get_size())
    surface_copy.fill(new_color)
    surface.set_colorkey(old_color)
    surface_copy.blit(surface, (0,0))
    return surface_copy

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
        self.x = x
        self.y = y
        self.rect = self.get_rect().move(x,y)

    def button_text(self, message:str) -> None:
        """Display text on button

        Args:
            message (str): text
        """
        text = Font('font.png')
        new_rect = text.render(self,message,(self.x,self.y))
        self.rect = new_rect


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

        self.character_space_width = self.characters["!"].get_width()*2.7

    def render(self, surface:pygame.Surface, text:str, location:tuple=(0,0)) -> pygame.Rect:
        """Renders text onto pygame surface using loaded font

        Args:
            surface (pygame.Surface): Surface to render text onto
            text (str): Text to render
            location (tuple, optional): Location on surface to render text (x,y). Defaults to (0,0).
            size_factor (int, optional): Text size multiplier. Defaults to 1.
        
        Returns:
            (pygame.Rect): The rect occupied by text on the surface
        """
        x_offset = 0

        text_surface_list = []
        surface_copy = surface.copy().convert_alpha()
        text_rect = (0,0,0,0)

        for character in text:
            if character != " ":
                text_surface_list.append((self.characters[character],(location[0] + x_offset, location[1])))

                self.character_spacing = self.characters[character].get_width()
                x_offset += round(self.characters[character].get_width()+1)
                text_rect = pygame.Rect(location[0],
                         location[1],
                         text_rect[2]+self.characters[character].get_rect().width,
                         text_rect[3]+self.characters[character].get_rect().height)
            else:
                x_offset += self.character_spacing - 1
            
        surface_copy.blits(text_surface_list)
        surface.blit(surface_copy,location)

        return text_rect


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
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.NOFRAME)
        self.clock = pygame.time.Clock()
        self.fps = frame_rate

    def run(self) -> None:
        """Run game"""

        button = Button(1,1,108,20)

        menu = Menu(button.get_width()+2,button.get_height()+2)
        menu.center_window((self.width, self.height))
        menu.fill((100,100,100),menu.get_rect())

        button.fill((230,230,230))
        button.button_text("MAIN MENU")
        button_rescaled = pygame.transform.scale_by(button,2)
        

        while 1:
            keys = pygame.key.get_pressed()
            self.screen.fill((255,255,255))

            

            if keys[K_ESCAPE]:
                pygame.quit()
                sys.exit()

            menu.blit(button_rescaled, button_rescaled.get_rect())
            
            
            self.screen.blit(menu, menu.rect)
            


            if pygame.event.get(pygame.QUIT):
                pygame.quit()
                sys.exit()

            
            pygame.display.update()
            self.clock.tick(self.fps)


if __name__ == "__main__":
    Game(640,390).run()