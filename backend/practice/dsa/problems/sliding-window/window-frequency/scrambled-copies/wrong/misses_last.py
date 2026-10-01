class Solution:
    # Mistake: stops before the last window.
    def scrambledCopies(self, text, word):
        m = len(word)
        if m > len(text):
            return []
        need = [0] * 26
        have = [0] * 26
        for c in word:
            need[ord(c) - 97] += 1
        out = []
        for i in range(len(text) - 1):
            have[ord(text[i]) - 97] += 1
            if i >= m:
                have[ord(text[i - m]) - 97] -= 1
            if i >= m - 1 and have == need:
                out.append(i - m + 1)
        return out
