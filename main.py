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


class Player(pygame.sprite.Sprite):
    """Player class"""
    def __init__(self,position:tuple) -> None:
        super().__init__()
        self.image = pygame.transform.scale_by(
            pygame.image.load('assets/images/circle.png').convert_alpha(),
            factor=3
        )

        self.position = pygame.Vector2(position)
        self.velocity = pygame.Vector2(0,0)

        self.rect = self.image.get_rect()
        self.outline = get_mask_outline(self.image, (1,1))
        self.outline_rect = self.outline.get_rect()

        # Player flags #############
        self.touching_ground = False
        self.double_jump = True
        self.moving_x = False
        ############################

        # Constants ######
        self.gravity_value = 9
        self.jump_speed = -1200
        self.friction = 5
        self.movement_speed = 500
        ##################

    def check_collisions(self, sprite_group:pygame.sprite.Group) -> pygame.Rect | None:
        """Returns: pygame.rect: rect of collided sprite"""

        collision = pygame.sprite.spritecollide(self, sprite_group, False)
        for sprite_found in collision:
            return sprite_found.rect

    def gravity(self, velocity:pygame.Vector2, gravity:int) -> pygame.Vector2:
        """Applies gravity to player"""
        return pygame.Vector2(velocity.x,velocity.y+gravity)

    def jump(self) -> None:
        """Make player jump"""
        if self.touching_ground:
            self.velocity.y = self.jump_speed
            self.double_jump = True
            self.touching_ground = False

        elif not self.touching_ground and self.double_jump:
            self.velocity.y = self.jump_speed
            self.double_jump = False

    def left(self) -> None:
        """Move player left"""
        self.velocity.x = -self.movement_speed
        self.moving_x = True

    def right(self) -> None:
        """Move player right"""
        self.velocity.x = self.movement_speed
        self.moving_x = True

    def move(self, position:pygame.Vector2,
              velocity:pygame.Vector2) -> None:
        """Change player position by a given velocity (pixels)"""
        return position + velocity

    def update(
        self,surface:pygame.Surface,
        dt:float,level:pygame.sprite.Group=None) -> None:
        """Update player position and draw on surface.
        Tries rendering next frame and corrects for collisions.
        Args:
            dt (float): time difference between frames (ms/frame)
        """

        if self.touching_ground and not self.moving_x:
            # Friction
            if bool(self.velocity.x // 1):
                if abs(self.velocity.x) < self.friction:
                    self.velocity.x = 0
                elif self.velocity.x > 0:
                    self.velocity.x -= self.friction
                elif self.velocity.x < 0:
                    self.velocity.x += self.friction

        self.rect.bottomright = self.move(self.position, self.velocity*dt)

        if level:
            collision = self.check_collisions(level)
            if collision:
                if self.rect.bottom>collision.top and self.velocity.y<0:
                    self.rect.bottom = collision.top
                    self.touching_ground = True
                    self.position.y =  self.rect.centery
                    self.velocity.y = 0

                elif self.rect.top>collision.bottom and self.velocity.y>0:
                    self.rect.top = collision.bottom
                    self.position.y =  self.rect.centery
                    self.velocity.y = 0

                elif self.rect.right>collision.left and self.velocity.x<0:
                    self.rect.right = collision.left
                    self.position.x =  self.rect.centerx
                    self.velocity.x = 0

                elif self.rect.left<collision.right and self.velocity.x>0:
                    self.rect.left = collision.right
                    self.position.x =  self.rect.centerx
                    self.velocity.x = 0
            else:
                self.position = self.move(self.position, self.velocity*dt)

            surface.blit(self.image, self.rect)


        else:
            self.position = self.move(self.position, self.velocity*dt)
            surface.blit(self.image, self.rect)
        
        print(self.position, self.rect)

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
        player = Player((0,0))

        #sample = pygame.transform.scale(pygame.image.load('assets/images/dvd.png').convert_alpha(), (200,200))
        #sample_mask = get_mask(sample)
        #sample_rect = sample_mask.get_rect()
        #sample_rect_pos = pygame.Vector2(sample_rect.center)
#
        player.image.fill((100,100,100),special_flags=pygame.BLEND_RGB_MAX)
        #speed = pygame.Vector2(200, 200)
#
        last_time = time.time()
#
        while self.running:
            player_velocity_value = Font().render(
                "Velocity = " + str(player.velocity),
                size_factor=1,
                text_color=(0,0,0)
            )

            player_position_value = Font().render(
                "Position: " + str(player.position),
                size_factor=1,
                text_color=(0,0,0)
            )

            player_touching_ground = Font().render(
                "Touching ground = " + str(player.touching_ground),
                size_factor=1,
                text_color=(0,0,0)
            )

            dt = time.time() - last_time
            last_time = time.time()
#
        #    if sample_rect_pos.x + (speed.x * dt) + (sample_rect.width/3) > (self.screen.get_width()):
        #        speed.x *= -1
        #    
        #    if sample_rect_pos.y + (speed.y * dt) + (sample_rect.height/3) > (self.screen.get_height()):
        #        speed.y *= -1
#
        #    if sample_rect_pos.x  - (sample_rect.width/3) + (speed.x *dt) <= (0):
        #        if abs(speed.x) != speed.x:
        #            speed.x *=-1
#
        #    if sample_rect_pos.y - (sample_rect.height/3) + (speed.y *dt) <= (0):
        #        if abs(speed.y) != speed.y:
        #            speed.y *=-1
#
        #    sample_rect_pos += (speed * dt)
        #    sample_rect.center = sample_rect_pos
        #    self.screen.blit(sample,sample_rect.topleft)
            #pygame.draw.rect(self.screen,(255,0,0), sample_rect)

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
            self.screen.blit(player_position_value, (2,10))
            self.screen.blit(player_touching_ground, (2,18))

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