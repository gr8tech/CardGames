'''
Program: Joker Jail Break (Single Player)
Author: Moosa Bonomali
Invented by: Ramon Huiskamp (roofkat).
https://roofkat.itch.io/joker-jailbreak
Email: gr8tech01@gmail.com
OS: Windows 10
Python: 3.x
Require Modules: pygame

Starting the game

python jokerjb.py or pythonw joker.py
'''

import pygame
import os
import re
import random
import string
import copy

from itertools import combinations

from settings import *

# initialize pygame
pygame.init()

# set up game screen
SCREEN = pygame.display.set_mode( (GAME_WIDTH, GAME_HEIGHT) )
pygame.display.set_caption(GAME_TITLE)

# load sprite image
try:
    SPRITE = pygame.image.load('assets/cards/cards.png')
except FileNotFoundError:
    print('Game images not found')
    pygame.quit()
    quit()

# SPRITE PARAMETERS
SPRITE_SPACING = 20

# special images in sprite
JOKER_IMAGE = pygame.rect.Rect(20, 548, CARD_WIDTH, CARD_HEIGHT)
DECK_BACK_IMAGE = pygame.rect.Rect(320, 548, CARD_WIDTH, CARD_HEIGHT)

# game clock
CLOCK = pygame.time.Clock()

# help message
HELP_MESSAGE = pygame.image.load(HELP_IMAGE).convert_alpha()

# game fonts
TITLE_FONT = pygame.font.Font(GAME_FONT_PATH, LARGE_FONT_SIZE)
BUTTON_FONT = pygame.font.Font(REGULAR_FONT_PATH, SMALL_FONT_SIZE)
STATS_FONT = pygame.font.Font(REGULAR_FONT_PATH, SMALL_FONT_SIZE)
NORMAL_FONT = pygame.font.Font(REGULAR_FONT_PATH, LARGE_FONT_SIZE)
SMALL_FONT = pygame.font.Font(REGULAR_FONT_PATH, SMALL_FONT_SIZE)

class Win(pygame.sprite.Sprite):
    '''
    Animation to display when the game is won
    '''
    def __init__(self, x_0, y_0):
        super().__init__()
        self.sprite = []
        # load images into sprite
        for i in range(1,4):
            self.sprite.append(pygame.image.load('assets/win/win%s.gif'%i))
        # select initial image to display
        self.image = self.sprite[0]
        self.rect = self.image.get_rect()
        self.rect.center = [x_0, y_0]
        # initial image index
        self.current_image = 0
    
    def update(self):
        '''
        Animate the win message
        '''
        # select next image to be displayed
        self.image = self.sprite[int(self.current_image)]
        # increment image index, 0.2 used to control the speed of animation
        self.current_image += 0.2
        # reset image index when all have been displayed
        if self.current_image >= len(self.sprite):
            self.current_image = 0 

