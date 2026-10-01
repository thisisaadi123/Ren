class Solution:
    # Mistake: on a tie keeps the later window instead of the leftmost.
    def coverWindow(self, s, t):
        need = {}
        for c in t:
            need[c] = need.get(c, 0) + 1
        missing = len(t)
        left = 0
        best = (len(s) + 1, 0)
        for i, c in enumerate(s):
            if need.get(c, 0) > 0:
                missing -= 1
            need[c] = need.get(c, 0) - 1
            while missing == 0:
                if i - left + 1 <= best[0]:
                    best = (i - left + 1, left)
                d = s[left]
                need[d] += 1
                if need[d] > 0:
                    missing += 1
                left += 1
        size, start = best
        return s[start:start + size] if size <= len(s) else ""
