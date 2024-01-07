# python 3.12.1
import sys
import pygame
from pygame.locals import *
from random import randint

class Button(pygame.Surface):
    """Button class"""
    def __init__(self, x:int, y:int, width:int, height:int,
                 button_color:pygame.Color=(255,255,255), message:str=None, message_location:tuple=(1,1),
                 message_size_factor:int=1) -> None:
        """Create button rect

        Args:
            x (int): x-position
            y (int): y-position
            width (int): button width
            height (int): button height
            button_color (pygame.Color, optional): Button color. Defaults to (255,255,255)
            message (str, optional): text. Defaults to None.
            message_location (tuple, optional): coordinate to place text. Defaults to (1,1)
            message_size_factor (int, optional): Text size multiplier. Defaults to 1.
        """
        super().__init__((width,height))

        if message is not None:
            text = Font().render(self, message, message_location, message_size_factor)
            self.color = button_color
            self.fill(self.color, text.get_rect())
            self.blit(text, text.get_rect().move(x,y))
            self.rect = self.get_rect()
            
            

        else:
            self.rect = pygame.Rect(x,y,width,height)
            self.color = button_color
            self.fill(self.color, self.rect())

    def update(self, surface:pygame.Surface) -> None:
        """Render button on a surface

        Args:
            surface (pygame.Surface): Surface to render button onto
        """
        surface.blit(self, self.rect)


class Font:
    """Custom font generator from a png image"""
    def __init__(self, font_path:str='font.png') -> None:
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

    def render(self, surface:pygame.Surface, text:str, location:tuple=(0,0), size_factor:int=1) -> pygame.Surface:
        """Renders text onto pygame surface using loaded font

        Args:
            surface (pygame.Surface): Surface to render text onto
            text (str): Text to render
            location (tuple, optional): Location on surface to render text (x,y). Defaults to (0,0).
            size_factor (int, optional): Text size multiplier. Defaults to 1.
        
        Returns:
            (pygame.Surface): The surface with rendered text
        """
        x_offset = 0
        surface_copy = surface.copy()
        text_surface_list = []

        for character in text:
            if character != " ":
                text_surface_list.append((self.characters[character],
                                          (location[0] + x_offset, location[1])))
                x_offset += (self.characters[character].get_width()+1)*size_factor
            else:
                x_offset += 4*size_factor

        if size_factor > 1:
            for index, character in enumerate(text_surface_list):
                character_surface = text_surface_list[index][0]
                text_surface_list[index] = (
                    pygame.transform.scale_by(character_surface, size_factor),
                    text_surface_list[index][1]
                    )

        surface_copy = pygame.transform.scale(
            surface_copy, (
                location[0] + (text_surface_list[-1][1][0])+text_surface_list[-1][0].get_width(),
                (location[1]+10*size_factor+location[1])
                )
            )

        surface_copy.blits(text_surface_list)
        return surface_copy.convert_alpha()

class Game(pygame.Surface):
    """Game class"""
    def __init__(self, surface:pygame.Surface, frame_rate:int=60) -> None:
        """Initialize instance of game

        Args:
            surface (pygame.Surface): The window surface to be used
            frame_rate (int, optional): Target framerate (FPS). Defaults to 60.
        """
        self.screen = surface
        self.clock = pygame.time.Clock()
        self.fps = frame_rate
        self.running = False

    def run(self) -> None:
        """Run game"""
        self.running = True
        pygame.event.clear() # clear event queue

        while self.running:
            self.screen.fill((255,255,255))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                        Menu(self.screen).run()

            pygame.display.update()
            self.clock.tick(self.fps)

class Menu(pygame.Surface):
    """Game menu"""
    def __init__(self, window_surface:pygame.Surface, frame_rate:int=60) -> None:
        super().__init__((window_surface.get_width(), window_surface.get_height()))
        self.screen = window_surface
        self.rect = self.get_rect()
        self.clock = pygame.time.Clock()
        self.fps = frame_rate
        self.running = False

    def center_window(self) -> None:
        """Move menu rect to center of screen

        Args:
            screen_resolution (tuple): Size of game window
        """
        center_x = self.screen.get_width() // 2
        center_y = self.screen.get_height() // 2
        self.rect = (center_x - self.rect.centerx, center_y - self.rect.centery)
    
    def run(self) -> None:
        """Run instance"""
        self.running = True
        pygame.event.clear() # clear event queue

        exit_button = Button(x=10,y=10,width=157,height=200,message="Hey There", message_location=(2,1),message_size_factor=2)

        while self.running:
            self.screen.fill((0,255,0))
            exit_button.update(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False

            pygame.display.update()
            self.clock.tick(self.fps)

class Window:
    """Window instance"""
    def __init__(self, screen_width:int, screen_height:int) -> None:
        """Initialize window instance

        Args:
            screen_width (int): Width of game window
            screen_height (int): Height of game window
            frame_rate (int, optional): Target framerate (FPS). Defaults to 60.
        """
        pygame.init()
        self.width = screen_width
        self.height = screen_height
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.NOFRAME)

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

def text_onto_surface(surface:pygame.Surface, message:str, coordinate:tuple) -> pygame.Surface:
    """Renders text onto pygame surface

    Args:
        surface (pygame.Surface): Surface to render on
        message (str): Message to render
        coordinate (tuple): Render location (x,y)

    Returns:
        pygame.Surface: New surface with rendered text
    """
    surface_copy = surface.copy()
    text = Font('font.png')
    text.render(surface_copy, message, coordinate)
    return surface_copy

if __name__ == "__main__":
    Game(Window(640,390).screen).run()
