class Solution:
    def hasTrailSum(self, root, target):
        totals = []

        def walk(node, s):
            s += node.val
            if not node.left and not node.right:
                totals.append(s)
            for c in (node.left, node.right):
                if c:
                    walk(c, s)

        if root:
            walk(root, 0)
        return target in totals
