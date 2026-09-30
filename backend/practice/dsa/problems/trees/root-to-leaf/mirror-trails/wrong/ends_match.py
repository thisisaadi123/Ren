class Solution:
    # Mistake: only checks that the root digit equals the leaf digit.
    def mirrorTrails(self, root):
        count, stack = 0, [root]
        while stack:
            node = stack.pop()
            if not node.left and not node.right:
                count += node.val == root.val
            stack.extend(c for c in (node.left, node.right) if c)
        return count
