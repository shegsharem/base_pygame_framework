""" python 3.12.1 """
# pylint: disable=maybe-no-member
import sys
import time
import pygame
from pygame.locals import *
from src.button import Button, get_mask
from src.font import Font
#from src.player import Player
from random import randint
from src.window import Window
from math import floor

class Level:
    """Level class. Block sprites shall be 5x5px"""
    def __init__(self, level_map:list) -> None:
        super().__init__()
        self.level_map = level_map
        self.group = pygame.sprite.Group()

        for row_index, row in enumerate(self.level_map):
            for col_index, cell in enumerate(row):
                x = -10 + int(col_index*10)
                y = -10 + int(row_index*10)

                # Dirt
                if cell == "D":
                    self.terrain = pygame.sprite.Sprite()
                    self.terrain.image = pygame.Surface((10,10))
                    self.terrain.rect = self.terrain.image.get_rect().move(x,y)
                    self.group.add(self.terrain)

    def update(self, screen:pygame.Surface):
        for sprite in self.group:
            screen.blit(sprite.image, sprite.rect)


def collision_check(rect:pygame.Rect,
                      sprite_group:pygame.sprite.Group,
                      velocity:pygame.Vector2) -> (pygame.Rect, list):
    """Checks for collisions

    Args:
        sprite_group (pygame.sprite.Group): Sprites to collide with
        velocity (pygame.Vector2): To manage movements

    Returns:
        rect (pygame.Rect): New player rect to use
        list: Collision types
    """

    collision_list = []

    collision_types = {
            'top': False,
            'bottom': False,
            'right': False,
            'left': False
    }

    for sprite in sprite_group:
        if rect.colliderect(sprite.rect):
            collision_list.append(sprite.rect)

    for sprite_rect in collision_list:
        
        rect.x += velocity.x
        rect.y += velocity.y

        # Check x direction collisions
        if velocity.x > 0:
            rect.right = sprite_rect.left
            collision_types['right'] = True
        if velocity.x < 0:
            rect.left = sprite_rect.right
            collision_types['left'] = True

    
        # Check y direction collisions
        if velocity.y > 0:
            rect.bottom = sprite_rect.top
            collision_types['bottom'] = True
        elif velocity.y < 0:
            rect.top = sprite_rect.bottom
            collision_types['top'] = True

    return rect, collision_types


