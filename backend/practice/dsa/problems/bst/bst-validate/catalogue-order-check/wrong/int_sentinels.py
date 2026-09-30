class Solution:
    # Mistake: starts the range at the 32-bit extremes, which are themselves legal values.
    def isSearchTree(self, root):
        stack = [(root, -2**31, 2**31 - 1)]
        while stack:
            node, lo, hi = stack.pop()
            if node is None:
                continue
            if not lo < node.val < hi:
                return False
            stack.append((node.left, lo, node.val))
            stack.append((node.right, node.val, hi))
        return True
