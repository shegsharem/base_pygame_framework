""" python 3.12.1 """
# pylint: disable=maybe-no-member
import sys
import time
import pygame
from pygame.locals import *
from src.level import Level

pygame.init()
screen = pygame.display.set_mode((1280,720),pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.NOFRAME)

clock = pygame.time.Clock()
player = Player()
level_map = list(open('level.txt'))
background = Level(level_map)
running = 0
FPS = 60


class Player(pygame.sprite.Sprite):#
    """Player class"""
    def __init__(self) -> None:
        super().__init__()
        self.image = pygame.transform.scale_by(
            pygame.image.load('assets/images/circle.png').convert_alpha(),
            factor=4
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
        self.gravity = 0.75
        self.jump_speed = -15
        self.friction = 3
        self.movement_speed = 15
        ##################

    def jump(self) -> None:
        """Make player jump"""
        if self.touching_ground:
            self.velocity.y = self.jump_speed
            self.double_jump = True

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
              velocity:pygame.Vector2) -> pygame.Vector2:
        """Change player position by a given velocity (pixels)"""
        return position + velocity

    def update(self,surface:pygame.Surface,
        level:pygame.sprite.Group=None) -> None:
        """Update player position and draw on surface.
        Tries rendering next frame and corrects for collisions.
        Args:
            dt (float): time difference between frames (ms/frame)
        """

        # Collisions ################################################################
        collision_list = []
        collision_types = {'top': False,'bottom': False,'right': False,'left': False}

        self.position = self.rect.topleft

        self.position += (self.velocity)
        self.rect.x = round(self.position.x)
        self.rect.y = round(self.position.y)

        for sprite in level:
            if self.rect.colliderect(sprite.rect):
                collision_list.append(sprite.rect)

        # Check y direction collisions #############
        for sprite_rect in collision_list:
            if self.velocity.y >= 0:
                self.rect.bottom = sprite_rect.top
                self.position = self.rect.topleft
                collision_types['bottom'] = True

            elif self.velocity.y < 0:
                self.rect.top = sprite_rect.bottom
                self.position = self.rect.topleft
                collision_types['top'] = True

        # Check x direction collisions #############
            elif self.velocity.x > 0:
                #self.rect.right = sprite_rect.left
                self.position = self.rect.topleft
                collision_types['right'] = True

            elif self.velocity.x < 0:
                #self.rect.left = sprite_rect.right
                self.position = self.rect.topleft
                collision_types['left'] = True
        ################################################################################

        if collision_types['left']:
            self.velocity.x = 0
        
        if collision_types['right']:
            self.velocity.x = 0

        if collision_types['bottom']:
            self.touching_ground = True
            self.velocity.y =0
            if collision_types['right']:
                self.velocity.x = 0

        if not collision_types['bottom']:
            self.touching_ground = False
            self.velocity.y += (self.gravity)

        #Friction
        if self.touching_ground:
            if self.velocity.x // 1:
                if abs(self.velocity.x) < self.friction:
                    self.velocity.x = 0
                elif self.velocity.x > 0:
                    self.moving_right = True
                    self.velocity.x -= self.friction
                elif self.velocity.x < 0:
                    self.moving_left = True
                    self.velocity.x += self.friction
        
        print(collision_types)
        print(self.position)
        print(self.velocity,"\n")


        pygame.draw.rect(surface, (200,200,200), self.outline_rect)
        surface.blit(self.image, self.rect)

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
        self.fps = frame_rate
        self.running = False
        self.player = Player()
        self.level_map = list(open('level.txt'))

    def run(self) -> None:
        """Run game"""
        self.running = True
        pygame.event.clear() # clear event queue
        background = Level(self.level_map)
        fps = self.fps

        pygame.event.set_allowed([QUIT, KEYDOWN, KEYUP])

        while self.running:
            previous_time = time.time()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                        pygame.quit()
                        sys.exit()

                    if event.key == pygame.K_a:
                        pass

                    if event.key == pygame.K_d:
                        pass

                    if event.key == pygame.K_s:
                        pass

                    if event.key == pygame.K_w:
                        self.player.jump()

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        pass

                    if event.key == pygame.K_d:
                        pass

            self.screen.fill((200,200,200))
            background.update(self.screen)
            self.player.update(self.screen,background.group)
            pygame.display.flip()
            dt = time.time() - previous_time
            self.clock.tick(fps-dt)

def main() -> None:
    """Main game loop"""
    player = Player()
    pygame.event.set_allowed([QUIT, KEYDOWN, KEYUP])

    running = 1
    

    while running:




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
    Game(screen,60).run()
