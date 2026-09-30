class Solution:
    # Mistake: takes words greedily from the highest score down; an early big word can block a better pair.
    def bestWordSet(self, words, tiles, points):
        bag = collections.Counter(tiles)
        total = 0
        for w in sorted(words, key=lambda w: -sum(points[ord(c) - 97] for c in w)):
            need = collections.Counter(w)
            if all(bag[c] >= k for c, k in need.items()):
                bag -= need
                total += sum(points[ord(c) - 97] for c in w)
        return total
