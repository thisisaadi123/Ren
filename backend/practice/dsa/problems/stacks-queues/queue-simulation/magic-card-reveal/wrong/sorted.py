class Solution:
    # Mistake: stacks the cards in plain sorted order.
    def stackDeck(self, cards):
        return sorted(cards)
