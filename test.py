import sys
import time
import pygame
from pygame.locals import *
from src.level import Level
from lighting import get_outline

pygame.init()
screen = pygame.display.set_mode((1920,1080),pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.NOFRAME)
level_map = list(open('level.txt'))

background = Level(level_map)
splashscreen = pygame.image.load('assets/images/background.png').convert_alpha()
splashscreen = pygame.transform.scale(splashscreen, (screen.get_width(), screen.get_height()))

clock = pygame.time.Clock()
#player = Player() when player is external file
FPS = 500

def intersecting_rect_with_rect_group(
        rect:pygame.Rect, collidable_group:pygame.sprite.Group) -> pygame.Rect:
    """Iterate through sprite group to find the minimum distances from the player"""
    checklist = []

    for sprite in collidable_group:
        if rect.colliderect(sprite.rect):
            checklist.append(sprite.rect)

    if not checklist:
        return None

    x = max(max(r.x for r in checklist),rect.x)
    width = min(min(r.right for r in checklist),rect.width) - x
    y = max(max(r.y for r in checklist),rect.y)
    height = min(min(r.bottom for r in checklist),rect.bottom) - y

    return pygame.Rect(x,y,width,height)

class Player(pygame.sprite.Sprite):
    """Player Class"""
    def __init__(self) -> None:
        super().__init__()

        # Player Flags #######
        self.sprite_number = 0
        self.flipped = False
        self.touching_ground = False
        self.moving_left = False
        self.moving_right = True
        ######################

        # Player Variables ##########################
        self.velocity = pygame.Vector2(0,0)
        self.friction = 0.2
        #############################################

        # Build sprite list:
        # {Sprite Number: (Image, Rect)} ##########################################################
        self.player_sprites = {}

        for i in range(6):
            image = pygame.transform.scale_by(
                pygame.image.load('assets/images/player/player'+str(i)+'.png').convert_alpha(),3)

            self.player_sprites[i] = image, image.get_bounding_rect()
        ###########################################################################################

    def move(self, rect:pygame.Rect, velocity) -> None:
        """Move rect by a velocity"""
        rect.move_ip(velocity)
        return rect

    def update(self, collidable_group:pygame.sprite.Group=None) -> [pygame.Surface, pygame.Rect]:
        """Updates player image and rect"""
        # Update player image ####################################################################
        if self.moving_left:
            image = pygame.transform.flip(self.player_sprites[self.sprite_number][0], True, False)
        else: image = self.player_sprites[self.sprite_number][0]
        ##########################################################################################

        rect:pygame.Rect = self.player_sprites[self.sprite_number][1]

        # Velocity limiter
        if self.velocity.y > 47:
            self.velocity.y = 47

        rect = self.move(rect,self.velocity)

        # Check for collisions ######################################
        collision_rect = intersecting_rect_with_rect_group(rect,collidable_group)
        
        if collision_rect is not None:
            if self.velocity.y > 0:
                self.velocity.y = 0
                rect.bottom = collision_rect.top
                self.touching_ground = True
        
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

        #if moving_left:

        else:
            self.touching_ground = False
            rect = self.move(rect,self.velocity)

        return image,rect


def main() -> None:
    """Main game loop"""
    pygame.event.set_allowed([QUIT, KEYDOWN, KEYUP])
    player = Player()
    running = 1

    screen.fill((0,0,0))

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

                if event.key == pygame.K_w:
                    player.velocity.y -= 20

                elif event.key == pygame.K_d:
                    player.velocity.x += 10
                    player.moving_right = True
                    player.moving_left = False
                
                elif event.key == pygame.K_a:
                    player.velocity.x -= 10
                    player.moving_left = True
                    player.moving_right = False

        level_terrain = background.render_terrain(screen)
        level_collision_mask = get_outline(level_terrain)
        
        player.velocity.y += 1

        player_image, player_rect = player.update(background.terrain_group)

        screen.blit(splashscreen, (0,0))
        screen.blit(level_collision_mask,(0,0))
        screen.blit(level_terrain,(0,0))

        screen.blit(player_image, player_rect)

        pygame.display.flip()
        dt = time.time() - previous_time
        clock.tick(FPS-dt)

if __name__ == "__main__":
    main()
