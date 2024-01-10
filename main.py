""" python 3.12.1 """
import sys
import time
import pygame
from pygame.locals import *
from button import Button
from font import Font
from player import Player

class BoxSprite(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__(self)

        self.image = pygame.Surface((width,height))
        self.image.fill(color)
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.move(10,0)

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
        self.time = time.time()
        self.fps = frame_rate
        self.running = False

        #self.player = Player((10,10), "data/images/playerframes/player", 7)
        #self.player_position = (90,90)

    def __str__(self) -> str:
        return f'The frame rate is set to {self.fps}.'

    def run(self) -> None:
        """Run game"""
        self.running = True
        pygame.event.clear() # clear event queue
        message = Font().render("Hello World!", (0,0), 2, (0,100,100))
        self.screen.fill((255,255,255))
        

        while self.running:
            last_time = time.time()
            self.screen.blit(message, (0,0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                        Menu(self.screen).run()

                    if event.key == pygame.K_a:
                        self.player.move((1,0))

            pygame.display.update()
            deltatime = self.fps - (time.time()-last_time)
            self.clock.tick(deltatime)

class Menu:
    """Game menu"""
    def __init__(self, surface:pygame.Surface, frame_rate:int=60) -> None:
        self.screen = surface
        self.rect = self.screen.get_rect()
        self.clock = pygame.time.Clock()
        self.fps = frame_rate
        self.running = False
        self.background_color = (56,56,56)

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

        play_button = Button(x=10,y=0,width=100,height=100,text="Play",
                                   button_color =(50,50,50),text_size_factor=3,
                                   button_highlighted_color=(85,85,85),
                                   text_color=(255,255,255), button_border_radius=7,
                                   callback=self.start_game, anchor='center')

        exit_button = Button(x=0,y=0,text="x",button_color= self.background_color,
                             button_highlighted_color=(255,0,0),
                             text_size_factor=2,text_color=(255,255,255),
                             callback=self.kill, anchor='topright')
        
        self.screen.fill(self.background_color)

        while self.running:
            deltatime = 0
            last_time = time.time()
            
            self.screen.blit(menu_title, (5,7))
            exit_button.update(self.screen)
            play_button.update(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.flip()
            deltatime = self.fps - (time.time()-last_time)
            self.clock.tick(deltatime)

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
        self.screen = pygame.display.set_mode((self.width, self.height),pygame.NOFRAME)

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
    Menu(Window(640,390).screen,30).run()
