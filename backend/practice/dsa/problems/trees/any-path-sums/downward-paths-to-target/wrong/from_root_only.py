class Solution:
    # Mistake: counts only paths that start at the root.
    def countPaths(self, root, target):
        total, stack = 0, [(root, root.val)]
        while stack:
            n, s = stack.pop()
            total += s == target
            stack += [(c, s + c.val) for c in (n.left, n.right) if c]
        return total
