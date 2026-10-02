class Solution:
    # Mistake: only counts paths that end at a leaf.
    def countPaths(self, root, target):
        total, stack = 0, [(root, [])]
        while stack:
            n, path = stack.pop()
            path = path + [n.val]
            if not n.left and not n.right:
                s = 0
                for v in reversed(path):
                    s += v
                    total += s == target
            stack += [(c, path) for c in (n.left, n.right) if c]
        return total
