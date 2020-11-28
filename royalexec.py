import pygame
import random

pygame.init()

# background colors
SNOW4 = pygame.Color('snow4')

# game clock
clock = pygame.time.Clock()

# screen parameters
DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 600

# card parameters
CARD_WIDTH = 80
CARD_HEIGHT = 112
SPRITE_SPACING = 20

# game parameters
TITLE = 'Royal Execution'
FPS = 60

# colors
TITLE_BACKGROUND = pygame.Color((63, 231, 157))
BLACK = pygame.Color('black')

# create game display
SCREEN = pygame.display.set_mode((800, 600))
pygame.display.set_caption(TITLE)

# load fonts and images
try:
    TITLE_FONT = pygame.font.Font('assets/fonts/pdark.ttf', 40)
    SPRITE = pygame.image.load('assets/cards/cards.png').convert_alpha()
except FileNotFoundError:
    print('Error loading game assets')
    pygame.quit()
    quit()

# get deck back image
x = 4 * SPRITE_SPACING + 3 * CARD_WIDTH
y = 5 * SPRITE_SPACING + 4 * CARD_HEIGHT
rect = pygame.rect.Rect(x, y, CARD_WIDTH, CARD_HEIGHT)
DECK_BACK_IMAGE = pygame.surface.Surface((CARD_WIDTH, CARD_HEIGHT))
DECK_BACK_IMAGE.blit(SPRITE, (0,0), rect)
 

# locations
COORD = {
    'draw': (80, 244),
    'discard': (640, 244),
    'hand1': (250, 403),
    'hand2': (360, 403),
    'hand3': (470, 403),
    'royal1': (250, 60),
    'royal2': (360, 60),
    'royal3': (470, 60)
}

class Card:
    
    def __init__(self):
        self.value = value
        self.symbol = symbol
        self.suite = suite

class Hand:
    
    def __init__(self, card, location):
        self.card = card
        self.location = location

class Discard:
    
    def __init__(self, location):
        self.location = location
        self.cards = []

class Royal:
    
    def __init__(self, location):
        self.location = location
        self.cards = []
        self.play = []

class Deck:

    def __init__(self, location):
        self.location = location
        self.cards = []

def quit_game():
    pygame.quit()
    quit()

def create_cards():
    deck = []
    royals = []
    for i, suite in enumerate('CSDHJ'):
        for j in range(1, 14):
            y = ((i + 1) * SPRITE_SPACING) + (i * CARD_HEIGHT)
            x = (j * SPRITE_SPACING) + ((j - 1) * CARD_WIDTH)
            rect = pygame.rect.Rect(x, y, CARD_WIDTH, CARD_HEIGHT)
            image = pygame.surface.Surface((CARD_WIDTH, CARD_HEIGHT))
            image.blit(SPRITE, (0,0), rect)
            # get jokers only form last row
            if i == 4 and j < 2:
                deck.append(image)
            # get non royals only
            if i < 4 and j < 11:
                deck.append(image)
            if i < 4 and j > 10:
                royals.append(image)
    random.shuffle(deck)
    random.shuffle(royals)
    return deck, royals

def display_deck():
    '''
    Displays a stack of cards behind the top cards
    '''
    scaled_count = int(len(deck) / 3) 
    x_0, y_0 = COORD['draw']
    # stack behind the draw deck
    for i in range(scaled_count-1, -1, -1):
        _d = 3 * i
        SCREEN.blit(DECK_BACK_IMAGE, (x_0+_d, y_0-_d))

def display_hands():
    for hand in hands:
        if hand.card == None:
            display_place_holder(hand.location[0], hand.location[1], CARD_WIDTH, CARD_HEIGHT)
        

def display_discard():
    if len(discard.cards) == 0:
        display_place_holder(discard.location[0], discard.location[1], CARD_WIDTH, CARD_HEIGHT)
        
def display_place_holder(x, y, w, h):
    rect = pygame.rect.Rect(x, y, w, h)
    pygame.draw.rect(SCREEN, BLACK, rect, width=1, border_radius=5)
    pygame.draw.circle(SCREEN, BLACK, rect.center, radius=(w/2-5), width=1 )

def display_royals():
    for royal in royals:
        if len(royal.cards) == 0:
            display_place_holder(royal.location[0], royal.location[1], CARD_WIDTH, CARD_HEIGHT)

def display_title():
    # prepare text
    text_surface = TITLE_FONT.render(TITLE, True, BLACK)
    text_rect = text_surface.get_rect()
    text_rect.center = (DISPLAY_WIDTH/2, text_rect.height/2)
    # prepare title background
    rect = pygame.rect.Rect(0, 0, DISPLAY_WIDTH, text_rect.height)
    # draw background
    pygame.draw.rect(SCREEN, TITLE_BACKGROUND, rect)
    # draw text
    SCREEN.blit(text_surface, text_rect)

deck, royals = create_cards()

# declare hands
hand1 = Hand(None, COORD['hand1'])
hand2 = Hand(None, COORD['hand2'])
hand3 = Hand(None, COORD['hand3'])
hands = [hand1, hand2, hand3]
discard = Discard(COORD['discard'])

# declare royals
royal1 = Royal(COORD['royal1'])
royal2 = Royal(COORD['royal2'])
royal3 = Royal(COORD['royal3'])
royals = [royal1, royal2, royal3]

print(len(deck), len(royals))
print(deck)
print(royals)



while True:

    # event loop
    for event in pygame.event.get():
        # quit event
        if event.type == pygame.QUIT:
            quit_game()

    SCREEN.fill(SNOW4)
    display_title()
    # for point in COORD:
    #     SCREEN.blit(DECK_BACK_IMAGE, COORD[point])
    display_deck()
    display_hands()
    display_discard()
    display_royals()
    pygame.display.update()
    clock.tick(FPS)
