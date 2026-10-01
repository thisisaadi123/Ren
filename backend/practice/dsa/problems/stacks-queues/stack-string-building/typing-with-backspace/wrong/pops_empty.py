class Solution:
    # Mistake: a backspace on an empty box crashes instead of doing nothing.
    def sameText(self, a, b):
        def screen(keys):
            out = []
            for c in keys:
                if c == "#":
                    out.pop()
                else:
                    out.append(c)
            return out

        return screen(a) == screen(b)
