class Solution:
    def bestWordSet(self, words, tiles, points):
        have = collections.Counter(tiles)
        n = len(words)
        best = 0
        for mask in range(1 << n):
            used = collections.Counter()
            for i in range(n):
                if mask >> i & 1:
                    used.update(words[i])
            if all(used[c] <= have[c] for c in used):
                best = max(best, sum(points[ord(c) - 97] * k for c, k in used.items()))
        return best
