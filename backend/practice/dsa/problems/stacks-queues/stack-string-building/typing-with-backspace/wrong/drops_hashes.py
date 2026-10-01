class Solution:
    # Mistake: ignores backspaces and compares the letters typed.
    def sameText(self, a, b):
        return a.replace("#", "") == b.replace("#", "")
