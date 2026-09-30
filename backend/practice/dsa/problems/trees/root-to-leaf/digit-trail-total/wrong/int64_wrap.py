class Solution:
    # Mistake: builds the numbers in 64-bit integers and only takes the remainder at the end.
    def digitTrailTotal(self, root):
        W = 2**64
        total, stack = 0, [(root, 0)]
        while stack:
            node, x = stack.pop()
            x = (x * 10 + node.val) % W
            if not node.left and not node.right:
                total = (total + x) % W
            for c in (node.left, node.right):
                if c:
                    stack.append((c, x))
        return total % (10**9 + 7)
