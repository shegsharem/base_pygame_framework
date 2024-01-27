"""Python 3.12.1"""
from pygame import Rect, sprite

def check_collision_with_sprite_group(target:sprite.Sprite, group:sprite.Group) -> dict[str, bool]:
    """Check collisions between a sprite and a group of sprites

    :param target: `target sprite`
    :type target: sprite.Sprite
    :param group: `sprite group`
    :type group: sprite.Group
    :return: where it has collided
    :rtype: dict[str, bool]
    """
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
            target.rect.bottom = collision.rect.top
            target.position.y = target.rect.y

        if abs(target.rect.top-collision.rect.bottom) < tolerance:
            collisions['top'] = True
            target.rect.top = collision.rect.bottom
            target.position.y = target.rect.y

        if abs(target.rect.right-collision.rect.left) < tolerance:
            collisions['right'] = True
            target.rect.right = collision.rect.left
            target.position.x = target.rect.x

        if abs(target.rect.left-collision.rect.right) < tolerance:
            collisions['left'] = True
            target.rect.left = collision.rect.right
            target.position.x = target.rect.x

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
