"""Level loader"""
from pygame import sprite, Surface, mask
from pygame.locals import SRCALPHA

class Level:
    """Level class. Block sprites shall be 5x5px"""
    def __init__(self, level_map:list) -> None:
        self.level_map = level_map
        self.group = sprite.Group()

        for row_index, row in enumerate(self.level_map):
            for col_index, cell in enumerate(row):
                x = -10 + int(col_index*10)
                y = -10 + int(row_index*10)

                # Dirt
                if cell == "D":
                    self.terrain = sprite.Sprite()
                    self.terrain.image = Surface((10,10))
                    self.terrain.rect = self.terrain.image.get_rect().move(x,y)
                    self.group.add(self.terrain)

                if cell == " ":
                    pass


    def render(self, screen:Surface) -> Surface:
        """Render level to pygame surface, relative to game window size

        Args:
            screen (Surface): Game window

        Returns:
            Surface: Rendered level
        """
        level_surface = Surface((screen.get_width(),screen.get_height()),SRCALPHA)
        for tile in self.group:
            level_surface.blit(tile.image, tile.rect)
        #level_surface.convert_alpha()
        return level_surface

    def render_level_mask_outlines(self, screen: Surface):
        top_surfaces = Surface((screen.get_width(),screen.get_height()),SRCALPHA)
        bottom_surfaces = Surface((screen.get_width(),screen.get_height()),SRCALPHA)
        left_surfaces = Surface((screen.get_width(),screen.get_height()),SRCALPHA)
        right_surfaces = Surface((screen.get_width(),screen.get_height()),SRCALPHA)

        level = self.render(screen)
        surface_mask = mask.from_surface(level)
        surface_mask.invert()
        mask_to_surface = surface_mask.to_surface()

        top_surfaces.blit(mask_to_surface,(0,-1))
        top_surfaces.blit(level,(0,0))
        top_surfaces.convert_alpha()

        bottom_surfaces.blit(mask_to_surface,(0,1))
        bottom_surfaces.blit(level,(0,0))
        bottom_surfaces.convert_alpha()

        left_surfaces.blit(mask_to_surface,(-1,0))
        left_surfaces.blit(level,(0,0))
        #left_surfaces.convert_alpha()

        right_surfaces.blit(mask_to_surface,(1,0))
        right_surfaces.blit(level,(0,0))
        #right_surfaces.convert_alpha()


        return (top_surfaces, bottom_surfaces, left_surfaces, right_surfaces)