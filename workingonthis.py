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

pygame.init()

screen = pygame.display.set_mode((1280,720))
previous_time = get_deltatime()

test_rect = Rectangle((10,10),(200,200))
test_rect2 = Rectangle((10,10),(100,100),(255,0,0))


test_circle = Circle((0,0),40,(0,9,0))
player = Player()
level_map = list(open('level.txt'))

rect_collision_group = pygame.sprite.Group()
rect_collision_group.add(test_rect2)
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

    screen.fill((0,0,0))
    mouse_pos = pygame.mouse.get_pos()

    #test_rect.position = mouse_pos
    test_rect2.position = (100,100)
    test_circle.position = mouse_pos
    player.position = mouse_pos

    collided_rect = intersecting_rect_with_sprite_group(test_circle.rect, rect_collision_group)

    #test_rect.update(dt)
    player.update(dt)
    test_rect2.update(dt)
    test_circle.update(dt)


    #screen.blit(test_rect.image,test_rect.position)
    screen.blit(test_rect2.image,test_rect2.position)

    if collided_rect:
        print(collided_rect)
        pygame.draw.rect(screen, (0,255,0), collided_rect)


    screen.blit(test_circle.image,test_circle.position)
    screen.blit(player.image,player.position)

    pygame.display.update([test_rect2, player, test_circle])
    pygame.display.flip()
