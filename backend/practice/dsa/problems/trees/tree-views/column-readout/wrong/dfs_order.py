class Solution:
    # Mistake: lists each column in depth-first order, so lower nodes can come before higher ones.
    def columnReadout(self, root):
        cols = {}

        def walk(t, c):
            if t:
                cols.setdefault(c, []).append(t.val)
                walk(t.left, c - 1)
                walk(t.right, c + 1)

        walk(root, 0)
        return [cols[c] for c in sorted(cols)]
