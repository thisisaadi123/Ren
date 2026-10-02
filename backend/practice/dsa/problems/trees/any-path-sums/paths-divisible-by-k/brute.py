class Solution:
    def divisiblePaths(self, root, k):
        nodes, stack = [], [root]
        while stack:
            n = stack.pop()
            nodes.append(n)
            stack += [c for c in (n.left, n.right) if c]
        total = 0
        for start in nodes:
            walk = [(start, start.val)]
            while walk:
                n, s = walk.pop()
                total += s % k == 0
                walk += [(c, s + c.val) for c in (n.left, n.right) if c]
        return total
