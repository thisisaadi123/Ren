class Solution:
    # Mistake: only looks at paths that start at the root.
    def longestPath(self, root, target):
        best, stack = 0, [(root, root.val, 1)]
        while stack:
            n, s, k = stack.pop()
            if s == target:
                best = max(best, k)
            stack += [(c, s + c.val, k + 1) for c in (n.left, n.right) if c]
        return best
