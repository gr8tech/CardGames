CARD_SYMBOLS = [
    {
        'name': 'WHITE HEART SUIT',
        'short': 'H',
        'unicode': '\u2661'
    },
    {
        'name': 'WHITE DIAMOND SUIT',
        'short': 'D',
        'unicode': '\u2662'
    },
    {
        'name': 'WHITE SPADE SUIT',
        'short': 'J',
        'unicode': '\u2664'
    },
    {
        'name': 'WHITE CLUB SUIT',
        'short': 'C',
        'unicode': '\u2667'
    },
]

# applicable cards in ascending order of rank
CARD_VALUES = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
CARD_FONTS = {
    'D':'BCDEFGHIJKLMA',
    'H':'OPQRSTUVWXYZN',
    'J':'bcdefghijklma',
    'C':'opqrstuvwxyzn'
}

class Card():
    '''
    Represent a card in a deck
    '''

    def __init__(self, value, rank, symbol, font):
        self.rank = rank
        self.value = value
        self.symbol = symbol
        self.font = font
        # card will be part of a double linked list in a player deck
        self.prev_card = None
        self.next_card = None

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return str(self.value) #+ ' ' + self.symbol['unicode'] + ' - ' + str(self.rank)
