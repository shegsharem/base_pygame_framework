# pylint: disable=maybe-no-member
import sys
import pygame
from pygame.locals import *

# Game Modules
from src.shapes import Circle, Rectangle
from src.deltatime import get_deltatime
from src.player import Player
from src.level import Level
from src.collisions import intersecting_rect_with_sprite_group
from src.lighting import get_outline_basic

pygame.init()

screen = pygame.display.set_mode((1280,720))
previous_time = get_deltatime()

test_rect = Rectangle((0,0),(50,50), (0,0,0))
test_rect2 = Rectangle((400,400),(100,100),(255,0,0))
test_rect3 = Rectangle((0,0),(100,100),(255,255,0))

test_rect_outline = get_outline_basic(test_rect.image)
#player = Player()
level_map = list(open('level.txt'))

rect_collision_group = pygame.sprite.Group()
rect_collision_group.add(test_rect2,test_rect3)
collided_rect = None

background = Level(level_map)
splashscreen = pygame.image.load('assets/images/background.png').convert_alpha()
splashscreen = pygame.transform.scale(splashscreen, (screen.get_width(), screen.get_height()))

#pygame.event.set_allowed([QUIT, KEYDOWN, KEYUP]) # allows certain inputs to increase performance


def input_processor() -> None:
    """Logic function for pygame events."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    if keys[K_ESCAPE]:
        pygame.quit()
        sys.exit()

    if keys[K_w]:
        player.sprite_number += 1
        player.acceleration.y = -2
        player.touching_ground = True

while True:
    dt, previous_time = get_deltatime(previous_time)

    input_processor()

    screen.blit(splashscreen,(0,0))
    mouse_pos = pygame.mouse.get_pos()


    test_rect.position = mouse_pos


    collided_rect = intersecting_rect_with_sprite_group(test_rect.rect, rect_collision_group)

    test_rect.update(dt)
    #player.update(dt)
    test_rect2.update(dt)
    test_rect3.update(dt)


    screen.blit(test_rect2.image,test_rect2.position)
    screen.blit(test_rect3.image,test_rect3.position)
    screen.blit(test_rect_outline,test_rect.position)
    print(test_rect_outline.get_rect())

    screen.blit(test_rect.image,test_rect.position)
    
    #screen.blit(player.image,player.position)

    if collided_rect:
        print(collided_rect)
        pygame.draw.rect(screen, (0,255,0), collided_rect)


    

    pygame.display.update([test_rect, test_rect2, test_rect3])
    pygame.display.flip()
