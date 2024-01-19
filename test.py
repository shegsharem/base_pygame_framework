import sys
import time
import pygame
from pygame.locals import *
from src.level import Level

pygame.init()
screen = pygame.display.set_mode((1280,720),pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.NOFRAME)
level_map = list(open('level.txt'))
background = Level(level_map)

velocity = pygame.Vector2(0,-20)

clock = pygame.time.Clock()
#player = Player() when player is external file
FPS = 1

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.rect = pygame.Rect((0,400,10,10))

    def move(self):
        self.rect.move_ip(velocity)

    def draw(self, surface:pygame.Surface):
        self.move()
        vector = pygame.Vector2(velocity.x + self.rect.centerx, velocity.y + self.rect.centery)
        pygame.draw.line(surface,(0,0,0),self.rect.center, vector,1)
        pygame.draw.rect(surface, (255,0,0), self.rect)


def main() -> None:
    """Main game loop"""
    pygame.event.set_allowed([QUIT, KEYDOWN, KEYUP])
    player = Player()
    running = 1

    screen.fill((255,255,255))

    level_surface = background.render(screen)
    level_collision_mask = background.render_level_mask_outlines(screen)

    

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

                if event.key == pygame.K_s or pygame.K_DOWN:
                    velocity.y += 1

        screen.fill((200,200,200))

        screen.blit(level_collision_mask[0],(10,-10))
        screen.blit(level_surface,(0,0))

        player.draw(screen)
        velocity.x = 20
        velocity.y += 1
        pygame.display.flip()
        dt = time.time() - previous_time
        clock.tick(FPS-dt)

if __name__ == "__main__":
    main()
