"""Module for lines and curves in pygame"""
from pygame import Surface, draw
from pygame.locals import SRCALPHA

def mesh(points:list) -> Surface:
    """Create mesh of lines given a list of point coordinates

    :param points: `list[(x,y)]`
    :type points: list
    :return: `mesh surface`
    :rtype: Surface
    """
    width  = max(point[0] for point in points)
    height = max(point[1] for point in points)
    surface = Surface((width,height),SRCALPHA)
    draw.lines(surface,(255,255,255), False, points)
    return surface
