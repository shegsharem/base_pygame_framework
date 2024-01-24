"""Level loader"""
from pygame import sprite, Surface, mask, image, transform
from pygame.locals import SRCALPHA

class Level:
    """Level class. Block sprites shall be 10x10px"""
    def __init__(self, level_map:list) -> None:
        self.level_map = level_map
        self.terrain_group = sprite.Group()
        dirt = transform.scale(image.load("assets/images/dirt.png").convert_alpha(), (36,36))
        grass = transform.scale(image.load("assets/images/grass.png").convert_alpha(), (36,36))

        for row_index, row in enumerate(self.level_map):
            for col_index, cell in enumerate(row):
                x = -36 + int(col_index*36)
                y = -36 + int(row_index*36)

                # Dirt
                if cell == "D":
                    self.terrain = sprite.Sprite()
                    self.terrain.image = dirt
                    self.terrain.rect = self.terrain.image.get_rect().move(x,y)
                    self.terrain_group.add(self.terrain)

                # Grass
                if cell == "G":
                    pass
                    #self.terrain = sprite.Sprite()
                    #self.terrain.image = grass
                    #self.terrain.rect = self.terrain.image.get_rect().move(x,y)
                    #self.terrain_group.add(self.terrain)

                if cell == " ":
                    pass


    def render_terrain(self, screen:Surface) -> Surface:
        """Render level to pygame surface, relative to game window size

        Args:
            screen (Surface): Game window

        Returns:
            Surface: Rendered level
        """
        level_surface = Surface((screen.get_width(),screen.get_height()),SRCALPHA)
        for tile in self.terrain_group:
            level_surface.blit(tile.image, tile.rect)
        level_surface.convert_alpha()

        return level_surface
