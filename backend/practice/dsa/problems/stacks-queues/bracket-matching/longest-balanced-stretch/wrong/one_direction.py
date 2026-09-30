class Solution:
    # Mistake: a single left-to-right counter pass misses stretches after an unclosed `(`.
    def longestBalanced(self, s):
        best = o = c = 0
        for ch in s:
            if ch == "(":
                o += 1
            else:
                c += 1
            if o == c:
                best = max(best, 2 * c)
            elif c > o:
                o = c = 0
        return best
