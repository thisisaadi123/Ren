import itertools
class Solution:
    def keypadSpellings(self, digits):
        keys = ["", "", "abc", "def", "ghi", "jkl", "mno", "pqrs", "tuv", "wxyz"]
        if not digits:
            return []
        return ["".join(p) for p in itertools.product(*[keys[int(d)] for d in digits])]
