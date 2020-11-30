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
WHITE = pygame.Color('white')
RED = pygame.Color('red')
HIGHLIGHTED = pygame.Color((255,0,0,128))

# create game display
SCREEN = pygame.display.set_mode((800, 600))
pygame.display.set_caption(TITLE)

# load fonts and images
try:
    TITLE_FONT = pygame.font.Font('assets/fonts/pdark.ttf', 40)
    SMALL_FONT = pygame.font.Font('assets/fonts/ShareTechMono-Regular.ttf', 15)
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
 
# joker options
INACTIVE = BLACK
ACTIVE = RED

# locations
COORD = {
    'draw': pygame.rect.Rect(80, 244, CARD_WIDTH, CARD_HEIGHT),
    'discard': pygame.rect.Rect(640, 244, CARD_WIDTH, CARD_HEIGHT),
    'hand1': pygame.rect.Rect(250, 410, CARD_WIDTH, CARD_HEIGHT),
    'hand2': pygame.rect.Rect(360, 410, CARD_WIDTH, CARD_HEIGHT),
    'hand3': pygame.rect.Rect(470, 410, CARD_WIDTH, CARD_HEIGHT),
    'royal1': pygame.rect.Rect(250, 55, CARD_WIDTH, CARD_HEIGHT),
    'royal2': pygame.rect.Rect(360, 55, CARD_WIDTH, CARD_HEIGHT),
    'royal3': pygame.rect.Rect(470, 55, CARD_WIDTH, CARD_HEIGHT)
}

class Card:
    
    def __init__(self, value, symbol, suite):
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

class JokerOption:

    def __init__(self, value, rect):
        self.value = value
        self.rect = rect
        self.color = INACTIVE

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
            card = Card(j, image, suite)
            # get jokers only form last row
            if i == 4 and j < 3:
                card.value = "flex"
                deck.append(card)
            # get non royals only
            if i < 4 and j < 11:
                deck.append(card)
            if i < 4 and j > 10:
                royals.append(card)
    # random.shuffle(deck)
    random.shuffle(royals)
    return deck, royals

def display_deck():
    '''
    Displays a stack of cards behind the top cards
    '''
    scaled_count = int(len(deck) / 3) 
    x_0, y_0 = COORD['draw'].topleft
    # stack behind the draw deck
    for i in range(scaled_count-1, -1, -1):
        _d = 3 * i
        SCREEN.blit(DECK_BACK_IMAGE, (x_0+_d, y_0-_d))

def display_hands():
    for hand in hands:
        if hand.card == None:
            display_place_holder(hand.location[0], hand.location[1], CARD_WIDTH, CARD_HEIGHT)
        else:
            SCREEN.blit(hand.card.symbol, hand.location)
        

def display_discard():
    if len(discard.cards) == 0:
        display_place_holder(discard.location[0], discard.location[1], CARD_WIDTH, CARD_HEIGHT)
        
def display_place_holder(x, y, w, h):
    rect = pygame.rect.Rect(x, y, w, h)
    pygame.draw.rect(SCREEN, BLACK, rect, width=1, border_radius=5)
    pygame.draw.circle(SCREEN, BLACK, rect.center, radius=(w/2-5), width=1 )

def display_royals():
    for royal in royals:
        cards = royal.cards + royal.play
        if len(cards) == 0:
            display_place_holder(royal.location.x, royal.location.y, CARD_WIDTH, CARD_HEIGHT)
        _d = 30
        for i, card in enumerate(cards):
            _y = royal.location.y + (i * _d)
            rect = pygame.rect.Rect(royal.location.x, _y, CARD_WIDTH, CARD_HEIGHT)
            SCREEN.blit(card.symbol, rect)

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

def get_cards():
    if len(deck) >= 3:
        for hand in hands:
            if hand.card != None:
                return
        for hand in hands:
            hand.card= deck.pop()

