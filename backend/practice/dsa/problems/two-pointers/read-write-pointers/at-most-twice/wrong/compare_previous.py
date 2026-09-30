class Solution:
    # Mistake: compares with the previous input value, which lets a third copy through.
    def keepAtMostTwo(self, values):
        out = []
        run = 0
        for i, x in enumerate(values):
            run = run + 1 if i and x == values[i - 1] else 1
            if run <= 3:
                out.append(x)
        return out
