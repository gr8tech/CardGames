import pygame

# game parameters
GAME_WIDTH = 1200
GAME_HEIGHT = 800
GAME_TITLE = 'Jocker Jail Break'
GAME_FPS = 60

# screen parameters
SCREEN_BACKGROUND = pygame.Color('lavenderblush4')
X_0 = GAME_WIDTH/2
Y_0 = GAME_HEIGHT/2

# card parameters
CARD_WIDTH = 157
CARD_HEIGHT = 222
CARD_SCALE_FACTOR = 0.75
CARD_SPACING = 3
# deck settings
DECK_SPACING = 20

# button parameters
BUTTON_ACTIVE_COLOR = pygame.Color('lightblue')
BUTTON_INACTIVE_COLOR = pygame.Color('blue')
BUTTON_WIDTH = 120
BUTTON_HEIGHT = 40

# walls and pillars highlighted color
HIGHLIGHTED = pygame.Color((255,0,0,128))

# font sizes
LARGE_FONT_SIZE = 60
MID_FONT_SIZE = 50
SMALL_FONT_SIZE = 20

# Game Assets
GAME_FONT_PATH = 'assets/fonts/pdark.ttf'
REGULAR_FONT_PATH = 'assets/fonts/ShareTechMono-Regular.ttf'
JOKER_IMAGE = 'joker.png'
DECK_BACK_IMAGE = 'assets/cards/deck.png'
HELP_IMAGE = 'assets/help.png'
CARDS = 'assets/cards/'

