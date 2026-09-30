class Solution:
    # Mistake: accepts a trail that stops at a checkpoint that still has children.
    def hasTrailSum(self, root, target):
        stack = [(root, target)] if root else []
        while stack:
            node, left = stack.pop()
            left -= node.val
            if left == 0:
                return True
            for c in (node.left, node.right):
                if c:
                    stack.append((c, left))
        return False
