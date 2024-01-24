"""Module for lighting and various visual effects in pygame"""
from pygame import Surface, mask, draw
from pygame.locals import SRCALPHA

def get_outline(surface:Surface) -> Surface:
    """Get outline of surface using pygame masks.
    Draws outline as a white line (1 pixel wide).

    :param surface: `Surface to outline`
    :type surface: Surface
    :return: `new surface` with outline drawn
    :rtype: Surface
    """
    outline = Surface(surface.get_size(),SRCALPHA)
    outline_mask = mask.from_surface(surface)
    outline_masks = outline_mask.connected_components()

    for partial_mask in outline_masks:
        points = partial_mask.outline()
        draw.lines(outline, (255,255,255,255), True, points)

    return outline
