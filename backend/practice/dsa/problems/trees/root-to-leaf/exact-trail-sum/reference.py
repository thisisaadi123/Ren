class Solution:
    def hasTrailSum(self, root, target):
        stack = [(root, target)] if root else []
        while stack:
            node, left = stack.pop()
            left -= node.val
            if not node.left and not node.right and left == 0:
                return True
            for c in (node.left, node.right):
                if c:
                    stack.append((c, left))
        return False
