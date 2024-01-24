"""Python 3.12.1"""
from pygame import Rect, sprite

def intersecting_rect_with_sprite_group(rect:Rect, sprite_group:sprite.Group) -> Rect | None:
    """Check rect overlapping with any sprite in sprite group

    :param rect: Single `rect`
    :type rect: Rect
    :param sprite_group: `sprite group` to collide with
    :type sprite_group: sprite.Group
    :return: `smallest rect of overlap` if overlapping, otherwise return `None`
    :rtype: Rect | None
    """
    checklist = []

    for group_sprite in sprite_group:
        if rect.colliderect(group_sprite.rect):
            checklist.append(group_sprite.rect)

    if not checklist:
        return None

    x = max(max(r.x for r in checklist),rect.x)
    width = min(min(r.width for r in checklist),rect.width) - x
    y = max(max(r.y for r in checklist),rect.y)
    height = min(min(r.bottom for r in checklist),rect.bottom) - y

    return Rect(x,y,width,height)
