class Solution:
    # Mistake: compares the set of values on each level, which ignores who is whose child.
    def flipEquivalent(self, a, b):
        def levels(t):
            out, cur = [], [t] if t else []
            while cur:
                out.append(sorted(n.val for n in cur))
                cur = [c for n in cur for c in (n.left, n.right) if c]
            return out

        return levels(a) == levels(b)
