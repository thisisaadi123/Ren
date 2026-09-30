class Solution:
    # Mistake: writes each grade once.
    def sortGrades(self, grades):
        return sorted(set(grades))
