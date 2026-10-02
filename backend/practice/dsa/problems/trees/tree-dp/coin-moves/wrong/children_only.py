class Solution:
    # Mistake: only lets coins move between a node and its own children, one level at a time.
    def coinMoves(self, root):
        total, stack = 0, [root]
        while stack:
            n = stack.pop()
            if n:
                for c in (n.left, n.right):
                    if c:
                        total += abs(c.val - 1)
                        stack.append(c)
        return total
