class Solution:
    # Mistake: the classic early-return search, which returns p or q even when the other is missing.
    def commonOrNone(self, root, p, q):
        def go(t):
            if not t or t.val in (p, q):
                return t
            a, b = go(t.left), go(t.right)
            if a and b:
                return t
            return a or b

        r = go(root)
        return r.val if r else -1
