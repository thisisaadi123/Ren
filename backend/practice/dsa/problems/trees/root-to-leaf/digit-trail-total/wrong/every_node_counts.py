class Solution:
    # Mistake: adds the number spelled at every node, not only at leaves.
    def digitTrailTotal(self, root):
        MOD = 10**9 + 7
        total, stack = 0, [(root, 0)]
        while stack:
            node, x = stack.pop()
            x = (x * 10 + node.val) % MOD
            total += x
            for c in (node.left, node.right):
                if c:
                    stack.append((c, x))
        return total % MOD
