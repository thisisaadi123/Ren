class Solution:
    # Mistake: jumps back to row 0 after the last row instead of climbing back up.
    def zigzagCode(self, text, rows):
        return "".join(text[r::rows] for r in range(rows))
