class Solution:
    # Mistake: reverses a normal pre-order (node, left, right), which gives right, left, node.
    def cleanupOrder(self, root):
        out, stack = [], [root] if root else []
        while stack:
            node = stack.pop()
            out.append(node.val)
            if node.right:
                stack.append(node.right)
            if node.left:
                stack.append(node.left)
        return out[::-1]
