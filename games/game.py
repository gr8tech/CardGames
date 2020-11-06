import sys
import random

from . import card

def create_deck():
    '''
    Creates a deck to be distributed to Players
    '''
    deck = []
    for rank, value in enumerate(card.CARD_VALUES):
        for symbol in card.CARD_SYMBOLS:
            deck.append(
                card.Card(value, rank, symbol, card.CARD_FONTS[symbol['short']][rank])
            )
    random.shuffle(deck)
    return deck

def deal_deck(deck):
    hand1 = PlayerHand('moosa')
    hand2 = PlayerHand('computer')
    for i in range(len(deck)):
        player_card = deck.pop()
        if i % 2 == 0:
            hand1.stack(player_card)
        else:
            hand2.stack(player_card)
    return hand1, hand2 

class PlayerHand(card.Card):

    def __init__(self, name):
        self.name = name
        self.first_card = None
        self.last_card = None
        self.cards = 0

    def stack(self, player_card):
        if self.last_card:
            player_card.prev_card = self.last_card
            self.last_card.next_card = player_card
            self.last_card = player_card

        else:
            self.first_card = player_card
            self.last_card = player_card
        self.cards += 1

    def push(self, player_card):
        if self.first_card:
            player_card.next_card, self.first_card.prev_card = self.first_card, player_card
            self.first_card = player_card
        else:
            self.first_card = player_card
            self.last_card = player_card
        self.cards += 1

    def pop(self):
        player_card = None
        if self.last_card:
            player_card = self.last_card
            self.last_card = self.last_card.prev_card
            if self.last_card:
                self.last_card.next_card = None
            else:
                self.first_card = None
        self.cards -= 1
        return player_card
        
    def __len__(self):
        return self.cards

    def __str__(self):
        return '{}: {} cards left'.format(self.name, self.cards)

    def _dump(self):
        cards = []
        current_card = self.first_card
        while current_card:
            cards.append(current_card.value)
            current_card = current_card.next_card
        return cards


# if __name__ == "__main__":

    # deck = create_deck()
    # hand1, hand2 = deal_deck(deck)
    # print(hand1)
    # print(hand1._dump())
    # # Enter the game loop
    # while True:
    #     # get player cards
    #     player1_card = hand1.pop()
    #     player2_card = hand2.pop()
    #     war_hand = None
    #     # check winner
    #     while True:
    #         # display cards
    #         print('Player1: ' + str(player1_card.value) + ' Symbol: ' + player1_card.symbol['short'] + ' Rank: ' + str(player1_card.rank))
    #         print('Player2: ' + str(player2_card.value) + ' Symbol: ' + player2_card.symbol['short'] + ' Rank: ' + str(player2_card.rank))
    #         # loop until clear winner in round
    #         if player1_card.rank > player2_card.rank:
    #             hand1.push(player1_card)
    #             hand1.push(player2_card)
    #             print('Player 1 wins round')
    #             print(hand1._dump())
    #             break
    #         elif player1_card.rank < player2_card.rank:
    #             hand2.push(player2_card)
    #             hand2.push(player1_card)
    #             print('Player 2 wins round')
    #             break
    #         else:
    #             # war
    #             print('WAR!!')
    #             if len(hand1) < 4:
    #                 print('Player 2 wins game')
    #                 exit(0)
    #                 break
    #             if len(hand2) < 4:
    #                 print('Player 1 wins game')
    #                 exit(0)
    #                 break
    #             war_hand = PlayerHand('war')
    #             for _ in range(3):
    #                 war_hand.push(hand2.pop())
    #             for _ in range(3):
    #                 war_hand.push(hand1.pop())
    #         # player1_card = hand1.pop()
    #         # player2_card = hand2.pop()
    #         print('PLAYER1', hand1)
    #         print('PLAYER2', hand2)

    #     if len(hand1) == 0:
    #         print('Player 2 wins game')
    #         break
    #     elif len(hand2) == 0:
    #         print('Player 1 wins game')
    #         break
            



