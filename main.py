""" python 3.12.1 """
# pylint: disable=maybe-no-member
import sys
import time
import pygame
from pygame.locals import *
from src.button import Button, get_mask
from src.font import Font
from src.player import Player
from random import randint
from src.window import Window

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
        self.screen.fill((255,255,255))
        sample = pygame.transform.scale(pygame.image.load('assets/images/dvd.png').convert_alpha(), (200,200))
        sample_mask = get_mask(sample)
        sample_rect = sample_mask.get_rect()
        sample_rect_pos = pygame.Vector2(sample_rect.center)

        sample.fill((255,255,255),special_flags=pygame.BLEND_RGB_MAX)
        speed = pygame.Vector2(200, 200)

        last_time = time.time()

        while self.running:
            dt = time.time() - last_time
            last_time = time.time()

            self.screen.fill((0,0,0))
            message = Font().render("Current time:", (0,0), 2, (100,100,100))
            t = Font().render(str(round(time.time(),4)), (0,0), 4, (200,0,0))

            if sample_rect_pos.x + (speed.x * dt) + (sample_rect.width/3) > (self.screen.get_width()):
                speed.x *= -1
            
            if sample_rect_pos.y + (speed.y * dt) + (sample_rect.height/3) > (self.screen.get_height()):
                speed.y *= -1

            if sample_rect_pos.x  - (sample_rect.width/3) + (speed.x *dt) <= (0):
                if abs(speed.x) != speed.x:
                    speed.x *=-1

            if sample_rect_pos.y - (sample_rect.height/3) + (speed.y *dt) <= (0):
                if abs(speed.y) != speed.y:
                    speed.y *=-1

            sample_rect_pos += (speed * dt)
            sample_rect.center = sample_rect_pos
            self.screen.blit(sample,sample_rect.topleft)
            #pygame.draw.rect(self.screen,(255,0,0), sample_rect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                        Menu(self.screen).run()

            self.screen.blit(message, (5,5))
            self.screen.blit(t, (5,25))
            self.screen.blit(sample,sample_rect)

            pygame.display.update()

class Menu:
    """Game menu"""
    def __init__(self, surface:pygame.Surface, frame_rate:int=60) -> None:
        self.screen = surface
        self.rect = self.screen.get_rect()
        self.clock = pygame.time.Clock()
        self.fps = frame_rate
        self.running = False
        self.background_color = (56,56,56)

    def start_game(self) -> None:
        self.running = False
        Game(self.screen, self.fps).run()
    
    def start_editor(self):
        self.running = False
        Editor(self.screen, self.fps).run()

    def kill(self) -> None:
        self.running = False

    def run(self) -> None:
        """Run instance"""
        self.running = True
        pygame.event.clear() # clear event queue

        menu_title = Font().render("Game", size_factor=2,text_color=(255,255,255))

        play_button = Button(
            text="Play",x=25,y=self.screen.get_height()-120,button_color =(65,65,65),text_size_factor=3,
            button_highlighted_color=(95,95,95),
            text_color=(255,255,255), button_border_radius=7,
            callback=self.start_game
        )

        editor_button = Button(
            text="Level Editor",x=25,y=self.screen.get_height()-50,button_color =(55,55,55),text_size_factor=2,
            button_highlighted_color=(95,95,95),
            text_color=(255,255,255), button_border_radius=7,
            callback=self.start_editor
        )

        exit_button = Button(
            width=25,height=25,
            text="x",button_color= self.background_color,
            button_highlighted_color=(255,0,0),
            text_size_factor=2,text_color=(255,255,255),
            callback=self.kill, anchor='topright'
        )

        self.screen.fill(self.background_color)

        while self.running:
            deltatime = 0
            last_time = time.time()
            
            self.screen.blit(menu_title, (5,7))
            exit_button.update(self.screen)
            play_button.update(self.screen)
            editor_button.update(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.flip()
            deltatime = self.fps - (time.time()-last_time)
            self.clock.tick(deltatime)

class Editor:
    """Game menu"""
    def __init__(self, surface:pygame.Surface, frame_rate:int=60) -> None:
        self.screen = surface
        self.rect = self.screen.get_rect()
        self.clock = pygame.time.Clock()
        self.fps = frame_rate
        self.running = False
        self.background_color = (56,56,56)
    
    def kill(self) -> None:
        self.running = False
        Menu(self.screen, self.fps).run()

    def run(self):
        """Run instance"""
        self.running = True
        pygame.event.clear() # clear event queue

        self.screen.fill(self.background_color)

        editor_title = Font().render("Level Editor", size_factor=1,text_color=(255,255,255))

        toolbar_frame = pygame.draw.rect(
            self.screen,(64,64,64),
            (10,55,self.screen.get_width()//5+10,
            self.screen.get_height()-80),
            border_radius=15
        )

        file_button = Button(
            width=45,height=25,
            text="File",button_color= (56,56,56),
            button_highlighted_color=(80,80,80),
            text_size_factor=2,text_color=(255,255,255),
            callback=self.kill
        )

        edit_button = Button(
            x=45,y=0,
            width=48,height=25,
            text="Edit",button_color= (56,56,56),
            button_highlighted_color=(80,80,80),
            text_size_factor=2,text_color=(255,255,255),
            callback=self.kill
        )

        exit_button = Button(
            x=0,y=0,
            width=25,height=25,
            text="x",button_color= self.background_color,
            button_highlighted_color=(255,0,0),
            text_size_factor=2,text_color=(255,255,255),
            callback=self.kill, anchor='topright'
        )

        while self.running:
            deltatime = 0
            last_time = time.time()

            self.screen.blit(editor_title, (2,self.screen.get_rect().bottom-10))
            exit_button.update(self.screen)
            file_button.update(self.screen)
            edit_button.update(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.flip()
            deltatime = self.fps - (time.time()-last_time)
            self.clock.tick(deltatime)



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
    Menu(Window(820,590).screen,60).run()
