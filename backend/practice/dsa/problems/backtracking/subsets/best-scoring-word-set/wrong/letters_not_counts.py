class Solution:
    # Mistake: only checks that each letter is present, not how many tiles of it remain.
    def bestWordSet(self, words, tiles, points):
        n = len(words)
        best = 0
        def go(i, bag, score):
            nonlocal best
            best = max(best, score)
            if i == n:
                return
            w = words[i]
            if all(bag[c] > 0 for c in w):
                nb = bag.copy()
                nb.subtract(w)
                go(i + 1, nb, score + sum(points[ord(c) - 97] for c in w))
            go(i + 1, bag, score)
        go(0, collections.Counter(tiles), 0)
        return best
