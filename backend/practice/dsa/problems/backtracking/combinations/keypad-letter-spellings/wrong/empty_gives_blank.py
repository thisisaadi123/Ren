class Solution:
    # Mistake: returns [""] for no key presses instead of an empty list.
    def keypadSpellings(self, digits):
        keys = {"2": "abc", "3": "def", "4": "ghi", "5": "jkl", "6": "mno", "7": "pqrs", "8": "tuv", "9": "wxyz"}
        out = [""]
        for d in digits:
            out = [s + ch for s in out for ch in keys[d]]
        return out