def create_joker_options():
    pos = list(COORD['hand1'].topleft)
    pos[1] -= 35
    _d = 20
    for i in range(2, 11):
        _x = (_d * ( i-2)) + (i-1)*15 + pos[0] - 22
        _y = pos[1]
        _j = i - 2
        rect = pygame.rect.Rect(_x, _y , 30, 30)
        option = JokerOption(i, rect)
        joker_options.append(option)

def display_joker_options():
    pos = list(COORD['hand1'].topleft)
    pos[1] -= 35
    _d = 20
    for i, option in enumerate(joker_options):
        surf = pygame.surface.Surface((30, 30))
        surf.fill(option.color)
        surf.get_rect().center
        text_surface = SMALL_FONT.render(str(i + 2), True, WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (15,15)
        surf.blit(text_surface, text_rect)
        SCREEN.blit(surf, option.rect)

    # message
    message_surface = SMALL_FONT.render('Select Joker value',True, RED, BLACK)
    message_rect = message_surface.get_rect()
    message_rect.left = pos[0] - 7
    message_rect.top = pos[-1] - 20
    SCREEN.blit(message_surface, message_rect)

def check_options_hover(event):
    for option in joker_options:
        if option.rect.collidepoint(event.pos):
            option.color = ACTIVE
        else:
            option.color = INACTIVE

deck, royals_cards = create_cards()

# value options for jokers
joker_options = []
create_joker_options()

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
# add cards to royals
for royal in royals:
    for _ in range(4):
        card = royals_cards.pop()
        royal.cards.append(card)

# state management for undo operations
# state = []

# selected hand
selected_hand = None
selected_royal = None
selected_joker = False
show_joker_options = False
active_royal = None

while True:

    # event loop
    for event in pygame.event.get():
        # quit event
        if event.type == pygame.QUIT:
            quit_game()

        if event.type == pygame.MOUSEMOTION:
            check_options_hover(event)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if show_joker_options:
                # check joker value selected
                for option in joker_options:
                    if option.rect.collidepoint(event.pos):
                        active_royal.play[-1].value = option.value
                        show_joker_options = False
                        break
            else:
                # detect click on draw deck
                if COORD['draw'].collidepoint(event.pos):
                    get_cards()
                # detect click on hand
                for hand in hands:
                    if hand.location.collidepoint(event.pos):
                        if hand == selected_hand:
                            selected_hand = None
                        elif hand.card != None:
                            selected_hand = hand

                # detect click on royal
                for royal in royals:
                    cards = royal.cards + royal.play
                    rect = pygame.rect.Rect(royal.location.x, royal.location.y, CARD_WIDTH, ((len(cards)-1)*30) + CARD_HEIGHT)
                    if rect.collidepoint(event.pos):
                        if selected_hand and len(royal.play) < 3:
                            royal.play.append(selected_hand.card)
                            if royal.play[-1].value =='flex' and len(royal.play) <= 2:
                                show_joker_options = True
                                active_royal = royal
                            selected_hand.card = None
                            selected_hand = None
                            if royal.play[-1].value == None:
                                show_joker_options == True
                            if len(royal.play) == 3:
                                pass

    SCREEN.fill(SNOW4)
    display_title()
    display_deck()
    display_hands()
    display_discard()
    display_royals()
    if show_joker_options:
        display_joker_options()
    # display selected hand
    if selected_hand and selected_hand.card != None:
        s = pygame.Surface((CARD_WIDTH, CARD_HEIGHT), pygame.SRCALPHA)
        s.fill(HIGHLIGHTED)
        SCREEN.blit(s, selected_hand.location.topleft)
    # display selected royal
    if selected_royal:
        cards = selected_royal.cards + selected_royal.play
        rect = pygame.rect.Rect(selected_royal.location.x, selected_royal.location.y + ((len(cards)-1)*30), CARD_WIDTH, CARD_HEIGHT)
        s = pygame.Surface((CARD_WIDTH, CARD_HEIGHT), pygame.SRCALPHA)
        s.fill(HIGHLIGHTED)
        SCREEN.blit(s, rect.topleft)

    pygame.display.update()
    clock.tick(FPS)
