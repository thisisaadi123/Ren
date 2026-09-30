class Solution:
    def keypadSpellings(self, digits):
        keys = {"2": "abc", "3": "def", "4": "ghi", "5": "jkl", "6": "mno", "7": "pqrs", "8": "tuv", "9": "wxyz"}
        if not digits:
            return []
        out, cur = [], []

        def go(i):
            if i == len(digits):
                out.append("".join(cur))
                return
            for ch in keys[digits[i]]:
                cur.append(ch)
                go(i + 1)
                cur.pop()

        go(0)
        return out
