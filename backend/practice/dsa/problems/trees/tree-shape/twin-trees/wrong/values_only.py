class Solution:
    # Mistake: compares the values in level order but ignores where the gaps are.
    def twins(self, a, b):
        def vals(t):
            out, q = [], [t]
            for n in q:
                if n:
                    out.append(n.val)
                    q += [n.left, n.right]
            return out

        return vals(a) == vals(b)
