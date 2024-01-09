# python 3.12.1
import sys
import pygame
from pygame.locals import *

class Button:
    """Simple button class."""

    def __init__(self, x:int, y:int,
                 width:int=10, height:int=10,
                 button_color:tuple=(255,255,255),
                 button_highlighted_color:tuple=(255,255,255),
                 text:str=None, text_size_factor:int=1,
                 text_color:tuple=None, button_border_radius:int=0, anchor:str=None,
                 callback=None) -> None:
        """Create button rect

        Args:
            x (int): x-position
            y (int): y-position
            width (int, optional): button width. Defaults to 10.
            height (int): button height. Defaults to 10.
            button_color (tuple, optional): Button color. Defaults to (255,255,255).
            button_hightlighted_color (tuple, optional): Button highlighted color.
                Defaults to (255,255,255).
            text (str, optional): text. Defaults to None.
            text_size_factor (int, optional): Text size multiplier. Defaults to 1.
            text_color (tuple, optional): Text color. Defaults to None.
            button_border_radius (int, optional): Button corner radius. Defaults to 0.
            anchor (optional): location to anchor button
            Callback: Button callback for when clicked
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.corner_radius = button_border_radius
        self.anchor = anchor

        self.color = pygame.Color(button_color)
        self.text_color = pygame.Color(text_color)
        self.highlighted_color = pygame.Color(button_highlighted_color)

        self.text = text
        self.text_size_factor = text_size_factor

        self.callback = callback

        self.button(self.color)

    def button(self, color:tuple=(0,0,0,0)) -> pygame.Surface:
        """Create button

        Returns: pygame.Surface: Button surface
        """
        if self.text:
            text_surface = Font().render(
                text=self.text,
                size_factor=self.text_size_factor,
                text_color=self.text_color
            )

            text_surface_rect = text_surface.get_rect()

            button_surface = pygame.Surface(
                (text_surface_rect.width+self.text_size_factor*10,
                text_surface_rect.height+self.text_size_factor*10),
                pygame.SRCALPHA
            )

            button_surface_rect = button_surface.get_rect()
            text_surface_rect.center = button_surface_rect.center

            pygame.draw.rect(
                surface=button_surface,
                color=color,
                rect=button_surface_rect,
                border_radius=self.corner_radius*self.text_size_factor
            )

            button_surface.blit(text_surface,text_surface_rect)
            return button_surface

        button_surface = pygame.Surface((self.width, self.height),pygame.SRCALPHA)
        button_surface_rect = button_surface.get_rect()

        pygame.draw.rect(
                surface=button_surface,
                color=color,
                rect=button_surface_rect,
                border_radius=self.corner_radius*self.text_size_factor
            )

        return button_surface

    def check_mouse(self, button:pygame.Surface) -> (bool, bool):
        """Check if mouse is hovering button

        Args:
            screen (pygame.Surface): Main window
            button_rect (pygame.Rect): Button surface

        Returns: (bool, bool): Is hovering, is clicked
        """
        is_hovering = 0
        is_clicked = 0
        mouse_position = pygame.mouse.get_pos()
        button_mask = pygame.mask.from_surface(button)
        button_mask_surface = pygame.Mask.to_surface(button_mask)
        button_mask_rect = button_mask_surface.get_rect().move(self.x,self.y)

        if button_mask_rect.collidepoint(mouse_position):
            if button_mask.get_at((mouse_position[0]-self.x,
                                   mouse_position[1]-self.y)):
                is_hovering = 1

        if pygame.mouse.get_pressed()[0]:
            is_clicked = 1

        return is_hovering, is_clicked


    def update(self, screen:pygame.Surface) -> pygame.Rect:
        """Update button and draw on screen

        Args:
            screen (pygame.Surface): Main window
            callback (optional): callback function for when clicked

        Returns: pygame.Rect
        """
        color, highlighted_color = self.color, self.highlighted_color
        button = self.button(color)

        is_hovering, is_clicked = self.check_mouse(button)

        if is_hovering:
            button = self.button(highlighted_color)
            if is_clicked and callable(self.callback):
                self.callback()

        if self.anchor:
            screen_rect, button_rect = screen.get_rect(), button.get_rect()

            if self.anchor == 'topleft':
                button_rect.topleft = screen_rect.topleft
                self.x, self.y = button_rect.x, button_rect.y
                return screen.blit(button,(self.x,self.y))

            if self.anchor == 'topright':
                button_rect.topright = screen_rect.topright
                self.x, self.y = button_rect.x, button_rect.y
                return screen.blit(button,(self.x,self.y))

            if self.anchor == 'center':
                button_rect.center = screen_rect.center
                self.x, self.y = button_rect.x, button_rect.y
                return screen.blit(button,(self.x,self.y))

            if self.anchor == 'bottomleft':
                button_rect.bottomleft = screen_rect.bottomleft
                self.x, self.y = button_rect.x, button_rect.y
                return screen.blit(button,(self.x,self.y))

            if self.anchor == 'bottomright':
                button_rect.bottomright = screen_rect.bottomright
                self.x, self.y = button_rect.x, button_rect.y
                return screen.blit(button,(self.x,self.y))

        return screen.blit(button,(self.x,self.y))


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

                clipped_character_image = clip(
                    font_image, (pixel-current_character_width), 0,
                    current_character_width, font_image.get_height()
                )

                self.characters[self.character_map[character_clip_count]] = clipped_character_image
                character_clip_count += 1
                current_character_width = 0
            else:
                current_character_width += 1

        self.character_space_width = self.characters["!"].get_width()

    def __str__(self) -> str:
        return f'{self.characters}'

    def render(self,text:str,
               location:tuple=(0,0),
               size_factor:int=1,
               text_color:pygame.Color=None) -> pygame.Surface:
        """Renders text to pygame surface using loaded font

        Args:
            text (str): Text to render
            location (tuple, optional): Location on surface to render text (x,y).
                Note: May clip text if not (0,0). Defaults to (0,0).
            size_factor (int, optional): Text size multiplier. Defaults to 1.
            text_color (pygame.Color, optional): Text color. Defaults to (0,0,0), black.
        
        Returns:
            (pygame.Surface): Pygame surface with rendered text
        """
        x_offset = 0
        text_surface_list = []

        for character in text:
            if character != " ":

                text_surface_list.append(
                    (self.characters[character],
                    (location[0]+x_offset,location[1]))
                )

                x_offset += (self.characters[character].get_width()+1)*size_factor
            else:
                x_offset += 4*size_factor

        if size_factor > 1:
            for index,character in enumerate(text_surface_list):
                character_surface = character[0]

                text_surface_list[index] = (
                    pygame.transform.scale_by(character_surface,size_factor),
                    text_surface_list[index][1]
                )

        text_surface = pygame.Surface(
            (x_offset-size_factor,
            text_surface_list[-1][0].get_height()),
            pygame.SRCALPHA
        )

        text_surface.blits(text_surface_list)
        text_surface_rect = text_surface.get_bounding_rect()

        text_surface = clip(
            text_surface,
            text_surface_rect.x,
            text_surface_rect.y,
            text_surface_rect.width,
            text_surface_rect.height
        )

        if text_color:
            text_surface.fill(text_color,special_flags=pygame.BLEND_RGB_MAX)
            return text_surface
        return text_surface


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

    def __str__(self) -> str:
        return f'The frame rate is set to {self.fps}.'

    def run(self) -> None:
        """Run game"""
        self.running = True
        pygame.event.clear() # clear event queue
        message = Font("font.png").render("Hello World!", (0,0), 2, (0,100,100))

        while self.running:
            self.screen.fill((255,255,255))
            self.screen.blit(message, (0,0))

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
    
    def start_game(self) -> None:
        self.running = False
        Game(self.screen, self.fps).run()

    def kill(self):
        self.running = False

    def run(self) -> None:
        """Run instance"""
        self.running = True
        pygame.event.clear() # clear event queue

        menu_title = Font().render("Editor", size_factor=2,text_color=(255,255,255))

        test_button = Button(x=10,y=0,width=100,height=100,text="Play",
                                   button_color =(50,50,50),text_size_factor=3,
                                   button_highlighted_color=(85,85,85),
                                   text_color=(255,255,255), button_border_radius=7,
                                   callback=self.start_game)

        exit_button = Button(x=0,y=0,text="x",button_color= (23,23,23),
                             button_highlighted_color=(255,0,0),
                             text_size_factor=2,text_color=(255,255,255),
                             callback=self.kill, anchor='topright')

        color = (56,56,56)

        while self.running:
            self.screen.fill(color)
            self.screen.blit(menu_title, (5,7))
            exit_button.update(self.screen)
            test_button.update(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

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
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.NOFRAME, pygame.SRCALPHA)

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

def get_mask_outline(surface:pygame.Surface, offset:tuple) -> pygame.Surface:
    """Gets an outline from mask of surface

    Args:
        surface (pygame.Surface): Surface to mask from
        offset (tuple): Offset of outline
    
    Returns:

    """
    surface_copy = surface.copy()
    mask = pygame.mask.from_surface(surface)
    mask_surface = mask.to_surface()
    mask_surface.set_colorkey((0,0,0))
    surface_copy.blit(mask_surface, (offset[0]-1,offset[1]))
    surface_copy.blit(mask_surface, (offset[0]+1,offset[1]))
    surface_copy.blit(mask_surface, (offset[0],offset[1]-1))
    surface_copy.blit(mask_surface, (offset[0],offset[1]+1))
    return surface_copy

if __name__ == "__main__":
    Menu(Window(1000,668).screen).run()
