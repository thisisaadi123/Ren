class Solution:
    # Mistake: lets a value equal a bound, so duplicates pass.
    def isSearchTree(self, root):
        stack = [(root, None, None)]
        while stack:
            node, lo, hi = stack.pop()
            if node is None:
                continue
            if (lo is not None and node.val < lo) or (hi is not None and node.val > hi):
                return False
            stack.append((node.left, lo, node.val))
            stack.append((node.right, node.val, hi))
        return True
