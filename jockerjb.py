import pygame
import os
import re
import settings
import random

import argparse

from itertools import combinations

# initialize pygame
pygame.init()

# common variables
ACTIVE_COLOR = 'lightblue'
INACTIVE_COLOR = 'blue'
DARKGREEN = (0,104,55)
HIGHLIGHTED = (255,0,0,128)

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
STATS_FONT = pygame.font.Font(REGULAR_FONT_PATH, SMALL_FONT_SIZE)

joker = 'joker.png'
deck = 'assets/cards/deck.png'

# set up game screen
SCREEN = pygame.display.set_mode( (settings.GAME_WIDTH, settings.GAME_HEIGHT) )
pygame.display.set_caption(settings.GAME_TITLE)

# game clock
CLOCK = pygame.time.Clock()

HELP_MESSAGE = pygame.image.load('assets/help.png').convert_alpha()

factor = 0.75
spacer = 3

class Win(pygame.sprite.Sprite):

    def __init__(self, x_0, y_0):
        super().__init__()
        self.sprite = []
        for i in range(1,4):
            self.sprite.append(pygame.image.load('assets/win/win%s.gif'%i))
        self.image = self.sprite[0]
        self.rect = self.image.get_rect()
        self.rect.topleft = [x_0, y_0]
        self.current_image = 0
    
    def update(self):
        self.image = self.sprite[int(self.current_image)]
        self.current_image += 0.2
        if self.current_image >= len(self.sprite):
            self.current_image = 0 

class Lose(pygame.sprite.Sprite):

    def __init__(self, x_0, y_0):
        super().__init__()
        self.sprite = []
        for i in range(1,4):
            self.sprite.append(pygame.image.load('assets/lose/lose%s.gif'%i))
        self.image = self.sprite[0]
        self.rect = self.image.get_rect()
        self.rect.topleft = [x_0, y_0]
        self.current_image = 0
    
    def update(self):
        self.image = self.sprite[int(self.current_image)]
        self.current_image += 0.2
        if self.current_image >= len(self.sprite):
            self.current_image = 0 

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

