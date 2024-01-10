""" python 3.12.1 """
import pygame
from font import Font

class Button:
    """Simple button class."""

    def __init__(self, x:int=0, y:int=0,
                 width:int=10, height:int=10,
                 button_color:tuple=(255,255,255),
                 button_highlighted_color:tuple=(255,255,255),
                 text:str=None, text_size_factor:int=1,
                 text_color:tuple=None, button_border_radius:int=0,
                 anchor:str=None, callback=None) -> None:
        """Create button rect

        Args:
            x (int, optional): x-position. Not needed with anchor.
            y (int,optional): y-position. Not needed with anchor.
            width (int, optional): button width. Defaults to 10.
            height (int): button height. Defaults to 10.
            button_color (tuple, optional): Button color. Defaults to (255,255,255).
            button_hightlighted_color (tuple, optional): Button highlighted color.
                Defaults to (255,255,255).
            text (str, optional): text. Defaults to None.
            text_size_factor (int, optional): Text size multiplier. Defaults to 1.
            text_color (tuple, optional): Text color. Defaults to None.
            button_border_radius (int, optional): Button corner radius. Defaults to 0.
            anchor (optional): location to anchor button
            Callback: Button callback for when clicked
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.corner_radius = button_border_radius
        self.anchor = anchor

        self.color = pygame.Color(button_color)
        self.text_color = pygame.Color(text_color)
        self.highlighted_color = pygame.Color(button_highlighted_color)
        self.selected_color = self.highlighted_color.lerp((
            abs(self.color[0]-10),
            abs(self.color[1]-10),
            abs(self.color[2]-10)),1
        )
        self.set_color = self.color

        self.text = text
        self.text_size_factor = text_size_factor

        self.callback = callback
        self.button:pygame.Surface = self.create_button(self.color)

    def create_button(self, color:tuple=(0,0,0,0)) -> pygame.Surface:
        """Create button"""
        if self.text:
            text_surface = Font().render(
                text=self.text,
                size_factor=self.text_size_factor,
                text_color=self.text_color
            )

            text_surface_rect = text_surface.get_rect()

            button_surface = pygame.Surface(
                (text_surface_rect.width+self.text_size_factor*10,
                text_surface_rect.height+self.text_size_factor*10),
                pygame.SRCALPHA
            )

            button_surface_rect = button_surface.get_rect()
            text_surface_rect.center = button_surface_rect.center

            pygame.draw.rect(
                surface=button_surface,
                color=color,
                rect=button_surface_rect,
                border_radius=self.corner_radius*self.text_size_factor
            )

            button_surface.blit(text_surface,text_surface_rect)
            return button_surface

        button_surface = pygame.Surface((self.width, self.height),pygame.SRCALPHA)
        button_surface_rect = button_surface.get_rect()

        pygame.draw.rect(
                surface=button_surface,
                color=color,
                rect=button_surface_rect,
                border_radius=self.corner_radius*self.text_size_factor
            )

        return button_surface

    def update(self, screen:pygame.Surface) -> pygame.Rect:
        """Update button and draw on screen"""
        button_mask = get_mask(self.button)
        button_mask_rect = button_mask.get_rect().move(self.x,self.y)
        mouse_hover = check_mouse_hover(
            button_mask,
            button_mask_rect
        )
        current_button_color = get_color_from_surface(self.button)
        mouse_down = pygame.mouse.get_pressed()[0]

        if mouse_hover:
            if not mouse_down and self.set_color == self.selected_color:
                if callable(self.callback):
                    self.callback()
            elif mouse_down:
                self.set_color = self.selected_color
            else:
                self.set_color = self.highlighted_color

        if not mouse_hover:
            if self.set_color == self.selected_color:
                if not mouse_down:
                    self.set_color = self.color
        

        if self.set_color != current_button_color:
            self.button = self.create_button(self.set_color)
        #button = self.button(self.color)

        if self.anchor:
            screen_rect, button_rect = screen.get_rect(), self.button.get_rect()

            if self.anchor == 'topleft':
                button_rect.topleft = screen_rect.topleft
                self.x, self.y = button_rect.x, button_rect.y
                return screen.blit(self.button,(self.x,self.y))

            if self.anchor == 'topright':
                button_rect.topright = screen_rect.topright
                self.x, self.y = button_rect.x, button_rect.y
                return screen.blit(self.button,(self.x,self.y))

            if self.anchor == 'center':
                button_rect.center = screen_rect.center
                self.x, self.y = button_rect.x, button_rect.y
                return screen.blit(self.button,(self.x,self.y))

            if self.anchor == 'bottomleft':
                button_rect.bottomleft = screen_rect.bottomleft
                self.x, self.y = button_rect.x, button_rect.y
                return screen.blit(self.button,(self.x,self.y))

            if self.anchor == 'bottomright':
                button_rect.bottomright = screen_rect.bottomright
                self.x, self.y = button_rect.x, button_rect.y
                return screen.blit(self.button,(self.x,self.y))

        return screen.blit(self.button,(self.x,self.y))

def check_mouse_hover(button_mask, button_mask_rect) -> bool:
    """Check if mouse is hovering button"""
    mouse_position = pygame.mouse.get_pos()

    if button_mask_rect.collidepoint(mouse_position):
        if button_mask.get_at(
            (mouse_position[0]-button_mask_rect.x,
             mouse_position[1]-button_mask_rect.y)):
            return True
    return False

def get_mask(surface:pygame.Surface) -> pygame.Mask:
    """Get surface mask"""
    return pygame.mask.from_surface(surface)

def get_color_from_surface(surface:pygame.Surface) -> pygame.Color:
    """Get color from surface"""
    return surface.get_at(surface.get_rect().topleft)