class Lose(pygame.sprite.Sprite):
    '''
    Animation to display when the game cannot be won
    '''
    def __init__(self, x_0, y_0):
        super().__init__()
        self.sprite = []
        # load images into sprite
        for i in range(1,4):
            self.sprite.append(pygame.image.load('assets/lose/lose%s.gif'%i))
        self.image = self.sprite[0]
        self.rect = self.image.get_rect()
        self.rect.center = [x_0, y_0]
        # initial image index
        self.current_image = 0
    
    def update(self):
        '''
        Animate the lose message
        '''
        # select next image to be displayed
        self.image = self.sprite[int(self.current_image)]
        # increment image index, 0.2 used to control the speed of animation
        self.current_image += 0.2
        # reset image index when all have been displayed
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
    Layout of Hands in the game. These layouts are for the walls, pillars, joker and deck of cards
    '''
    def __init__(self, x_0, y_0):
        '''
        Args:
            x_0, y_0 : midpoint of the screen
        '''
        self.x_0 = x_0 - 50
        self.y_0 =y_0 + 50

    def get_layouts(self):
        '''
        Generates the positions of Cards on the screen
        N - North, NW - North West, NE - North East, E - East, W - West, S - South, SE - South East, SW - South West, C - Center (Joker Position), D - Deck with spare cards
        '''
        layouts = {
            'NW':{
                    'type': 'pillar',
                    'x_0': self.x_0 - CARD_WIDTH - DECK_SPACING,
                    'y_0': self.y_0 - CARD_HEIGHT - DECK_SPACING
            },
            'N':{
                    'type': 'wall',
                    'x_0': self.x_0, 
                    'y_0': self.y_0 - CARD_HEIGHT - DECK_SPACING
            },
            'NE':{
                    'type': 'pillar',
                    'x_0': self.x_0 + CARD_WIDTH + DECK_SPACING, 
                    'y_0': self.y_0 - CARD_HEIGHT - DECK_SPACING
            },
            'E':{
                    'type': 'wall',
                    'x_0': self.x_0 + CARD_WIDTH + DECK_SPACING, 
                    'y_0': self.y_0
            },
            'SE': {
                    'type': 'pillar',
                    'x_0': self.x_0 + CARD_WIDTH + DECK_SPACING, 
                    'y_0': self.y_0 + CARD_HEIGHT + DECK_SPACING
            },
            'S': {
                    'type': 'wall',
                    'x_0': self.x_0, 
                    'y_0': self.y_0 + CARD_HEIGHT + DECK_SPACING
            },
            'SW': {
                    'type': 'pillar',
                    'x_0': self.x_0 - CARD_WIDTH - DECK_SPACING, 
                    'y_0': self.y_0 + CARD_HEIGHT + DECK_SPACING
            },
            'W': {
                    'type': 'wall',
                    'x_0': self.x_0 - CARD_WIDTH - DECK_SPACING, 
                    'y_0': self.y_0
            },
            'C': {
                    'type': 'joker',
                    'x_0': self.x_0, 
                    'y_0': self.y_0
            },
            'D': {
                    'type': 'deck',
                    'x_0': self.x_0 - (3 * CARD_WIDTH), 
                    'y_0': self.y_0
            }
        }
        return layouts

class Card:

    def __init__(self, value, rect, suite):
        self.value = value
        self.rect = rect
        self.suite = suite

class JockerJB:
    '''
    Jocker Jail Break main class
    '''

    def __init__(self):
        # player name
        self.get_player_name = True
        self.player = ''

        # show help
        self.help = False
        # played games
        self.played = 0
        # won games
        self.streak = 0

        # start coordinates from drawing Hands and Decks
        self.x_0 = X_0 - (CARD_WIDTH / 2)
        self.y_0 = Y_0 - (CARD_HEIGHT / 2)
        self.layout = Layout(self.x_0, self.y_0)

        # initial cards deck
        self.cards = None
        # list of buttons on UI
        self.buttons = []

        # list of walls, pillars, joker position
        self.hands = None
        # list of rects for wall and pillars
        self.rects = None

        # selected cards during play
        self.selected = dict()

        # undo buffer
        self.undo = []

        # win/lose conditions
        self.win = False
        self.lose = False

    def display_stack(self, hand, x_0, y_0):
        '''
        Displays a stack of cards behind the top cards
        '''
        # stack on top of the Joker
        if hand.type == 'joker':
            for i in range(0, len(hand) - 1, 1):
                _d = 10 * (len(hand) - 1 - i)
                # img = pygame.image.load(CARDS + hand[i])
                # img = pygame.transform.rotozoom(img, 0, 0.65)
                SCREEN.blit(SPRITE, (x_0 + _d, y_0 - _d), hand[i])
        # stack behind the spare deck
        elif hand.type == 'main':
            for i in range(len(hand)-1, -1, -1):
                _d = CARD_SPACING * i
                SCREEN.blit(SPRITE, (x_0+_d, y_0-_d), DECK_BACK_IMAGE)
        # stack behind the walls and pillars
        else:
            for i in range(len(hand)-1, 0, -1):
                _d = CARD_SPACING * i
                SCREEN.blit(SPRITE, (x_0+_d, y_0-_d), DECK_BACK_IMAGE)

    def create_deck(self):
        '''
        Create shuffled list of cards for game
        '''
        cards = []

        suites = 'CSDH'
        for j, suite in enumerate(suites):
            # generate y coordinate of card in sprite
            y = ((j + 1)) * SPRITE_SPACING + (j * CARD_HEIGHT)
            for i in range(1, 14):
                # card value
                value = i
                # generate x coordinate of card in sprite
                x = (i * SPRITE_SPACING) + ( (i - 1) * CARD_WIDTH)
                # create card rect in sprite
                rect = pygame.rect.Rect(x, y, CARD_WIDTH, CARD_HEIGHT)
                # generate card object
                card = Card(value, rect, suite)
                cards.append(card)
        random.shuffle(cards)
        return cards

    def display_text(self, font, message, color, center, show=True):
        '''
        Displays text on the provided center
        '''
        text_surface = font.render(message, True, color)
        text_rect = text_surface.get_rect(center=center)
        if show:
            SCREEN.blit(text_surface, text_rect)
        return text_surface, text_rect

    def draw_button(self, button):
        '''
        Draw a button
        '''
        pygame.draw.rect(SCREEN, button.color, button.rect)
        SCREEN.blit(button.text_surf, button.text_rect)
    
    def create_button(self, title, x,y,width,height, callback):
        '''
        Create a button
        '''
        text_mid_point_x = x + width/2
        text_mid_point_y = y + height/2
        button_rect = pygame.Rect(x,y,width,height)
        text_surface, text_rect = self.display_text(BUTTON_FONT, title, pygame.Color('white'), button_rect.center)
        button = Button(
            button_rect,
            text_surface,
            text_rect,
            pygame.Color(BUTTON_INACTIVE_COLOR),
            callback
        )
        return button

    def game_quit(self):
        '''
        Quit the game
        '''
        pygame.quit()
        quit()

    def game_over(func):
        '''
        Decorator function to check if the game is over. The game is over if it has been won, or it cannot be one based on possible options
        '''
        def inner(self):
            if self.win == False and self.lose == False:
                func(self)
        return inner

    def check_win(self):
        '''
        Check if the game has been won. The game is won when one of the walls has been cleared and there is card on the Joker
        '''
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
        '''
        Game restart. All plays made are undone
        '''
        while len(self.undo) > 0:
            self.undo_play()
        # cleared the cards selected dictionary, in case something was selected
        self.selected = dict()

    @game_over
    def undo_play(self):
        '''
        Undo moves done, one at a time
        '''
        if self.undo:
            move = self.undo.pop()
            for item in move:
                self.hands[item['pos']].append(item['card']) 
                if item['source'] == 'joker':
                    self.hands['C'].pop()
        # cleared the cards selected dictionary, in case something was selected
        self.selected = dict()

    @game_over
    def play(self):
        '''
        Collects selected cards and checks valid of the play
        Returns:
            True: if the play is valid
        '''
        selection = []
        blacks = 0
        reds = 0
        # compute tota value of Blacks and Reds
        for pos in self.selected:
            selection.append(pos)
            card_type = self.hands[pos][-1].suite
            card_value = self.hands[pos][-1].value
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
            # save play if valid
            self.undo.append(moves)
            # remove valid play cards from the top
            for pos in selection:
                del self.selected[pos]
                self.hands[pos].pop()
        # check if game has been won
        self.check_win()

    def valid_play(self, cards):
        '''
        Check if selected cards constitue a valid combination of Reds and Blacks
        Args:
            cards: selected cards
        Returns:
            value: total value of Blacks or Reds
            False: combination is not valid
        '''
        blacks = 0
        reds = 0
        for card in cards:
            # extract card value and symbol
            card_type = card.suite
            card_value = card.value
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
        '''
        Check if the game cannot be won. Check is only done when there are 3 cards on top of the Joker.
        All possible combinations and their validity are made for available cards.
        '''
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
                self.rects[pos] = pygame.rect.Rect(layouts[pos]['x_0'], layouts[pos]['y_0'], CARD_WIDTH, CARD_HEIGHT)

        # add joker hand
        hand = Hand('joker')
        hand.append(JOKER_IMAGE)
        self.hands['C'] = hand

        # add deck with spare cards
        main_deck = Hand('main')
        main_deck.extend(self.cards)
        self.hands['D'] = main_deck

    def show_stats(self):
        '''
        Show player stats
        '''
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
        '''
        Create game buttons
        '''
        quit_button = self.create_button('QUIT', (GAME_WIDTH - 10 - BUTTON_WIDTH), 10, BUTTON_WIDTH, BUTTON_HEIGHT, self.game_quit)
        help_button = self.create_button('HELP', (GAME_WIDTH - 10 - BUTTON_WIDTH), BUTTON_HEIGHT + 30, BUTTON_WIDTH, BUTTON_HEIGHT, self.game_help)
        undo_button = self.create_button('UNDO', (GAME_WIDTH - 10 - BUTTON_WIDTH), BUTTON_HEIGHT + 90, BUTTON_WIDTH, BUTTON_HEIGHT, self.undo_play)
        restart_button = self.create_button('RESTART', (GAME_WIDTH - 10 - BUTTON_WIDTH), BUTTON_HEIGHT + 150, BUTTON_WIDTH, BUTTON_HEIGHT, self.restart_play)
        newgame_button = self.create_button('NEW GAME', (GAME_WIDTH - 10 - BUTTON_WIDTH), BUTTON_HEIGHT + 210, BUTTON_WIDTH, BUTTON_HEIGHT, self.new_game)
        play_button = self.create_button('PLAY', Layout(self.x_0, self.y_0).get_layouts()['E']['x_0'] + BUTTON_WIDTH - 20, GAME_HEIGHT/2, BUTTON_WIDTH, BUTTON_HEIGHT, self.play)
        self.buttons = [
            quit_button,
            help_button,
            play_button,
            undo_button,
            restart_button,
            newgame_button
        ]

    def game_help(self):
        '''
        Activate help
        '''
        self.help = True
        close_button = self.create_button('RESUME', (GAME_WIDTH - 10 - BUTTON_WIDTH), 10, BUTTON_WIDTH, BUTTON_HEIGHT, self.help_close)
        self.buttons = [close_button]

    def help_close(self):
        '''
        Close help
        '''
        self.help = False
        self.create_buttons()

    def show_help(self):
        '''
        Display help message on the screen
        '''
        SCREEN.fill(pygame.Color('lavenderblush4'))
        x = X_0 - HELP_MESSAGE.get_rect().w/2
        y = Y_0 - HELP_MESSAGE.get_rect().h/2
        SCREEN.blit(HELP_MESSAGE, (x, y))

    def display_player_name(self):
        SCREEN.fill(pygame.Color('lavenderblush4'))
        # display title
        text_surface, text_rect = self.display_text(TITLE_FONT, "Enter your name", pygame.Color('black'), (X_0, Y_0), show=False)
        base_rect = copy.copy(text_rect)
        text_rect.y = base_rect.y - base_rect.height * 1.5
        SCREEN.blit(text_surface, text_rect)
        # display sub-title
        text_surface, text_rect = self.display_text(SMALL_FONT, "Press return when done.", pygame.Color('black'), (X_0, Y_0), show=False)
        text_rect.y = base_rect.y - base_rect.height/2
        SCREEN.blit(text_surface, text_rect)
        # input rect
        input_rect = pygame.rect.Rect(base_rect.x, base_rect.y, base_rect.width, base_rect.height)
        pygame.draw.rect(SCREEN, pygame.Color('white'), base_rect)
        # display entered name (max 15 chars)
        text_surface, text_rect = self.display_text(NORMAL_FONT, self.player+'_', pygame.Color('black'), (X_0, Y_0), show=False)
        text_rect.x, text_rect.y = input_rect.x, input_rect.y-5
        SCREEN.blit(text_surface, text_rect)
        self.buttons = []
        
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
        win = Win(X_0, Y_0)
        win_grp = pygame.sprite.Group()
        win_grp.add(win)

        # Lose Animation
        lose = Lose(X_0, Y_0)
        lose_grp = pygame.sprite.Group()
        lose_grp.add(lose)

        # GAME LOOP
        while True:

            # EVENT LOOP
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

                    # check if a button has been clicked and run the callback function
                    for button in self.buttons:
                            if button.rect.collidepoint(event.pos):
                                button.callback()

                # button mouse hover actions
                if event.type == pygame.MOUSEMOTION:
                    for button in self.buttons:
                        if button.rect.collidepoint(event.pos):
                            button.color = BUTTON_ACTIVE_COLOR
                        else:
                            button.color = BUTTON_INACTIVE_COLOR  

                # check if the player name is required
                if event.type == pygame.KEYDOWN:
                    if (event.unicode in string.ascii_letters + ' ') and event.unicode != '' and len(self.player) <=15:
                        self.player += event.unicode
                    if event.key == pygame.K_BACKSPACE:
                        self.player = self.player[:-1]
                    if (event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER) and len(self.player.strip()) > 0:
                        self.player = self.player.strip()
                        self.get_player_name = False
                        self.create_buttons()        

            SCREEN.fill(pygame.Color(SCREEN_BACKGROUND))
            
            # draw cards on screen
            layouts = self.layout.get_layouts()
            for pos in layouts:
                if len(self.hands[pos]) > 0:
                    self.display_stack(self.hands[pos], layouts[pos]['x_0'], layouts[pos]['y_0'])
                    if pos != 'D':
                        card = self.hands[pos][-1]

                        if type(card) == Card:
                            SCREEN.blit(SPRITE, (layouts[pos]['x_0'], layouts[pos]['y_0']), card.rect)
                        
                        elif type(card) == pygame.rect.Rect:
                            SCREEN.blit(SPRITE, (layouts[pos]['x_0'], layouts[pos]['y_0']), card)

            # highlight selected cards
            for pos in self.selected:
                s = pygame.Surface((self.rects[pos][2], self.rects[pos][3]), pygame.SRCALPHA)
                s.fill(HIGHLIGHTED)
                SCREEN.blit(s, (self.rects[pos][0], self.rects[pos][1]))

            # show player stats
            self.show_stats()

            # display help
            if self.help:
                self.show_help()

            # draw buttons
            for button in self.buttons:
                self.draw_button(button)
  
            # display win or lose animations
            if self.win:
                win_grp.draw(SCREEN)
                win_grp.update()
            elif self.lose:
                lose_grp.draw(SCREEN)
                lose_grp.update()

            # check if the game has been lost
            self.check_lose()

            if self.get_player_name:
                self.display_player_name()

            # update the screen
            pygame.display.update()
            CLOCK.tick(GAME_FPS)
    
if __name__ == "__main__":
    game = JockerJB()
    game.start()

    
    
