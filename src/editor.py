import pygame
from button import Button
from font import Font

class Editor:
    """Game menu"""
    def __init__(self, surface:pygame.Surface, frame_rate:int=60) -> None:
        self.screen = surface
        self.rect = self.screen.get_rect()
        self.clock = pygame.time.Clock()
        self.fps = frame_rate
        self.running = False
        self.background_color = (56,56,56)

    def kill(self) -> None:
        self.running = False

    def run(self):
        """Run instance"""
        self.running = True
        pygame.event.clear() # clear event queue

        self.screen.fill(self.background_color)

        pixel_text =  Font().render("- Pixel -", size_factor=2,text_color=(255,255,255))
        editor_text = Font().render("Art Editor", size_factor=2,text_color=(255,255,255))

        options_frame = pygame.draw.rect(
            self.screen,(64,64,64),
            (10,55,100,
            self.screen.get_height()-80),
            border_radius=15
        )

        new_button = Button(
            x=15,y=60,
            width=90,height=40,
            text="New",button_color= (56,56,56),
            button_highlighted_color=(80,80,80),
            text_size_factor=2,text_color=(255,255,255),
            button_border_radius=7,callback=self.kill
        )

        open_button = Button(
            x=15,y=105,
            width=90,height=40,
            text="Open",button_color= (56,56,56),
            button_highlighted_color=(80,80,80),
            text_size_factor=2,text_color=(255,255,255),
            button_border_radius=7,callback=self.kill
        )

        exit_button = Button(
            x=0,y=0,
            width=25,height=25,
            text="x",button_color= self.background_color,
            button_highlighted_color=(255,0,0),
            text_size_factor=2,text_color=(255,255,255),
            callback=self.kill, anchor='topright'
        )

        while self.running:
            deltatime = 0
            last_time = time.time()

            self.screen.blit(pixel_text, (19,self.screen.get_rect().top+5))
            self.screen.blit(editor_text, (10,self.screen.get_rect().top+25))
            new_button.update(self.screen)
            open_button.update(self.screen)
            exit_button.update(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.flip()
            deltatime = self.fps - (time.time()-last_time)
            self.clock.tick(deltatime)