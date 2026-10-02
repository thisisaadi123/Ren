class Solution:
    # Mistake: tries '1' before '0', so the order is reversed.
    def spacedStrings(self, n, ones):
        out = []

        def go(s, left):
            if len(s) == n:
                if left == 0:
                    out.append(s)
                return
            if left and not s.endswith("1"):
                go(s + "1", left - 1)
            go(s + "0", left)

        go("", ones)
        return out
