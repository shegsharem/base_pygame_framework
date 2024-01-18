"""Level loader"""
from pygame import sprite, Surface
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

