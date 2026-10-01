from collections import Counter


class Solution:
    # Mistake: rebuilds the chunk counts at every start: O(n * words).
    def everyWordOnce(self, s, words):
        L, w = len(words[0]), len(words)
        need = Counter(words)
        out = []
        for i in range(len(s) - L * w + 1):
            have = Counter()
            for k in range(w):
                chunk = s[i + k * L:i + (k + 1) * L]
                have[chunk] += 1
                if have[chunk] > need[chunk]:
                    break
            else:
                out.append(i)
        return out
