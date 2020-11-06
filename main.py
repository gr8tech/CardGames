import pygame
import game
import time
import copy


pygame.init()
    
GAME_TITLE = 'WAR'
DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 600
COLOR_WHITE = (255, 255, 255)
COLOR_RED = (255, 0, 0)
COLOR_OFFWHITE = (180, 180, 180)
COLOR_BLACK = (0, 0, 0)
COLOR_BLUE = (33, 40, 227)
COLOR_HOVER_BLUE = (99, 103, 231)
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
RIGHT_PLAYER_DECK_POS = (648, 451)
PLAY_BUTTON_POS = (540, 542, 80, 40)
BUTTON_FONT = pygame.font.Font(FONT_DARK, 20)
DECK_FONT = pygame.font.Font(FONT_DARK, 50)


class CardGame:

    def __init__(self):
        self.game_display = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
        self.game_display.fill(COLOR_OFFWHITE)
        pygame.display.set_caption(GAME_TITLE)
        self.clock = pygame.time.Clock()
        self.game_exit = False
        self.local_hand = None

    def text_objects(self, message, font, color):
        text_surface = font.render(message, True, color)
        return text_surface, text_surface.get_rect()

    def message_display(self, message, color=COLOR_BLACK, center = ((DISPLAY_WIDTH/2), (DISPLAY_HEIGHT/2)), font=FONT_DARK, top=None, left=None, font_size=120):
        font = pygame.font.Font(font, font_size)
        text_surface, text_rect = self.text_objects(message, font, color)
        if not top and not left:
            text_rect.center = center
        else:
            text_rect.top = top
            text_rect.left = left
        self.game_display.blit(text_surface, text_rect)
        # pygame.display.update()

    def display_image(self, image, location=(0,0)):
        img = pygame.image.load(image)
        self.game_display.blit(img, location)

    def put_card(self, hand, pos):
        # play game
        player_card = hand.pop()
        if player_card.symbol['short'] == 'D' or player_card.symbol['short'] == 'H':
            color = COLOR_RED
        else:
            color = COLOR_BLACK
        self.message_display(player_card.font, top=pos[1], left=pos[0], font_size=FONT_SIZE, color=color, font=CARDS_FONT)
        pygame.display.update()
        return player_card

    def draw_button(self, screen, button):
        pygame.draw.rect(screen, button['color'], button['rect'])
        screen.blit(button['title'], button['title_rect'])

    def create_button(self, title, x,y,width,height, callback):
        text_mid_point_x = x + width/2
        text_mid_point_y = y + height/2
        button_rect = pygame.Rect(x,y,width,height)
        text_surface = BUTTON_FONT.render(title, True, COLOR_WHITE)
        text_rect = text_surface.get_rect(center=button_rect.center)
        button = {
            'rect': button_rect,
            'title': text_surface,
            'title_rect': text_rect,
            'color': COLOR_BLUE,
            'callback': callback
        }
        return button

    def display_deck(self, player1=0, player2=0):
        # Left player
        self.display_image(DECK_BACK, LEFT_PLAYER_DECK_POS)
        self.message_display(str(player2), top=LEFT_PLAYER_DECK_POS[1], left=LEFT_PLAYER_DECK_POS[0], font_size=50, color=COLOR_BLACK, font=NORMAL_FONT)
        # Right player
        self.display_image(DECK_BACK, RIGHT_PLAYER_DECK_POS)
        self.message_display(str(player1), top=RIGHT_PLAYER_DECK_POS[1], left=RIGHT_PLAYER_DECK_POS[0], font_size=50, color=COLOR_BLACK, font=NORMAL_FONT)

    # def update_deck():
    #     self.game_display.fill(COLOR_WHITE)
    #     self.display_deck(len(hand1), len(hand2))
    
    def start(self):
        self.display_image(INTRO_BACKGROUND)
        self.message_display('WAR', COLOR_RED)
        pygame.display.update()
        time.sleep(2)
        self.game_loop()

    def game_loop(self):
        deck = game.create_deck()
        hand1, hand2 = game.deal_deck(deck)
        self.display_deck(len(hand1), len(hand2))
        play_button = self.create_button(
            'PLAY', *PLAY_BUTTON_POS, self.put_card
        )
        buttons = [
            play_button
        ]
        
        self.game_display.fill(COLOR_WHITE)
        for button in buttons:
            self.draw_button(self.game_display, button)
        pygame.display.update()

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
                                self.game_display.fill(COLOR_WHITE)
                                self.display_deck(len(hand1), len(hand2))  
                                player1_card = button['callback'](hand1, RIGHT_PLAYER_CARD_POS[:2])
                                time.sleep(1)
                                player2_card = button['callback'](hand2, LEFT_PLAYER_CARD_POS[:2])
                                time.sleep(1)
                                self.game_display.fill(COLOR_WHITE)
                                
                                if player1_card.rank > player2_card.rank:
                                    hand1.push(player1_card)
                                    hand1.push(player2_card)
                                    break
                                elif player1_card.rank < player2_card.rank:
                                    hand2.push(player2_card)
                                    hand2.push(player1_card)
                                    break
                                else:
                                    # war
                                    self.message_display('WAR!!!!',color=COLOR_RED, center=((DISPLAY_WIDTH/2), (RIGHT_PLAYER_CARD_POS[1]-50)), font_size=50, font=NORMAL_FONT)
                                    time.sleep(1)
                                
                                        # print('WAR!!')
                                        # if len(hand1) < 4:
                                        #     print('Player 2 wins game')
                                        #     exit(0)
                                        #     break
                                        # if len(hand2) < 4:
                                        #     print('Player 1 wins game')
                                        #     exit(0)
                                        #     break
                                        # war_hand = PlayerHand('war')
                                        # for _ in range(3):
                                        #     war_hand.push(hand2.pop())
                                        # for _ in range(3):
                                        #     war_hand.push(hand1.pop())

            # right player button
            # self.button()

            # play game
            # player1_card = hand1.pop()
            # if player1_card.symbol['short'] == 'D' or player1_card.symbol['short'] == 'H':
            #     color = COLOR_RED
            # else:
            #     color = COLOR_BLACK
            # self.message_display(player1_card.font, top=RIGHT_PLAYER_CARD_POS[1], left=RIGHT_PLAYER_CARD_POS[0], font_size=FONT_SIZE, color=color, font=CARDS_FONT)
            # time.sleep(2)
            # player2_card = hand2.pop()
            # if player2_card.symbol['short'] == 'D' or player2_card.symbol['short'] == 'H':
            #     color = COLOR_RED
            # else:
            #     color = COLOR_BLACK
            # self.message_display(player2_card.font, top=LEFT_PLAYER_CARD_POS[1], left=LEFT_PLAYER_CARD_POS[0], font_size=FONT_SIZE, color=color, font=CARDS_FONT)
            # time.sleep(2)
            # war_hand = None

            

            # self.game_display.fill(COLOR_WHITE)
            self.display_deck(len(hand1), len(hand2))    
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