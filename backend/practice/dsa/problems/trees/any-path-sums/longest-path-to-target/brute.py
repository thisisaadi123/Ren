class Solution:
    def longestPath(self, root, target):
        nodes, stack = [], [root]
        while stack:
            n = stack.pop()
            nodes.append(n)
            stack += [c for c in (n.left, n.right) if c]
        best = 0
        for start in nodes:
            walk = [(start, start.val, 1)]
            while walk:
                n, s, k = walk.pop()
                if s == target:
                    best = max(best, k)
                walk += [(c, s + c.val, k + 1) for c in (n.left, n.right) if c]
        return best
