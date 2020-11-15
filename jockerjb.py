import pygame
import os
import re
import settings
import random


# initialize pygame
pygame.init()

# common variables
ACTIVE_COLOR = 'lightblue'
INACTIVE_COLOR = 'blue'

# default button dimensions
BUTTON_WIDTH = 120
BUTTON_HEIGHT = 40

# fonts
LARGE_FONT_SIZE = 60
MID_FONT_SIZE = 50
SMALL_FONT_SIZE = 20
GAME_FONT_PATH = 'assets/fonts/pdark.ttf'
REGULAR_FONT_PATH = 'assets/fonts/ShareTechMono-Regular.ttf'
TITLE_FONT = pygame.font.Font(GAME_FONT_PATH, LARGE_FONT_SIZE)
BUTTON_FONT = pygame.font.Font(REGULAR_FONT_PATH, SMALL_FONT_SIZE)

class Hand(list):
    '''
    A group of cards
    '''
    def __init__(self, type):
        list.__init__(self)
        # layout position of hand
        self.type = type

class Button:
    '''
    Represents a button in the game
    '''
    def __init__(self, rect, text_surf, text_rect, color, callback, kwargs=None):
        # button rect
        self.rect = rect
        # button text 
        self.text_surf = text_surf
        self.text_rect = text_rect
        # button color
        self.color = color
        # callback function when the button is clicked
        self.callback = callback

class Layout:
    '''
    Layout of Hands in the game
    '''
    def __init__(self, x_0, y_0):
        self.x_0 = x_0
        self.y_0 =y_0

    def get_layouts(self):
        layouts = {
            'NW':{
                    'type': 'pillar',
                    'x_0': self.x_0 - settings.CARD_WIDTH - settings.DECK_SPACING,
                    'y_0': self.y_0 - settings.CARD_HEIGHT - settings.DECK_SPACING
            },
            'N':{
                    'type': 'wall',
                    'x_0': self.x_0, 
                    'y_0': self.y_0 - settings.CARD_HEIGHT - settings.DECK_SPACING
            },
            'NE':{
                    'type': 'pillar',
                    'x_0': self.x_0 + settings.CARD_WIDTH + settings.DECK_SPACING, 
                    'y_0': self.y_0 - settings.CARD_HEIGHT - settings.DECK_SPACING
            },
            'E':{
                    'type': 'wall',
                    'x_0': self.x_0 + settings.CARD_WIDTH + settings.DECK_SPACING, 
                    'y_0': self.y_0
            },
            'SE': {
                    'type': 'pillar',
                    'x_0': self.x_0 + settings.CARD_WIDTH + settings.DECK_SPACING, 
                    'y_0': self.y_0 + settings.CARD_HEIGHT + settings.DECK_SPACING
            },
            'S': {
                    'type': 'wall',
                    'x_0': self.x_0, 
                    'y_0': self.y_0 + settings.CARD_HEIGHT + settings.DECK_SPACING
            },
            'SW': {
                    'type': 'pillar',
                    'x_0': self.x_0 - settings.CARD_WIDTH - settings.DECK_SPACING, 
                    'y_0': self.y_0 + settings.CARD_HEIGHT + settings.DECK_SPACING
            },
            'W': {
                    'type': 'wall',
                    'x_0': self.x_0 - settings.CARD_WIDTH - settings.DECK_SPACING, 
                    'y_0': self.y_0
            },
            'C': {
                    'type': 'joker',
                    'x_0': self.x_0, 
                    'y_0': self.y_0
            },
            'D': {
                    'type': 'deck',
                    'x_0': self.x_0 - (2.5 * settings.CARD_WIDTH), 
                    'y_0': self.y_0
            }
        }
        return layouts

# set up game screen
screen = pygame.display.set_mode( (settings.GAME_WIDTH, settings.GAME_HEIGHT) )
pygame.display.set_caption(settings.GAME_TITLE)

