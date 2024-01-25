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
from src.lighting import get_outline
from src.curves import mesh
import math

pygame.init()

screen = pygame.display.set_mode((1280,720), DOUBLEBUF)
previous_time = get_deltatime()

test_rect = Rectangle((0,0),(50,50), (0,0,0))

test_rect_outline = get_outline(test_rect.image)
#player = Player()
level_map = list(open('level.txt'))

background = Level(level_map)
level_terrain = background.render_terrain(screen)
level_outline = get_outline(level_terrain)
splashscreen = pygame.image.load('assets/images/background.png').convert_alpha()
splashscreen = pygame.transform.scale(splashscreen, (screen.get_width(), screen.get_height()))

points = [
    (100,100),(500,100),
    (300,400),(100,100),
    (300,200),(500,100),
    (300,200),(300,400)
]

quadratic = []
xs = []
for x in range(-200,200):
    xs.append(x)

for x,y in enumerate(xs):
    quadratic.append((x,math.pow(1/10*y,2)))

point_mesh = mesh(quadratic)


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
        pass
        #player.sprite_number += 1
        #player.acceleration.y = -2
        #player.touching_ground = True

y=0
while True:
    dt, previous_time = get_deltatime(previous_time)

    print(dt)
    input_processor()

    mouse_pos = pygame.mouse.get_pos()

    test_rect.position = mouse_pos

    test_rect.update(dt)
    #player.update(dt)

    screen.blit(splashscreen,(0,0))
    screen.blit(level_terrain,(0,0))
    screen.blit(level_outline,(0,0))

    screen.blit(test_rect.image,test_rect.position)
    screen.blit(test_rect_outline,test_rect.position)
    screen.blit(point_mesh, (200,200))
    y+=10*dt

    #screen.blit(player.image,player.position)

    pygame.display.flip()
