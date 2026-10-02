class Solution:
    # Mistake: checks each node alone and each parent-child pair, not longer paths.
    def divisiblePaths(self, root, k):
        total, stack = 0, [root]
        while stack:
            n = stack.pop()
            total += n.val % k == 0
            for c in (n.left, n.right):
                if c:
                    total += (n.val + c.val) % k == 0
                    stack.append(c)
        return total
