class Solution:
    def everyWordOnce(self, s, words):
        L, w = len(words[0]), len(words)
        need = {}
        for x in words:
            need[x] = need.get(x, 0) + 1
        out = []
        for off in range(L):
            have = {}
            left = off
            used = 0
            for j in range(off, len(s) - L + 1, L):
                chunk = s[j:j + L]
                if chunk not in need:
                    have.clear()
                    used = 0
                    left = j + L
                    continue
                have[chunk] = have.get(chunk, 0) + 1
                used += 1
                while have[chunk] > need[chunk]:
                    first = s[left:left + L]
                    have[first] -= 1
                    used -= 1
                    left += L
                if used == w:
                    out.append(left)
                    first = s[left:left + L]
                    have[first] -= 1
                    used -= 1
                    left += L
        out.sort()
        return out
