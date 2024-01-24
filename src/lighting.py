"""Module for lighting and various visual effects in pygame"""
from pygame import Surface, mask
from pygame.locals import SRCALPHA

def get_outline(surface:Surface) -> Surface:
    """Uses pygame masks to return the mask of a surface with a one pixel outline

    Args:
        surface (pygame.Surface): Surface to act on

    Returns:
        pygame.Surface: outline mask
    """
    surface_outline = Surface(surface.get_size(),SRCALPHA)

    new_mask = mask.from_surface(surface)
    mask_surface = new_mask.to_surface(unsetcolor=(0,0,0,0), setcolor=(255,255,255,255))

    surface_outline.blit(mask_surface,(0,-1))
    surface_outline.blit(mask_surface,(0,1))
    surface_outline.blit(mask_surface,(-1,0))
    surface_outline.blit(mask_surface,(1,0))

    surface_outline.convert_alpha()
    return surface_outline
