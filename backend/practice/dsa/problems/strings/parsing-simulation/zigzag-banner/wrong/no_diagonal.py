class Solution:
    # Mistake: middle rows only take the characters on the way down, dropping the ones on the way up.
    def zigzagCode(self, text, rows):
        n = len(text)
        if rows == 1 or rows >= n:
            return text
        cycle = 2 * (rows - 1)
        return "".join(text[start + r] for r in range(rows) for start in range(0, n, cycle) if start + r < n)
