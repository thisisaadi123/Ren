from collections import Counter


class Solution:
    # Mistake: treats words as a set, so a repeated word only needs to appear once.
    def everyWordOnce(self, s, words):
        L = len(words[0])
        need = set(words)
        w = len(need)
        return [i for i in range(len(s) - L * w + 1)
                if set(s[i + k * L:i + (k + 1) * L] for k in range(w)) == need
                and len(Counter(s[i + k * L:i + (k + 1) * L] for k in range(w))) == w]