# draw a card
x_0 = settings.X_0 - (settings.CARD_WIDTH / 2)
y_0 = settings.Y_0 - (settings.CARD_HEIGHT / 2)
joker = 'joker.png'
deck = 'assets/cards/deck.png'
factor = 0.75



# game clock
clock = pygame.time.Clock()

def display_stack(screen, hand, x_0, y_0):
    if hand.type == 'joker':
        for i in range(0, len(hand)-1, 1):
            # print(hand[i+1])
            _d = 20 * (len(hand)-1-i)
            img = pygame.image.load(settings.CARDS+hand[i])
            img = pygame.transform.rotozoom(img, 0, 0.65)
            screen.blit(img, (x_0+_d, y_0-_d))
    elif hand.type == 'main':
        for i in range(len(hand)-1, -1, -1):
            _d = spacer * i
            screen.blit(img_back, (x_0+_d, y_0-_d))
    else:
        for i in range(len(hand)-1, 0, -1):
            _d = spacer * i
            screen.blit(img_back, (x_0+_d, y_0-_d))

def create_deck():
    cards = []
    for filename in os.listdir(settings.CARDS):
        if '_' in filename:
            cards.append(filename)
    random.shuffle(cards)
    return cards

def display_text(screen, font, message, color, center):
    text_surface = font.render(message, True, color)
    text_rect = text_surface.get_rect(center=center)
    screen.blit(text_surface, text_rect)
    return text_surface, text_rect

def draw_button(screen, button):
    pygame.draw.rect(screen, button.color, button.rect)
    screen.blit(button.text_surf, button.text_rect)
    
def create_button(title, x,y,width,height, callback):
    text_mid_point_x = x + width/2
    text_mid_point_y = y + height/2
    button_rect = pygame.Rect(x,y,width,height)
    text_surface, text_rect = display_text(screen, BUTTON_FONT, title, pygame.Color('white'), button_rect.center)
    button = Button(
        button_rect,
        text_surface,
        text_rect,
        pygame.Color(INACTIVE_COLOR),
        callback
    )
    return button

def game_quit():
    pygame.quit()
    quit()

def check_win():
    for pos in layouts:
        if (pos != 'C' or pos !='D') and layouts[pos]['type'] == 'wall':
            if len(hands[pos]) == 0:
                print('WIN')
                game_quit()

def new_game():
    pass

def restart_play():
    while len(undo) > 0:
        undo_play()

def undo_play():
    if undo:
        move = undo.pop()
        for item in move:
            print(item)
            hands[item['pos']].append(item['card']) 
            if item['source'] == 'joker':
                print(hands['C'])
                hands['C'].pop()

def play():
    selection = []
    blacks = 0
    reds = 0
    for pos in selected:
        selection.append(pos)
        res = re.search('(\w)_(\d+)', hands[pos][-1])
        card_type = res.group(1)
        card_value = int(res.group(2))
        if card_type.startswith('S') or card_type.startswith('C'):
            blacks += card_value
        elif card_type.startswith('D') or card_type.startswith('H'):
            reds += card_value

    print('BLACKS', blacks)
    print('REDS', reds)

    if blacks == reds:
        moves = []
        for pos in selected:
            moves.append({
                'pos': pos,
                'card': hands[pos][-1],
                'source': 'hands'
            })
        undo.append(moves)
        for pos in selection:
            del selected[pos]
            hands[pos].pop()
            check_win()

layout = Layout(x_0, y_0)

cards = create_deck()

# create pillars and walls
hands = dict()
rects = dict()
layouts = layout.get_layouts()
for pos in layouts:
    if layouts[pos]:
        if layouts[pos]['type'] == 'pillar':
            hand = Hand('pillar')
            for _ in range(3):
                hand.append(cards.pop())
        elif layouts[pos]['type'] == 'wall':
            hand = Hand('wall')
            for _ in range(7):
                hand.append(cards.pop())
        hands[pos] = hand
        rects[pos] = pygame.rect.Rect(layouts[pos]['x_0'], layouts[pos]['y_0'], settings.CARD_WIDTH*factor, settings.CARD_HEIGHT*factor)

