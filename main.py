import importlib
import pygame
import gui

# get lists of games
try:
    import config
except ModuleNotFoundError:
    print('Error: Config file not found')
    exit(0)

# Window title
APP_TITLE = 'Card Games'

# launcher title
TITLE = 'GAME LAUNCHER'

# quit button position
QUIT_BUTTON_POS = (40, 520, gui.BUTTON_WIDTH, gui.BUTTON_HEIGHT)

# game list properties
ROWS = 6
COLUMNS = 5
START_x_POS = 49
START_y_POS = 120
BUTTON_SPACING = 20
MAX_GAMES = 30

class GameLauncher:

    def __init__(self):
        # initialize the gui
        self.g = gui.GUI(APP_TITLE)

    def launch_game(self, kwargs):
        try:
            module = kwargs['game']
            game = importlib.import_module('games.{}'.format(module))
            card_game = game.CardGame(kwargs['gui'])
            card_game.start()
        except ModuleNotFoundError as e:
            print('Error: Unable to launch game. {}'.format(e))

    def start(self):
        # start the launcher loop
        self.loop()

    def load_game_list(self):
        '''
        load list of games, max: 30
        '''
        # generate locations for games launcher buttons
        locations = []
        for j in range(6):
            for i in range(5):
                x = START_x_POS + ((gui.BUTTON_WIDTH + BUTTON_SPACING) * i)
                y = START_y_POS + ((gui.BUTTON_HEIGHT + BUTTON_SPACING) * j)
                locations.append((x, y))
        # generate buttons
        buttons = []
        for i, game in enumerate(config.games[:MAX_GAMES]):
            buttons.append(
                self.g.create_button(game['name'], *locations[i], gui.BUTTON_WIDTH, gui.BUTTON_HEIGHT, self.launch_game, 
                {
                    'game':game['module'],
                    'gui': self.g
                })   
            )
        return buttons

    def loop(self):
        
        # create list of buttons for the launcher screen
        buttons = [
            self.g.create_button('QUIT', *QUIT_BUTTON_POS, self.g.game_quit)
        ]

        games_list = self.load_game_list()

        buttons.extend(games_list)

        while True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_quit()
                elif event.type == pygame.MOUSEMOTION:
                    for button in buttons:
                        if button.rect.collidepoint(event.pos):
                            button.color = gui.LIGHT_BLUE
                        else:
                            button.color = gui.DARK_BLUE
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for button in buttons:
                        if button.rect.collidepoint(event.pos):
                            if button.kwargs:
                                button.callback(button.kwargs)
                            else:
                                button.callback()

            self.g.screen.fill(gui.BLACK) 
            self.g.display_text(gui.TITLE_FONT, TITLE, gui.RED, gui.TITLE_POS)
            for button in buttons:
                self.g.draw_button(self.g.screen, button)
            pygame.display.update()
            self.g.clock.tick(60)
            

    def game_quit(self):
        pygame.quit()
        quit()

if __name__ == "__main__":
    launcher = GameLauncher()
    launcher.start()