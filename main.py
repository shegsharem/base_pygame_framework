# python 3.12.1
import sys
import pygame
from pygame.locals import *
from random import randint

class Button:
    """Button class"""
    def __init__(self, x:int, y:int, width:int, height:int,
                 button_color:pygame.Color=(255,255,255), message:str=None,
                 message_location:tuple=(1,1), message_size_factor:int=1) -> None:
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
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = button_color
        self.message = message
        self.message_location = message_location
        self.message_size_factor = message_size_factor
        self.rect = pygame.Rect(x,y,width,height)

    def draw(self, surface:pygame.Surface) -> None:
        """Draw button on a surface

        Args:
            surface (pygame.Surface): Surface to render button onto
        """
        if self.message is not None:
            text = Font().render(self.message, self.message_location, self.message_size_factor)
            text_rect = text.get_bounding_rect().move(self.x,self.y)
            pygame.draw.rect(surface, self.color, text_rect,14,1,1,1,1)
            surface.blit(text, text_rect)
        else:
            pygame.draw.rect(surface,self.color, self.rect, 0, 2)

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

        self.character_space_width = self.characters["!"].get_width()

    def render(self, text:str, location:tuple=(0,0), size_factor:int=1) -> pygame.Surface:
        """Renders text to pygame surface using loaded font

        Args:
            text (str): Text to render
            location (tuple, optional): Location on surface to render text (x,y). Defaults to (0,0).
            size_factor (int, optional): Text size multiplier. Defaults to 1.
        
        Returns:
            (pygame.Surface): Pygame surface with rendered text
        """
        x_offset = 0
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

        text_surface = pygame.Surface((x_offset-size_factor,
                                       text_surface_list[-1][0].get_height()))
        text_surface.fill((255,255,255))
        text_surface.blits(text_surface_list)
        return text_surface.convert_alpha()

class Game:
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
        message = Font("font.png").render("Heythere", (0,0), 3)

        while self.running:
            self.screen.fill((255,255,255))
            self.screen.blit(message, (2,2))

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

class Menu:
    """Game menu"""
    def __init__(self, surface:pygame.Surface, frame_rate:int=60) -> None:
        self.screen = surface
        self.rect = self.screen.get_rect()
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

        self.screen.fill((0,255,0))

        exit_button = Button(x=100,y=200,width=157,height=200,message="EXIT",message_size_factor=23)
        exit_button.draw(self.screen)

        while self.running:


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

if __name__ == "__main__":
    Game(Window(1920,1080).screen).run()
