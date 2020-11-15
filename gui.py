import pygame
import time

# init pygame
pygame.init()

# display parameters
DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 600

# declare fonts
LARGE_FONT_SIZE = 60
MID_FONT_SIZE = 50
SMALL_FONT_SIZE = 20
GAME_FONT_PATH = 'fonts/pdark.ttf'
REGULAR_FONT_PATH = 'fonts/ShareTechMono-Regular.ttf'
TITLE_FONT = pygame.font.Font(GAME_FONT_PATH, LARGE_FONT_SIZE)
BUTTON_FONT = pygame.font.Font(REGULAR_FONT_PATH, SMALL_FONT_SIZE)

# default position for titles
TITLE_POS = (DISPLAY_WIDTH/2, LARGE_FONT_SIZE)

# default button dimensions
BUTTON_WIDTH = 120
BUTTON_HEIGHT = 40

class Button:

    def __init__(self, rect, text_surf, text_rect, color, callback, kwargs=None):
        self.rect = rect
        self.text_surf = text_surf
        self.text_rect = text_rect
        self.color = color
        self.callback = callback
        self.kwargs = kwargs

class GUI:

    def __init__(self, title, display_width=DISPLAY_WIDTH, display_height=DISPLAY_HEIGHT):
        # create the game screen
        self.screen = pygame.display.set_mode((display_width, display_height))
        # set window title
        pygame.display.set_caption(title)
        # game clock
        self.clock = pygame.time.Clock()

    def display_text(self, font, message, color, center):
        text_surface = font.render(message, True, color)
        text_rect = text_surface.get_rect(center=center)
        self.screen.blit(text_surface, text_rect)
        return text_surface, text_rect

    def display_image(self, image, location=(0,0)):
        img = pygame.image.load(image)
        self.screen.blit(img, location)

    def draw_button(self, screen, button):
        pygame.draw.rect(screen, button.color, button.rect)
        screen.blit(button.text_surf, button.text_rect)

    def create_button(self, title, x,y,width,height, callback, args=None):
        text_mid_point_x = x + width/2
        text_mid_point_y = y + height/2
        button_rect = pygame.Rect(x,y,width,height)
        text_surface, text_rect = self.display_text(BUTTON_FONT, title, WHITE, button_rect.center)
        button = Button(
            button_rect,
            text_surface,
            text_rect,
            DARK_BLUE,
            callback,
            args
        )
        return button
            
    def game_quit(self):
        pygame.quit()
        quit()

if __name__ == "__main__":
    g = GUI('A new window')
    pygame.display.update()
    while True:
        g.screen.fill(BLACK) 
        g.display_text(TITLE_FONT, 'LAUNCHER', RED, TITLE_POS)
        pygame.display.update()
        g.clock.tick(60)
    