class Player(pygame.sprite.Sprite):
    """Player class"""
    def __init__(self) -> None:
        super().__init__()
        self.image = pygame.transform.scale(
            pygame.image.load('assets/images/dvd.png').convert_alpha(),
            (100,100)
        )

        self.velocity = pygame.Vector2(0,0)
        self.position = pygame.Vector2(0,0)

        self.rect = self.image.get_rect()
        self.outline = get_mask_outline(self.image, (1,1))
        self.outline_rect = self.outline.get_rect()

        # Player flags #############
        self.touching_ground = False
        self.double_jump = True
        self.moving_right = False
        self.moving_left = False
        self.moving_x = False
        ############################

        # Constants ######
        self.gravity = 9
        self.jump_speed = -1000
        self.friction = 3
        self.movement_speed = 900
        ##################

    def jump(self) -> None:
        """Make player jump"""
        if not self.touching_ground and self.double_jump:
            self.velocity.y = self.jump_speed
            self.double_jump = False
        
        if self.touching_ground:  
            self.velocity.y = self.jump_speed
            self.double_jump = True
            self.touching_ground = False

    def left(self) -> None:
        """Move player left"""
        self.velocity.x = -self.movement_speed
        self.moving_x = True

    def right(self) -> None:
        """Move player right"""
        self.velocity.x = self.movement_speed
        self.moving_x = True

    def move(self, position:pygame.Vector2,
              velocity:pygame.Vector2) -> pygame.Vector2:
        """Change player position by a given velocity (pixels)"""
        return position + velocity

    def update(self,surface:pygame.Surface,
        dt:float,level:pygame.sprite.Group=None) -> None:
        """Update player position and draw on surface.
        Tries rendering next frame and corrects for collisions.
        Args:
            dt (float): time difference between frames (ms/frame)
        """
        self.moving_left, self.moving_right = False, False
        self.velocity.y += (self.gravity) # Apply gravity

        if self.touching_ground and not self.moving_x:
            if bool(self.velocity.x // 1):
                if abs(self.velocity.x) < self.friction:
                    self.velocity.x = 0
                elif self.velocity.x > 0:
                    self.moving_right = True
                    self.velocity.x -= self.friction
                elif self.velocity.x < 0:
                    self.moving_left = True
                    self.velocity.x += self.friction

        self.rect.topleft += self.velocity*dt

        rect, collision_list = collision_check(self.rect, level, self.velocity*dt) # Check collisions

        if collision_list['bottom']:
            self.touching_ground = True
            self.velocity.y = 0

        if not collision_list['bottom']:
            self.touching_ground = False

            if collision_list['top']:
                self.velocity.y *= -1


        self.position += (self.velocity*dt)
        
        self.rect.topleft = self.position
        print(collision_list)

        pygame.draw.rect(surface, (200,200,200), self.outline_rect.move(0,-1))
        surface.blit(self.image, self.rect.move(0,-1))

class Game:
    """Game class"""
    def __init__(self, surface:pygame.Surface, frame_rate:int=60) -> None:
        """Initialize instance of game

        Args:
            surface: Surface to draw on.
            frame_rate: Framerate target
        """
        self.screen = surface
        self.clock = pygame.time.Clock()
        self.time = time.time()
        self.fps = frame_rate
        self.running = False

        self.level_map = list(open('level.txt'))

    def __str__(self) -> str:
        return f'The frame rate is set to {self.fps}.'

    def run(self) -> None:
        """Run game"""
        self.running = True
        pygame.event.clear() # clear event queue
        background = Level(self.level_map)
        player = Player()

        last_time = time.time()

        while self.running:
            dt = time.time() - last_time
            last_time = time.time()

            player_velocity_value = Font().render(
                "Velocity = " + str(player.velocity),
                size_factor=2,
                text_color=(0,0,0)
            )

            player_position_value = Font().render(
                "Position: " + str(player.position),
                size_factor=2,
                text_color=(0,0,0)
            )

            player_touching_ground = Font().render(
                "Touching ground = " + str(player.touching_ground),
                size_factor=2,
                text_color=(0,0,0)
            )

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                        Menu(self.screen).run()

                    if event.key == pygame.K_a:
                        player.left()

                    if event.key == pygame.K_d:
                        player.right()

                    if event.key == pygame.K_s:
                        player.velocity.y = 500

                    if event.key == pygame.K_w:
                        player.jump()

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        player.moving_x = False

                    if event.key == pygame.K_d:
                        player.moving_x = False


            self.screen.fill((200,200,200))
            background.update(self.screen)
            pygame.draw.rect(self.screen,(0,0,0), player.rect,1)
            player.update(self.screen,dt,background.group)
            self.screen.blit(player_velocity_value, (2,2))
            self.screen.blit(player_position_value, (2,20))
            self.screen.blit(player_touching_ground, (2,40))

            pygame.display.flip()

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
            text="Play",x=25,y=self.screen.get_height()-120,
            width=90, height=60,button_color =(65,65,65),text_size_factor=3,
            button_highlighted_color=(95,95,95),
            text_color=(255,255,255), button_border_radius=4,
            callback=self.start_game
        )

        editor_button = Button(
            text="Editor",x=25,y=self.screen.get_height()-50,
            width=90, height=35,
            button_color =(55,55,55),text_size_factor=2,
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

        pixel_text =  Font().render("- Pixel -", size_factor=2,text_color=(255,255,255))
        editor_text = Font().render("Art Editor", size_factor=2,text_color=(255,255,255))

        options_frame = pygame.draw.rect(
            self.screen,(64,64,64),
            (10,55,100,
            self.screen.get_height()-80),
            border_radius=15
        )

        new_button = Button(
            x=15,y=60,
            width=90,height=40,
            text="New",button_color= (56,56,56),
            button_highlighted_color=(80,80,80),
            text_size_factor=2,text_color=(255,255,255),
            button_border_radius=7,callback=self.kill
        )

        open_button = Button(
            x=15,y=105,
            width=90,height=40,
            text="Open",button_color= (56,56,56),
            button_highlighted_color=(80,80,80),
            text_size_factor=2,text_color=(255,255,255),
            button_border_radius=7,callback=self.kill
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

            self.screen.blit(pixel_text, (19,self.screen.get_rect().top+5))
            self.screen.blit(editor_text, (10,self.screen.get_rect().top+25))
            new_button.update(self.screen)
            open_button.update(self.screen)
            exit_button.update(self.screen)

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
    Menu(Window(1280,720).screen,60).run()