class Solution:
    # Mistake: starts writing at grade 1.
    def sortGrades(self, grades):
        count = [0] * 101
        for g in grades:
            count[g] += 1
        out = []
        for g in range(1, 101):
            out.extend([g] * count[g])
        return out
