class Solution:
    # Mistake: counts matching words for every prefix from scratch: O(n^2 * L).
    def prefixScores(self, words):
        out = []
        for w in words:
            total = 0
            for i in range(1, len(w) + 1):
                p = w[:i]
                for x in words:
                    if x.startswith(p):
                        total += 1
            out.append(total)
        return out
