class Solution:
    # Mistake: keeps counting when the walk goes the same way twice, so it measures plain depth.
    def longestZigzag(self, root):
        best = 0
        stack = [(root, 0)]
        while stack:
            n, length = stack.pop()
            best = max(best, length)
            stack += [(c, length + 1) for c in (n.left, n.right) if c]
        return best
