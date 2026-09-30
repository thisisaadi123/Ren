class Solution:
    # Mistake: a missing child ends a path, so one-child nodes are counted as path ends.
    def digitTrailTotal(self, root):
        MOD = 10**9 + 7

        def walk(node, x):
            if node is None:
                return x
            x = (x * 10 + node.val) % MOD
            if not node.left and not node.right:
                return x
            return (walk(node.left, x) + walk(node.right, x)) % MOD

        return walk(root, 0)
