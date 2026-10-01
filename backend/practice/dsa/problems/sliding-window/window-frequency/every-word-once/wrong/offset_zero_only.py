class Solution:
    # Mistake: only tries starts that are multiples of the word length.
    def everyWordOnce(self, s, words):
        L, w = len(words[0]), len(words)
        need = {}
        for x in words:
            need[x] = need.get(x, 0) + 1
        out = []
        have = {}
        left = 0
        used = 0
        for j in range(0, len(s) - L + 1, L):
            chunk = s[j:j + L]
            if chunk not in need:
                have.clear()
                used = 0
                left = j + L
                continue
            have[chunk] = have.get(chunk, 0) + 1
            used += 1
            while have[chunk] > need[chunk]:
                have[s[left:left + L]] -= 1
                used -= 1
                left += L
            if used == w:
                out.append(left)
                have[s[left:left + L]] -= 1
                used -= 1
                left += L
        return out
