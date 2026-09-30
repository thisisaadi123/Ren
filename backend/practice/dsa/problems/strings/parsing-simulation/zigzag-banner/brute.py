class Solution:
    def zigzagCode(self, text, rows):
        lines = [[] for _ in range(rows)]
        r, step = 0, 1
        for c in text:
            lines[r].append(c)
            if rows > 1:
                if r == 0:
                    step = 1
                elif r == rows - 1:
                    step = -1
                r += step
        return "".join("".join(line) for line in lines)
