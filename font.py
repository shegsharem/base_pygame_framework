""" python 3.12.1 """
import pygame

class Font:
    """Custom font generator from a png image"""
    def __init__(self, font_path:str='data/images/font.png') -> None:
        self.character_spacing = 1
        current_character_width = 0
        character_clip_count = 0

        font_image = pygame.image.load(font_path).convert_alpha()
        self.characters = {}

        self.character_map = [
            "A","B","C","D","E","F","G","H","I",
            "J","K","L","M","N","O","P","Q","R",
            "S","T","U","V","W","X","Y","Z","a",
            "b","c","d","e","f","g","h","i","j",
            "k","l","m","n","o","p","q","r","s",
            "t","u","v","w","x","y","z","1","2",
            "3","4","5","6","7","8","9","0","?",
            "/","!",".",",",":",";","\"","(",")",
            "[","]","<",">","-","+","=","%","@",
            "#","_","$","'","&","*"
        ]

        for pixel in range(font_image.get_width()):
            pixel_color = font_image.get_at((pixel,0)) # Returns color of pixel
            if pixel_color == (255,0,0):

                clipped_character_image = clip(
                    font_image, (pixel-current_character_width), 0,
                    current_character_width, font_image.get_height()
                )

                self.characters[self.character_map[character_clip_count]] = clipped_character_image
                character_clip_count += 1
                current_character_width = 0
            else:
                current_character_width += 1

        self.character_space_width = self.characters["!"].get_width()

    def __str__(self) -> str:
        return f'{self.characters}'

    def render(self,text:str,
               location:tuple=(0,0),
               size_factor:int=1,
               text_color:pygame.Color=None) -> pygame.Surface:
        """Renders text to pygame surface using loaded font

        Args:
            text (str): Text to render
            location (tuple, optional): Location on surface to render text (x,y).
                Note: May clip text if not (0,0). Defaults to (0,0).
            size_factor (int, optional): Text size multiplier. Defaults to 1.
            text_color (pygame.Color, optional): Text color. Defaults to (0,0,0), black.
        
        Returns:
            (pygame.Surface): Pygame surface with rendered text
        """
        x_offset = 0
        text_surface_list = []

        for character in text:
            if character != " ":

                text_surface_list.append(
                    (self.characters[character],
                    (location[0]+x_offset,location[1]))
                )

                x_offset += (self.characters[character].get_width()+1)*size_factor
            else:
                x_offset += 4*size_factor

        if size_factor > 1:
            for index,character in enumerate(text_surface_list):
                character_surface = character[0]

                text_surface_list[index] = (
                    pygame.transform.scale_by(character_surface,size_factor),
                    text_surface_list[index][1]
                )

        text_surface = pygame.Surface(
            (x_offset-size_factor,
            text_surface_list[-1][0].get_height()),
            pygame.SRCALPHA
        )

        text_surface.blits(text_surface_list)
        text_surface_rect = text_surface.get_bounding_rect()

        text_surface = clip(
            text_surface,
            text_surface_rect.x,
            text_surface_rect.y,
            text_surface_rect.width,
            text_surface_rect.height
        )

        if text_color:
            text_surface.fill(text_color,special_flags=pygame.BLEND_RGB_MAX)
            return text_surface
        return text_surface

def clip(surface:pygame.Surface, x:int, y:int, width:int, height:int) -> pygame.Surface:
    """Clipping function for pygame surfaces

    Args:
        surface (pygame.Surface): Surface to clip from
        x (int): x-position of clip
        y (int): y-position of clip
        width (int): width of clip
        height (int): height of clip

    Returns:
        pygame.Surface: New clipped surface
    """
    surface_copy = surface.copy()
    surface_copy.set_clip(pygame.Rect(x,y,width,height))
    return surface.subsurface(surface_copy.get_clip()).copy()
