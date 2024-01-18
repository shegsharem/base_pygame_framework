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
#player = Player() when player is external file
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
        self.pre_position = [0,0]
        self.delta_position = [0,0]

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
        self.gravity = 1
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

    def handle_collisions(self,rect:pygame.Rect,
                          level:pygame.sprite.Group) -> list[pygame.Rect,dict[str, bool]] | None:
        """Check collisions and handle accordingly"""
        collision_list = sprite_group_collision(rect, level)

        if collision_list:
            collision_types = {'top': False,'bottom': False,
                               'right': False,'left': False}

            # Check y direction collisions #############
            for sprite_rect in collision_list:
                if self.velocity.y > 0:
                    rect.bottom = sprite_rect.top
                    collision_types['bottom'] = True

                elif self.velocity.y < 0:
                    rect.top = sprite_rect.bottom
                    collision_types['top'] = True

            # Check x direction collisions #############
            for sprite_rect in collision_list:
                if self.velocity.x > 0:
                    #self.rect.right = sprite_rect.left
                    collision_types['right'] = True

                elif self.velocity.x < 0:
                    #self.rect.left = sprite_rect.right
                    collision_types['left'] = True

            return [rect,collision_types]
        return None

    def update(self,surface:pygame.Surface,
        level:pygame.sprite.Group=None) -> None:
        """Update player position and draw on surface.
        Tries rendering next frame and corrects for collisions.
        Args:
            dt (float): time difference between frames (ms/frame)
        """
        self.pre_position = [self.rect.x,self.rect.y] # using for delta position

        # Check next frame for collision #####################
        future_rect = pygame.Rect(
            self.pre_position[0],
            self.pre_position[1],
            self.rect.width+self.velocity.x,
            self.rect.height+self.velocity.y
        )

        # Setting position to check collision

        print(future_rect)

        collision = self.handle_collisions(future_rect, level)
        ######################################################

        if collision:
            print(collision[0])
            self.rect = collision[0]

            if collision[1]['left']:
                self.velocity.x = 0

            if collision[1]['right']:
                self.velocity.x = 0

            if collision[1]['bottom']:
                self.touching_ground = True
                self.velocity.y =0
                if collision[1]['right']:
                    self.velocity.x = 0

            if not collision[1]['bottom']:
                self.touching_ground = False

        elif not collision:
            self.rect.x += self.velocity.x
            self.rect.y += self.velocity.y

        pygame.draw.rect(surface, (0,0,0), self.rect,1)
        surface.blit(self.image, self.rect)
        pygame.draw.rect(surface, (255,0,0), future_rect, 1)

        print(self.rect.y)
        print(future_rect.y)
        print(self.velocity,"\n")

        # Gravity
        self.velocity.y += self.gravity

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


def rect_collision(rect1:pygame.Rect,rect2:pygame.Rect) -> bool:
    """Checks for single collision"""
    if rect1.colliderect(rect2):
        return True
    return False

def sprite_group_collision(rect:pygame.Rect,sprite_group:pygame.sprite.Group) -> list | None:
    """Check rect collision with any sprite in sprite_group

    Returns:
        list: Rects of sprite_group that have been collided with
    """
    collision_list = []

    for sprite in sprite_group:
        if rect.colliderect(sprite.rect):
            collision_list.append(sprite.rect)

    if len(collision_list) > 0:
        return collision_list
    return None

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

def main() -> None:
    """Main game loop"""
    player = Player()
    player_mask = get_mask_outline(player.image,(1,1))
    player_mask.convert_alpha()
    pygame.event.set_allowed([QUIT, KEYDOWN, KEYUP])
    running = 1
    screen.fill((255,255,255))
    level_surface = background.render(screen)
    level_mask = pygame.mask.from_surface(level_surface,threshold=127)
    #level_mask.invert()
    level_mask_surface = level_mask.to_surface()

    while running:
        previous_time = time.time()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = 0
                    pygame.quit()
                    sys.exit()

                if event.key == pygame.K_w or pygame.K_UP:
                    player.jump()

        screen.fill((255,255,255))
        
        screen.blit(level_surface,(0,0))
        #screen.blit(level_mask_surface,(0,0))
        #screen.blit(player_mask,(player.rect.x,player.rect.y-1))
        player.update(screen,background.group)
        
        pygame.display.flip()
        dt = time.time() - previous_time
        clock.tick(FPS-dt)

if __name__ == "__main__":
    main()
