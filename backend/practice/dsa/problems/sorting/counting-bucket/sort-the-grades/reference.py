class Solution:
    def sortGrades(self, grades):
        count = [0] * 101
        for g in grades:
            count[g] += 1
        out = []
        for g, c in enumerate(count):
            out.extend([g] * c)
        return out
