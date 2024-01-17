"""Menu"""
import sys
import pygame
from button import Button
from font import Font


class Menu:
    """Game menu"""
    def __init__(self, surface:pygame.Surface, frame_rate:int=60) -> None:
        self.screen = surface
        self.rect = self.screen.get_rect()
        self.clock = pygame.time.Clock()
        self.fps = frame_rate
        self.running = False
        self.background_color = (56,56,56)

    def kill(self) -> None:
        """Kill main loop"""
        self.running = False

    def run(self) -> None:
        """Run instance"""
        self.running = True
        pygame.event.clear() # clear event queue

        menu_title = Font().render("Game", size_factor=2,text_color=(255,255,255))

        play_button = Button(
            text="Play",x=25,y=self.screen.get_height()-120,
            width=90, height=60,button_color =(65,65,65),text_size_factor=3,
            button_highlighted_color=(95,95,95),
            text_color=(255,255,255), button_border_radius=4,
            callback=self.kill
        )

        editor_button = Button(
            text="Editor",x=25,y=self.screen.get_height()-50,
            width=90, height=35,
            button_color =(55,55,55),text_size_factor=2,
            button_highlighted_color=(95,95,95),
            text_color=(255,255,255), button_border_radius=7,
            callback=self.kill
        )

        exit_button = Button(
            width=25,height=25,
            text="x",button_color= self.background_color,
            button_highlighted_color=(255,0,0),
            text_size_factor=2,text_color=(255,255,255),
            callback=self.kill, anchor='topright'
        )

        self.screen.fill(self.background_color)

        while self.running:
            
            self.screen.blit(menu_title, (5,7))
            exit_button.update(self.screen)
            play_button.update(self.screen)
            editor_button.update(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.flip()
            self.clock.tick(self.fps)
