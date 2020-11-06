import unittest
import main
import card
import random

class War(unittest.TestCase):

    def setUp(self):
        random.seed(112827287323)
        self.deck = ['2', 'Q', '6', 'Q', '9', 'K', 'K', '2', '3', '5', '10', '7', 'J', '8', '6', '7', '8', '10', '3', '7', '5', 'Q', '9', '4', '5', '2', '7', '5', 'A', 'K', 'A', '6', '3', '8', 'Q', '9', '4', 'A', '4', '9', 'A', '8', '10', '10', '6', 'J', 'J', 'J', 'K', '4', '3', '2']
        self.player_card = card.Card(2, 0, {
            'name': 'WHITE HEART SUIT',
            'short': 'WH',
            'unicode': '\u2661'
        })

    def test_card_str(self):
        self.assertEqual(str(self.player_card), '2')

    def test_card_repr(self):
        self.assertEqual(repr(self.player_card), '2')

    def test_create_deck(self):
        deck = main.create_deck()
        for idx,item in enumerate(deck):
            self.assertEqual(item.value, self.deck[idx])

    def test_deal_deck(self):
        hand1, hand2 = main.deal_deck(deck)


    # def test_create_card(self):
    #     card1 = 
    #     self.assertEqual(card1.prev_card, None)
    #     self.assertEqual(card1.next_card, None)
    #     self.assertEqual(card1.value, 2)
    #     self.assertEqual(card1.rank,  0)
    #     self.assertIn(card1.symbol, card.CARD_SYMBOLS)