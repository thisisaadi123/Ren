class Solution:
    def totalsFromTop(self, root):
        vals = []

        def collect(t):
            if t:
                vals.append(t.val)
                collect(t.left)
                collect(t.right)

        collect(root)

        def rewrite(t):
            if t:
                old = t.val
                t.val = sum(v for v in vals if v >= old)
                rewrite(t.left)
                rewrite(t.right)

        rewrite(root)
        return root
