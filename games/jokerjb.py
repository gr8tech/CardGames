'''
Joker jailbreak

Created by Ramon Huiskamp (roofkat).
https://roofkat.itch.io/joker-jailbreak
'''

import pygame
import string
import random

pygame.init()

TITLE = 'Joker Jailbreak'
DISPLAY_HEIGHT = 600
DISPLAY_WIDTH = 800

CARDFONT = pygame.font.Font('../fonts/cards.ttf', 120)

class Card:

    def __init__(self, value, symbol, color):
        self.value = value
        self.symbol = symbol
        self.color = color

class Deck(list):

    def __init__(self, center):
        self.center = center
        list.__init__(self)


def display_card(screen, font, symbol, color, center):
        text_surface = font.render(symbol, True, color)
        text_rect = text_surface.get_rect(center=center)
        screen.blit(text_surface, text_rect)
        return text_surface, text_rect

def create_deck(): 
    cards = []
    i = 1
    for char in string.ascii_letters:
        if char == 'a' or char == 'A' or char == 'n' or char == 'N':
            i = 1
        color = pygame.Color('black')
        if ord(char) >= 65 and ord(char) <= 90:
            color = pygame.Color('red')
        cards.append(Card(i, char, color))
        i += 1
    random.shuffle(cards)
    return cards

if __name__ == "__main__":
        
    cards = create_deck()

    screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()



    jocker_deck = [
        Card(None, '?', pygame.Color('black'))
    ]

    center = (DISPLAY_WIDTH/2, DISPLAY_HEIGHT/2)
    screen.fill(pygame.Color('white'))
    text_surface, text_rect = display_card(screen, CARDFONT, jocker_deck[0].symbol, jocker_deck[0].color, center)

    w = text_rect.width
    h = text_rect.height
    x = DISPLAY_WIDTH/2
    y = DISPLAY_HEIGHT/2
    s = 20

    CENTERS = [
    {
        'center': (x-w-s, y-h-20),
        'type': 'pillar'
    },
    {
        'center': (x, y-h-20),
        'type': 'wall'
    },
    {
        'center': (x+w+s, y-h-20),
        'type': 'pillar'
    },
    {
        'center': (x+w+s, y),
        'type': 'wall'
    },
    {
        'center': (x+w+s, y+h+20),
        'type': 'pillar'
    },
    {
        'center': (x, y+h+20),
        'type': 'wall'
    },
    {
        'center': (x-w-20, y+h+20),
        'type': 'pillar'
    },
    {
        'center': (x-w-20, y),
        'type': 'wall'
    }
]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # screen.fill(pygame.Color('white'))
        # for card in jocker_deck:
        #     center = (DISPLAY_WIDTH/2, DISPLAY_HEIGHT/2)
        #     display_card(screen, CARDFONT, card.symbol, card.color, center)
        # for center in deck_centers:
        #     display_card(screen, CARDFONT, jocker_deck[0].symbol, jocker_deck[0].color, center['center'])


        
        pygame.display.update()
        clock.tick(60)

