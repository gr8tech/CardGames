def create_deck():
    '''
    Creates a deck
    '''
    deck = []
    for rank, value in enumerate(card.CARD_VALUES):
        for symbol in card.CARD_SYMBOLS:
            deck.append(
                card.Card(value, rank, symbol, card.CARD_FONTS[symbol['short']][rank])
            )
    random.shuffle(deck)
    return deck