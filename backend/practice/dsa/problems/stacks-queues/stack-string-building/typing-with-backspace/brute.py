class Solution:
    def sameText(self, a, b):
        def screen(keys):
            s = ""
            for c in keys:
                s = s[:-1] if c == "#" else s + c
            return s

        return screen(a) == screen(b)
