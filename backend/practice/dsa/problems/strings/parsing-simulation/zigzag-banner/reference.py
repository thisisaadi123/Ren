class Solution:
    def zigzagCode(self, text, rows):
        n = len(text)
        if rows == 1 or rows >= n:
            return text
        cycle = 2 * (rows - 1)
        out = []
        for r in range(rows):
            for start in range(0, n, cycle):
                if start + r < n:
                    out.append(text[start + r])
                if 0 < r < rows - 1 and start + cycle - r < n:
                    out.append(text[start + cycle - r])
        return "".join(out)
