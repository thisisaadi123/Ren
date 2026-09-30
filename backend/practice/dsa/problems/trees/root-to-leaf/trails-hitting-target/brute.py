class Solution:
    def trailsWithSum(self, root, target):
        # Build every root-to-leaf path as a fresh tuple, left to right, then filter.
        def paths(node):
            if not node.left and not node.right:
                return [(node.val,)]
            res = []
            for c in (node.left, node.right):
                if c:
                    res += [(node.val,) + p for p in paths(c)]
            return res

        if not root:
            return []
        return [list(p) for p in paths(root) if sum(p) == target]
