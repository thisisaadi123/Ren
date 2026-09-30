class Solution:
    def giftBundles(self, cards, target):
        n = len(cards)
        seen = set()
        for mask in range(1 << n):
            pick = [cards[i] for i in range(n) if mask >> i & 1]
            if sum(pick) == target:
                seen.add(tuple(sorted(pick)))
        return [list(t) for t in seen]
