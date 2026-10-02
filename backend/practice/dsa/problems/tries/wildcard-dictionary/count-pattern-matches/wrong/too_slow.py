class Solution:
    # Mistake: compares every pattern with every word: O(P * W * L).
    def countMatches(self, words, patterns):
        out = []
        for p in patterns:
            n = 0
            for w in words:
                if len(w) != len(p):
                    continue
                ok = True
                for a, b in zip(p, w):
                    if a != "." and a != b:
                        ok = False
                        break
                if ok:
                    n += 1
            out.append(n)
        return out
