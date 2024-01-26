"""Python 3.12.1"""
from pygame import Rect, sprite, rect

def check_collision_with_sprite_group(target:sprite.Sprite, group:sprite.Group) -> dict[str, bool]:
    collision = sprite.spritecollideany(target,group)
    tolerance = 2
    collisions = {
        "top": False,
        "bottom": False,
        "right": False,
        "left": False,
    }

    if collision:
        if abs(target.rect.bottom-collision.rect.top) < tolerance:
            collisions['bottom'] = True
            target.position.y -=1

        if abs(target.rect.top-collision.rect.bottom) < tolerance:
            collisions['top'] = True
            target.position.y +=1

        elif abs(target.rect.right-collision.rect.left) < tolerance:
            collisions['right'] = True
            target.position.x -=1

        elif abs(target.rect.left-collision.rect.right) < tolerance:
            collisions['left'] = True
            target.position.x +=1
    return collisions

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
