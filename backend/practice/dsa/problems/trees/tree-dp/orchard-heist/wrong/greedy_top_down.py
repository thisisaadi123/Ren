class Solution:
    # Mistake: decides at each node by comparing it with its children alone.
    def mostApples(self, root):
        def go(t):
            if not t:
                return 0
            kids = (t.left.val if t.left else 0) + (t.right.val if t.right else 0)
            if t.val >= kids:
                g = lambda c: go(c.left) + go(c.right) if c else 0
                return t.val + g(t.left) + g(t.right)
            return go(t.left) + go(t.right)

        return go(root)
