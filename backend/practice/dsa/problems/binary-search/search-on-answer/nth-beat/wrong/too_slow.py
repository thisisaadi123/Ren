class Solution:
    # Merges the two sequences one beat at a time: O(n).
    def nthBeat(self, n, a, b):
        x = y = 0
        beat = 0
        for _ in range(n):
            na, nb = x + a, y + b
            beat = min(na, nb)
            if na == beat:
                x = na
            if nb == beat:
                y = nb
        return beat % (10**9 + 7)
