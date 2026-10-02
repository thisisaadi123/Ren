class Solution:
    # Mistake: counts only paths that start at the root.
    def divisiblePaths(self, root, k):
        total, stack = 0, [(root, root.val)]
        while stack:
            n, s = stack.pop()
            total += s % k == 0
            stack += [(c, s + c.val) for c in (n.left, n.right) if c]
        return total
