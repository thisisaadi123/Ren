class Solution:
    def sameText(self, a, b):
        def screen(keys):
            out = []
            for c in keys:
                if c == "#":
                    if out:
                        out.pop()
                else:
                    out.append(c)
            return out

        return screen(a) == screen(b)
