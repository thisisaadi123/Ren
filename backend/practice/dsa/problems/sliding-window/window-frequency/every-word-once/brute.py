from collections import Counter


class Solution:
    def everyWordOnce(self, s, words):
        L, w = len(words[0]), len(words)
        need = Counter(words)
        return [i for i in range(len(s) - L * w + 1)
                if Counter(s[i + k * L:i + (k + 1) * L] for k in range(w)) == need]
