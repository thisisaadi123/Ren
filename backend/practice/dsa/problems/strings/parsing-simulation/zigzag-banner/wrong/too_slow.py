class Solution:
    # Walks the whole text once per row to find that row's characters: O(n · rows).
    def zigzagCode(self, text, rows):
        if rows == 1:
            return text
        cycle = 2 * (rows - 1)
        out = []
        for r in range(rows):
            for i, c in enumerate(text):
                k = i % cycle
                if min(k, cycle - k) == r:
                    out.append(c)
        return "".join(out)
