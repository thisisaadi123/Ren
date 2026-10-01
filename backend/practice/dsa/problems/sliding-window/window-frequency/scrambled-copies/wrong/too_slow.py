class Solution:
    # Mistake: re-counts every window from scratch: O(n * m).
    def scrambledCopies(self, text, word):
        m = len(word)
        need = [0] * 26
        for c in word:
            need[ord(c) - 97] += 1
        out = []
        for i in range(len(text) - m + 1):
            have = [0] * 26
            for c in text[i:i + m]:
                have[ord(c) - 97] += 1
            if have == need:
                out.append(i)
        return out
