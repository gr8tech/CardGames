import pygame
from . import game
import time
import copy
import gui

from pygame_textinput import TextInput
    
GAME_TITLE = 'WAR'

FONT_SIZE = 120
FONT_DARK = 'fonts/pdark.ttf'
NORMAL_FONT = 'fonts/ShareTechMono-Regular.ttf'
CARDS_FONT = 'fonts/cards.ttf'
INTRO_BACKGROUND = 'images/cards2.jpg'
DECK_BACK = 'images/back.png'

TABLE_MAT_WIDTH = 699
TABLE_MAT_HEIGHT = 264
TABLE_MAT_POS = (51, 168)
LEFT_PLAYER_CARD_POS =  (270, 234.5)
RIGHT_PLAYER_CARD_POS = (421, 234.5)
LEFT_PLAYER_DECK_POS = (42, 31)
LEFT_WAR_HAND = (121, 234.5)
RIGHT_WAR_HAND = (570, 234.5)
RIGHT_PLAYER_DECK_POS = (648, 451)
PLAY_BUTTON_POS = (540, 542, 80, 40)
QUIT_BUTTON_POS = (50, 542, 80, 40)

DECK_FONT = pygame.font.Font(FONT_DARK, 50)


class CardGame:

    def __init__(self, g):
        self.g = g
        self.screen = self.g.screen
        self.g.screen.fill(gui.OFFWHITE)
        pygame.display.set_caption(GAME_TITLE)
        self.game_exit = False
        self.local_hand = None
        

    def put_card(self, hand, pos):
        # play game
        player_card = hand.pop()
        if player_card.symbol['short'] == 'D' or player_card.symbol['short'] == 'H':
            color = COLOR_RED
        else:
            color = COLOR_BLACK
        self.g.message_display(player_card.font, top=pos[1], left=pos[0], font_size=FONT_SIZE, color=color, font=CARDS_FONT)
        pygame.display.update()
        return player_card

    def display_deck(self, player1=0, player2=0):
        # Left player
        self.g.display_image(DECK_BACK, LEFT_PLAYER_DECK_POS)
        self.g.message_display(str(player2), top=LEFT_PLAYER_DECK_POS[1], left=LEFT_PLAYER_DECK_POS[0], font_size=50, color=COLOR_BLACK, font=NORMAL_FONT)
        # Right player
        self.g.display_image(DECK_BACK, RIGHT_PLAYER_DECK_POS)
        self.g.message_display(str(player1), top=RIGHT_PLAYER_DECK_POS[1], left=RIGHT_PLAYER_DECK_POS[0], font_size=50, color=COLOR_BLACK, font=NORMAL_FONT)

    def display_war_hand(self, hand):
        self.g.display_image(DECK_BACK, LEFT_WAR_HAND)
        self.g.display_image(DECK_BACK, RIGHT_WAR_HAND)
        cards = int(len(hand)/2)
        self.g.message_display(str(cards), top=LEFT_WAR_HAND[1], left=LEFT_WAR_HAND[0], font_size=50, color=COLOR_BLACK, font=NORMAL_FONT)
        self.g.message_display(str(cards), top=RIGHT_WAR_HAND[1], left=RIGHT_WAR_HAND[0], font_size=50, color=COLOR_BLACK, font=NORMAL_FONT)
    
    def display_splash(self):
        self.g.screen.fill(gui.WHITE)
        self.g.display_image(INTRO_BACKGROUND)
        self.g.display_text(gui.TITLE_FONT, 'WAR', gui.RED, (gui.DISPLAY_WIDTH/2, gui.DISPLAY_HEIGHT/2) )
        # pygame.display.update()

    def display_textinput(self, textinput, events):
        # input background rect
        rect = pygame.Rect(20, gui.DISPLAY_HEIGHT-102, 300, 30)
        # Feed input with events every frame
        textinput.update(events)
        # Blit its surface onto the screen
        pygame.draw.rect(self.g.screen, gui.WHITE, rect)
        self.g.screen.blit(textinput.get_surface(), (25, gui.DISPLAY_HEIGHT-100))

    def start(self):
        textinput = TextInput(text_color=gui.RED)
        clock = pygame.time.Clock()
        print(textinput.get_surface().get_rect())

        while True:
            self.display_splash()
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    exit()

            self.display_textinput(textinput, events)

            pygame.display.update()
            clock.tick(60)

    # def start(self):
    #     self.display_splash()
    #     # self.game_loop()
    #     # Create TextInput-object
    #     textinput = TextInput(text_color=gui.RED)
    #     while True:
    #         events = pygame.event.get()
    #         for event in events:
    #             if event.type == pygame.QUIT:
    #                 exit()
    #         textinput.update(events)
    #         # Blit its surface onto the screen
    #         self.g.screen.blit(textinput.get_surface(), (100, 500))
    #         pygame.display.update()
    #         self.g.clock.tick(60)

    def game_loop(self):
        deck = game.create_deck()
        hand1, hand2 = game.deal_deck(deck)

        hand2=copy.deepcopy(hand1)

        self.display_deck(len(hand1), len(hand2))
        play_button = self.create_button(
            'PLAY', *PLAY_BUTTON_POS, self.put_card
        )
        quit_button = self.create_button(
            'EXIT', *QUIT_BUTTON_POS, self.game_exit
        )
        buttons = [
            play_button,
            quit_button
        ]
        
        self.game_display.fill(COLOR_WHITE)
        for button in buttons:
            self.draw_button(self.game_display, button)
        pygame.display.update()

        war_hand = None

        while not self.game_exit:
            if len(hand1) == 0 or len(hand2) == 0:
                break

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_exit = True
                elif event.type == pygame.MOUSEMOTION:
                    if play_button['rect'].collidepoint(event.pos):
                        play_button['color'] = COLOR_HOVER_BLUE
                    else:
                        play_button['color'] = COLOR_BLUE
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        for button in buttons:
                            if button['rect'].collidepoint(event.pos):
                                # self.display_deck(len(hand1), len(hand2))  
                                # if war_hand:
                                #     self.display_war_hand(war_hand)
                                player1_card = button['callback'](hand1, RIGHT_PLAYER_CARD_POS[:2])
                                time.sleep(1)
                                player2_card = button['callback'](hand2, LEFT_PLAYER_CARD_POS[:2])
                                time.sleep(1)
                                # self.game_display.fill(COLOR_WHITE)
                                
                                if player1_card.rank > player2_card.rank:
                                    hand1.push(player1_card)
                                    hand1.push(player2_card)
                                    war_hand = None
                                    break
                                elif player1_card.rank < player2_card.rank:
                                    hand2.push(player2_card)
                                    hand2.push(player1_card)
                                    war_hand = None
                                    break
                                else:
                                    # war
                                    self.g.message_display('WAR!!!!',color=COLOR_RED, center=((DISPLAY_WIDTH/2), (RIGHT_PLAYER_CARD_POS[1]-50)), font_size=50, font=NORMAL_FONT)
                                    time.sleep(1)
                                    if len(hand1) < 4:
                                        print('Player 2 wins game')
                                        exit(0)
                                        break
                                    if len(hand2) < 4:
                                        print('Player 1 wins game')
                                        exit(0)
                                        break
                                    if war_hand ==None:
                                        war_hand = game.PlayerHand('war')
                                    for _ in range(3):
                                        war_hand.push(hand2.pop())
                                    for _ in range(3):
                                        war_hand.push(hand1.pop())

            # right player button
            # self.button()

            # play game
            # player1_card = hand1.pop()
            # if player1_card.symbol['short'] == 'D' or player1_card.symbol['short'] == 'H':
            #     color = COLOR_RED
            # else:
            #     color = COLOR_BLACK
            # self.g.message_display(player1_card.font, top=RIGHT_PLAYER_CARD_POS[1], left=RIGHT_PLAYER_CARD_POS[0], font_size=FONT_SIZE, color=color, font=CARDS_FONT)
            # time.sleep(2)
            # player2_card = hand2.pop()
            # if player2_card.symbol['short'] == 'D' or player2_card.symbol['short'] == 'H':
            #     color = COLOR_RED
            # else:
            #     color = COLOR_BLACK
            # self.g.message_display(player2_card.font, top=LEFT_PLAYER_CARD_POS[1], left=LEFT_PLAYER_CARD_POS[0], font_size=FONT_SIZE, color=color, font=CARDS_FONT)
            # time.sleep(2)
            # war_hand = None

            

            # self.game_display.fill(COLOR_WHITE)
                            self.game_display.fill(COLOR_WHITE)
                            self.display_deck(len(hand1), len(hand2))    
                            if war_hand:
                                self.display_war_hand(war_hand)
                            for button in buttons:
                                self.draw_button(self.game_display, button)
                            pygame.display.update()
            self.clock.tick(60)
            

    def game_quit(self):
        pygame.quit()
        quit()

if __name__ == "__main__":
    card_game = CardGame()
    card_game.start()