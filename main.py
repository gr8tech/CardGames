import pygame
import importlib

# get lists of games
try:
    import config
except ModuleNotFoundError:
    print('Error: Config file not found')
    exit(0)

# init pygame
pygame.init()
    
APP_TITLE = 'Card Games'

# display parameters
DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 600

# declare colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
OFFWHITE = (180, 180, 180)
BLACK = (0, 0, 0)
DARK_BLUE = (33, 40, 227)
LIGHT_BLUE = (99, 103, 231)

# declare fonts
LARGE_FONT_SIZE = 80
MID_FONT_SIZE = 50
SMALL_FONT_SIZE = 20
GAME_FONT = 'fonts/pdark.ttf'
REGULAR_FONT = 'fonts/ShareTechMono-Regular.ttf'


TITLE_FONT = pygame.font.Font(GAME_FONT, LARGE_FONT_SIZE)
BUTTON_FONT = pygame.font.Font(REGULAR_FONT, SMALL_FONT_SIZE)

TITLE_POS = (DISPLAY_WIDTH/2, LARGE_FONT_SIZE/2)
QUIT_BUTTON_DIM = (40, 520, 80, 40)

BUTTON_WIDTH = 120
BUTTON_HEIGHT = 40

class Button:

    def __init__(self, rect, text_surf, text_rect, color, callback, args=None):
        self.rect = rect
        self.text_surf = text_surf
        self.text_rect = text_rect
        self.color = color
        self.callback = callback
        self.args = args

class GameLauncher:

    def __init__(self):
        self.game_display = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
        pygame.display.set_caption(APP_TITLE)

    # def text_objects(self, message, font, color):
    #     text_surface = font.render(message, True, color)
    #     return text_surface, text_surface.get_rect()

    def display_text(self, font, message, color, center):
        text_surface = font.render(message, True, color)
        text_rect = text_surface.get_rect(center=center)
        self.game_display.blit(text_surface, text_rect)
        return text_surface, text_rect

    def display_image(self, image, location=(0,0)):
        img = pygame.image.load(image)
        self.game_display.blit(img, location)

    def draw_button(self, screen, button):
        pygame.draw.rect(screen, button.color, button.rect)
        screen.blit(button.text_surf, button.text_rect)

    def create_button(self, title, x,y,width,height, callback, args=None):
        text_mid_point_x = x + width/2
        text_mid_point_y = y + height/2
        button_rect = pygame.Rect(x,y,width,height)
        text_surface, text_rect = self.display_text(BUTTON_FONT, title, WHITE, button_rect.center)
        # text_surface = BUTTON_FONT.render(title, True, WHITE)
        # text_rect = text_surface.get_rect(center=button_rect.center)
        button = Button(
            button_rect,
            text_surface,
            text_rect,
            DARK_BLUE,
            callback,
            args
        )
        return button

    def launch_game(self, module):
        try:
            game = importlib.import_module('games.{}'.format(module))
            card_game = game.CardGame()
            card_game.start()
        except ModuleNotFoundError as e:
            print('Error: Unable to launch game. {}'.format(e))

    def start(self):
        self.loop()

    def loop(self):
        clock = pygame.time.Clock()
        
        buttons = [
            self.create_button('QUIT', *QUIT_BUTTON_DIM, self.game_quit)
        ]

        # load list of games, max: 30
        locations = []
        for j in range(6):
            for i in range(5):
                x = 49 + ((BUTTON_WIDTH + 20) * i)
                y = 120 + ((BUTTON_HEIGHT + 20) * j)
                locations.append((x, y))
        for i, game in enumerate(config.games[:30]):
            print(game['module'])
            buttons.append(
                self.create_button(game['name'], *locations[i], BUTTON_WIDTH, BUTTON_HEIGHT, self.launch_game, game['module'])   
            )
  

        while True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_quit()
                elif event.type == pygame.MOUSEMOTION:
                    for button in buttons:
                        if button.rect.collidepoint(event.pos):
                            button.color = LIGHT_BLUE
                        else:
                            button.color = DARK_BLUE
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for button in buttons:
                        if button.rect.collidepoint(event.pos):
                            if button.args:
                                button.callback(button.args)
                            else:
                                button.callback()


            self.game_display.fill(BLACK) 
            self.display_text(TITLE_FONT, 'LAUNCHER', RED, TITLE_POS)
            for button in buttons:
                self.draw_button(self.game_display, button)
            pygame.display.update()
            clock.tick(60)
            

    def game_quit(self):
        pygame.quit()
        quit()

if __name__ == "__main__":
    launcher = GameLauncher()
    launcher.start()