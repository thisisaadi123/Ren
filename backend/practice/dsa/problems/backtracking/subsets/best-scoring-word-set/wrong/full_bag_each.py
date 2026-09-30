class Solution:
    # Mistake: checks every word against the full bag, so two words can share the same tiles.
    def bestWordSet(self, words, tiles, points):
        bag = collections.Counter(tiles)
        total = 0
        for w in words:
            need = collections.Counter(w)
            if all(bag[c] >= k for c, k in need.items()):
                total += sum(points[ord(c) - 97] for c in w)
        return total
