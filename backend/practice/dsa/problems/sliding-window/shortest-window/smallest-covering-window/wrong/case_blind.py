class Solution:
    # Mistake: treats uppercase and lowercase as the same letter.
    def coverWindow(self, s, t):
        low, lt = s.lower(), t.lower()
        need = {}
        for c in lt:
            need[c] = need.get(c, 0) + 1
        missing = len(lt)
        left = 0
        best = (len(s) + 1, 0)
        for i, c in enumerate(low):
            if need.get(c, 0) > 0:
                missing -= 1
            need[c] = need.get(c, 0) - 1
            while missing == 0:
                if i - left + 1 < best[0]:
                    best = (i - left + 1, left)
                d = low[left]
                need[d] += 1
                if need[d] > 0:
                    missing += 1
                left += 1
        size, start = best
        return s[start:start + size] if size <= len(s) else ""