class JockerJB:
    '''
    Jocker Jail Break main class
    '''

    def __init__(self, player='Player'):
        self.player = player
        self.help = False
        self.played = 0
        self.streak = 0

        # start coordinates from drawing Hands and Decks
        self.x_0 = settings.X_0 - (settings.CARD_WIDTH / 2)
        self.y_0 = settings.Y_0 - (settings.CARD_HEIGHT / 2)
        self.layout = Layout(self.x_0, self.y_0)

        # initial cards deck
        self.cards = None
        self.buttons = []

        self.hands = None
        self.rects = None

        # selected cards
        self.selected = dict()

        # undo buffer
        self.undo = []

        # win/lose condition
        self.win = False
        self.lose = False

        self.cl = True

    def display_stack(self, hand, x_0, y_0):
        img_back = pygame.image.load(deck)
        img_back = pygame.transform.rotozoom(img_back, 0, 0.75)
        if hand.type == 'joker':
            for i in range(0, len(hand)-1, 1):
                _d = 20 * (len(hand)-1-i)
                img = pygame.image.load(settings.CARDS+hand[i])
                img = pygame.transform.rotozoom(img, 0, 0.65)
                SCREEN.blit(img, (x_0+_d, y_0-_d))
        elif hand.type == 'main':
            for i in range(len(hand)-1, -1, -1):
                _d = spacer * i
                SCREEN.blit(img_back, (x_0+_d, y_0-_d))
        else:
            for i in range(len(hand)-1, 0, -1):
                _d = spacer * i
                SCREEN.blit(img_back, (x_0+_d, y_0-_d))

    def create_deck(self):
        cards = []
        for filename in os.listdir(settings.CARDS):
            if '_' in filename:
                cards.append(filename)
        random.shuffle(cards)
        return cards

    def display_text(self, font, message, color, center, show=True):
        text_surface = font.render(message, True, color)
        text_rect = text_surface.get_rect(center=center)
        if show:
            SCREEN.blit(text_surface, text_rect)
        return text_surface, text_rect

    def draw_button(self, button):
        pygame.draw.rect(SCREEN, button.color, button.rect)
        SCREEN.blit(button.text_surf, button.text_rect)
    
    def create_button(self, title, x,y,width,height, callback):
        text_mid_point_x = x + width/2
        text_mid_point_y = y + height/2
        button_rect = pygame.Rect(x,y,width,height)
        text_surface, text_rect = self.display_text(BUTTON_FONT, title, pygame.Color('white'), button_rect.center)
        button = Button(
            button_rect,
            text_surface,
            text_rect,
            pygame.Color(INACTIVE_COLOR),
            callback
        )
        return button

    def game_quit(self):
        pygame.quit()
        quit()

    def game_over(func):
        def inner(self):
            if self.win == False and self.lose == False:
                func(self)
        return inner

    def check_win(self):
        layouts = self.layout.get_layouts()
        for pos in layouts:
            if (layouts[pos]['type'] == 'wall') and (len(self.hands['C']) == 1) and (len(self.hands[pos]) == 0):
                    self.win = True
                    self.streak += 1
                    self.played += 1

    def new_game(self):
        self.start()
    
    @game_over
    def restart_play(self):
        while len(self.undo) > 0:
            self.undo_play()
        self.selected = dict()

    @game_over
    def undo_play(self):
        if self.undo:
            move = self.undo.pop()
            for item in move:
                self.hands[item['pos']].append(item['card']) 
                if item['source'] == 'joker':
                    self.hands['C'].pop()
        self.selected = dict()

    @game_over
    def play(self):
        selection = []
        blacks = 0
        reds = 0
        for pos in self.selected:
            selection.append(pos)
            res = re.search('(\w)_(\d+)', self.hands[pos][-1])
            card_type = res.group(1)
            card_value = int(res.group(2))
            if card_type.startswith('S') or card_type.startswith('C'):
                blacks += card_value
            elif card_type.startswith('D') or card_type.startswith('H'):
                reds += card_value

        if blacks == reds:
            moves = []
            for pos in self.selected:
                moves.append({
                    'pos': pos,
                    'card': self.hands[pos][-1],
                    'source': 'hands'
                })
            self.undo.append(moves)
            for pos in selection:
                del self.selected[pos]
                self.hands[pos].pop()
        self.check_win()

    def valid_play(self, cards):
        blacks = 0
        reds = 0
        for card in cards:
            res = re.search('(\w)_(\d+)', card)
            card_type = res.group(1)
            card_value = int(res.group(2))
            if card_type.startswith('S') or card_type.startswith('C'):
                blacks += card_value
            elif card_type.startswith('D') or card_type.startswith('H'):
                reds += card_value
        if blacks == reds:
            return blacks
        else:
            return False


    @game_over
    def check_lose(self):
        combos = 0
        if len(self.hands['C']) == 4:
            top_cards = []
            for pos in self.hands:
                if pos != 'D' and len(self.hands[pos]) >=  1:
                    top_cards.append(self.hands[pos][-1])
            plays = []
            for i in range(2, len(top_cards) + 1):
                play = combinations(top_cards, i)
                for cards in play:
                    res = self.valid_play(cards)
                    if res:
                        return
            self.lose = True
            self.played += 1

    def draw_cards(self):
        # buffer for Hands
        self.hands = dict()
        # buffer for hands rect
        self.rects = dict()
        # get layouts for drawing Hands on screen
        layouts = self.layout.get_layouts()
        # draw cards on the screen
        for pos in layouts:
            if layouts[pos]:
                if layouts[pos]['type'] == 'pillar':
                    hand = Hand('pillar')
                    for _ in range(3):
                        hand.append(self.cards.pop())
                elif layouts[pos]['type'] == 'wall':
                    hand = Hand('wall')
                    for _ in range(7):
                        hand.append(self.cards.pop())
                self.hands[pos] = hand
                self.rects[pos] = pygame.rect.Rect(layouts[pos]['x_0'], layouts[pos]['y_0'], settings.CARD_WIDTH*factor, settings.CARD_HEIGHT*factor)

        # add joker hand
        hand = Hand('joker')
        hand.append(joker)
        self.hands['C'] = hand

        main_deck = Hand('main')
        main_deck.extend(self.cards)
        self.hands['D'] = main_deck

    def show_stats(self):
        stats_labels = [
            self.display_text(STATS_FONT, 'Player: %s'%self.player, pygame.Color('White'), (100, 15), show=False),
            self.display_text(STATS_FONT, 'Games Played: %s'%self.played, pygame.Color('White'), (100, 45), show=False),
            self.display_text(STATS_FONT, 'Streak: %s'%self.streak, pygame.Color('White'), (100, 75), show=False),
        ]
        for label in stats_labels:
            text_surface = label[0]
            text_rect = label[1]
            text_rect.x = 10
            SCREEN.blit(text_surface, text_rect)

    def create_buttons(self):
        # game buttons
        quit_button = self.create_button('QUIT', (settings.GAME_WIDTH - 10 - BUTTON_WIDTH), 10, BUTTON_WIDTH, BUTTON_HEIGHT, self.game_quit)
        help_button = self.create_button('HELP', (settings.GAME_WIDTH - 10 - BUTTON_WIDTH), BUTTON_HEIGHT + 30, BUTTON_WIDTH, BUTTON_HEIGHT, self.game_help)
        undo_button = self.create_button('UNDO', (settings.GAME_WIDTH - 10 - BUTTON_WIDTH), BUTTON_HEIGHT + 90, BUTTON_WIDTH, BUTTON_HEIGHT, self.undo_play)
        restart_button = self.create_button('RESTART', (settings.GAME_WIDTH - 10 - BUTTON_WIDTH), BUTTON_HEIGHT + 150, BUTTON_WIDTH, BUTTON_HEIGHT, self.restart_play)
        newgame_button = self.create_button('NEW GAME', (settings.GAME_WIDTH - 10 - BUTTON_WIDTH), BUTTON_HEIGHT + 210, BUTTON_WIDTH, BUTTON_HEIGHT, self.new_game)
        play_button = self.create_button('PLAY', Layout(self.x_0, self.y_0).get_layouts()['E']['x_0'] + BUTTON_WIDTH + 40, settings.GAME_HEIGHT/2 - 20, BUTTON_WIDTH, BUTTON_HEIGHT, self.play)
        self.buttons = [
            quit_button,
            help_button,
            play_button,
            undo_button,
            restart_button,
            newgame_button
        ]

    def game_help(self):
        self.help = True
        close_button = self.create_button('RESUME', (settings.GAME_WIDTH - 10 - BUTTON_WIDTH), 10, BUTTON_WIDTH, BUTTON_HEIGHT, self.help_close)
        self.buttons = [close_button]

    def help_close(self):
        self.help = False
        self.create_buttons()

    def show_help(self):
        SCREEN.fill(pygame.Color('lavenderblush4'))
        x = settings.X_0 - HELP_MESSAGE.get_rect().w/2
        y = settings.Y_0 - HELP_MESSAGE.get_rect().h/2
        SCREEN.blit(HELP_MESSAGE, (x, y))
        
    def start(self):
        # create a deck
        self.cards = self.create_deck()
        self.draw_cards()
        self.create_buttons()

        # reset win/lose
        self.win = False
        self.lose = False

        # reset selected
        self.selected = dict()

        # Win Animation
        win = Win(100, 200)
        win_grp = pygame.sprite.Group()
        win_grp.add(win)

        # Lose Animation
        lose = Lose(100, 200)
        lose_grp = pygame.sprite.Group()
        lose_grp.add(lose)

        while True:

            # event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for pos in self.rects:
                        if len(self.hands[pos]) > 0:
                            if self.rects[pos].collidepoint(event.pos):
                                if self.win or self.lose:
                                        continue
                                if pos == 'D':
                                    if len(self.hands['C']) < 4 and len(self.hands['D']) > 0:   
                                        self.hands['C'].append(self.hands['D'].pop())
                                        self.undo.append([{
                                            'pos': pos,
                                            'card': self.hands['C'][-1],
                                            'source': 'joker'
                                        }])
                                    self.selected.pop('C', None)
                                elif pos == 'C' and len(self.hands[pos]) == 1:
                                    continue        
                                else:
                                    if pos in self.selected:
                                        del self.selected[pos]
                                    else:
                                        self.selected[pos] = 1
                    for button in self.buttons:
                            if button.rect.collidepoint(event.pos):
                                button.callback()


                if event.type == pygame.MOUSEMOTION:
                    for button in self.buttons:
                        if button.rect.collidepoint(event.pos):
                            button.color = ACTIVE_COLOR
                        else:
                            button.color = INACTIVE_COLOR    

            SCREEN.fill(pygame.Color(settings.SCREEN_BACKGROUND))
            
            # draw cards
            layouts = self.layout.get_layouts()
            for pos in self.hands:
                if len(self.hands[pos]) > 0:
                    self.display_stack(self.hands[pos], layouts[pos]['x_0'], layouts[pos]['y_0'])
                    if pos != 'D':
                        card_img = pygame.image.load(settings.CARDS + self.hands[pos][-1])
                        card_img = pygame.transform.rotozoom(card_img, 0, 0.75)
                        SCREEN.blit(card_img, (layouts[pos]['x_0'], layouts[pos]['y_0']))

            # highlight selected hands
            for pos in self.selected:
                s = pygame.Surface((self.rects[pos][2], self.rects[pos][3]), pygame.SRCALPHA)
                s.fill(HIGHLIGHTED)
                SCREEN.blit(s, (self.rects[pos][0], self.rects[pos][1]))

            # display win or lose animations
            if self.win:
                win_grp.draw(SCREEN)
                win_grp.update()
            if self.lose:
                lose_grp.draw(SCREEN)
                lose_grp.update()

            self.check_lose()

            # show player stats
            self.show_stats()

            # display help
            if self.help:
                self.show_help()

            # draw buttons
            for button in self.buttons:
                self.draw_button(button)

            pygame.display.update()
            CLOCK.tick(settings.GAME_FRAMES)

if __name__ == "__main__":
    game = JockerJB()
    game.start()
