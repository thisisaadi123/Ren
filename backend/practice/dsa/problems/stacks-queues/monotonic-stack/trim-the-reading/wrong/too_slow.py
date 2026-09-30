class Solution:
    # Mistake: deletes one digit per pass, rescanning from the left each time: O(n·k).
    def trimReading(self, num, k):
        s = num
        for _ in range(k):
            i = 0
            while i + 1 < len(s) and s[i] <= s[i + 1]:
                i += 1
            s = s[:i] + s[i + 1:]
        return s.lstrip("0") or "0"