# add joker hand
hand = Hand('joker')
hand.append(joker)
hands['C'] = hand

main_deck = Hand('main')
main_deck.extend(cards)
hands['D'] = main_deck

img_back = pygame.image.load(deck)
img_back = pygame.transform.rotozoom(img_back, 0, 0.75)

# selected cards
selected = dict()

# undo buffer
undo = []

# game buttons
quit_button = create_button('QUIT', (settings.GAME_WIDTH - 10 - BUTTON_WIDTH), 10, BUTTON_WIDTH, BUTTON_HEIGHT, game_quit)
undo_button = create_button('UNDO', (settings.GAME_WIDTH - 10 - BUTTON_WIDTH), BUTTON_HEIGHT + 30, BUTTON_WIDTH, BUTTON_HEIGHT, undo_play)
restart_button = create_button('RESTART', (settings.GAME_WIDTH - 10 - BUTTON_WIDTH), BUTTON_HEIGHT + 90, BUTTON_WIDTH, BUTTON_HEIGHT, restart_play)
newgame_button = create_button('NEW GAME', (settings.GAME_WIDTH - 10 - BUTTON_WIDTH), BUTTON_HEIGHT + 150, BUTTON_WIDTH, BUTTON_HEIGHT, new_game)
play_button = create_button('PLAY', Layout(x_0, y_0).get_layouts()['E']['x_0'] + BUTTON_WIDTH + 40, settings.GAME_HEIGHT/2 - 20, BUTTON_WIDTH, BUTTON_HEIGHT, play)
buttons = [
    quit_button,
    play_button,
    undo_button,
    restart_button,
    newgame_button
]

while True:

    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            for pos in rects:
                if len(hands[pos]) > 0:
                    if rects[pos].collidepoint(event.pos):
                        if pos == 'D':
                            if len(hands['C']) < 4 and len(main_deck) > 0:                        
                                print('Deck selected')
                                hands['C'].append(main_deck.pop())
                                undo.append([{
                                    'pos': pos,
                                    'card': hands['C'][-1],
                                    'source': 'joker'
                                }])
                            selected.pop('C', None)
                        elif pos == 'C' and len(hands[pos]) == 1:
                            continue        
                        else:
                            if pos in selected:
                                del selected[pos]
                            else:
                                selected[pos] = 1
            for button in buttons:
                if button.rect.collidepoint(event.pos):
                    button.callback()


        if event.type == pygame.MOUSEMOTION:
            for button in buttons:
                if button.rect.collidepoint(event.pos):
                    button.color = ACTIVE_COLOR
                else:
                    button.color = INACTIVE_COLOR    

    screen.fill(pygame.Color(settings.SCREEN_BACKGROUND))

    cards = 2
    spacer = 3
    
    # draw cards
    layouts = layout.get_layouts()
    for pos in hands:
        if len(hands[pos]) > 0:
            display_stack(screen, hands[pos], layouts[pos]['x_0'], layouts[pos]['y_0'])
            if pos != 'D':
                card_img = pygame.image.load(settings.CARDS+hands[pos][-1])
                card_img = pygame.transform.rotozoom(card_img, 0, 0.75)
                screen.blit(card_img, (layouts[pos]['x_0'], layouts[pos]['y_0']))
        else:
            if hand.type == 'wall':
                print('You Win!!')
                pygame.quit()
                quit()

    # highlight selected hands
    for pos in selected:
        s = pygame.Surface((rects[pos][2],rects[pos][3]), pygame.SRCALPHA)
        s.fill((255,0,0,128))
        screen.blit(s, (rects[pos][0],rects[pos][1]))

    # draw buttons
    for button in buttons:
        draw_button(screen, button)

    pygame.display.update()
    clock.tick(settings.GAME_FRAMES)
